import numpy as np

from scipy.cluster.hierarchy import dendrogram, cophenet
from scipy.spatial.distance import pdist, squareform

from sklearn.metrics import silhouette_samples, silhouette_score

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.cm as cm


def cophenetic_corr(linkage_matrix, data_mtx, distance_measure='euclidean'):

    """
    Calculates cophenetic correlation.

    :param linkage_matrix: Linkage matrix.
    :param data_mtx: Data if distce measure is not "precomputed", pairwise distances otherwise.
    :param distance_measure: Distance mesure name.
    """
    
    if distance_measure != 'precomputed':
        
        cop_corr = cophenet(
            linkage_matrix, 
            pdist(data_mtx, metric=distance_measure),
        )[0]
        
    else:
        
        cop_corr = cophenet(
            linkage_matrix, 
            squareform(data_mtx),
        )[0]
        
    print(
        'Cophenetic correlation : {}'.format(cop_corr)
    )
    


def plot_cluster_dendrogram(
    clusters, linkage_matrix, dataset_df, orientation='left', 
    legend_position='upper left', leaf_font_size=None, title=None, labels=None):
    """
    Plots dendrogram where links are colored based on clusters.

    :param clusters: Cluster id for each data point.
    :param linkage_matrix: Linkage matrix.
    :param dataset_df: Dataset dataframe.
    :param orientation: Dendrogram orrientation
    :param legend_position: Legend position, e.g. 'upper left'
    :param leaf_font_size: Leaf font size.
    :param title: Plot title.
    :param labels: Custom leaf labels.
    :return: Collor pallete used to color each cluster.
    """

    # Get unique clusters
    unique_clusters = np.unique(clusters)
    # Get first two columns of linkage matrix (representing nodes in links)
    trunc_linkage = linkage_matrix[:, :2].astype(np.int32)
    # Get last "original" point ID
    max_orig_point_id = dataset_df.shape[0]

    # Initialize dict that will hold
    # cluster-link relations
    cluster_link_dict = {}

    # Iterate through all the clusters
    for clust in unique_clusters:

        # Get all points belonging to current cluster
        clust_points = np.where(clusters==clust)[0]

        # Perform itteration untill we collect all links associated
        # with current cluster
        while True:

            # Find all positions in linkage matrix where points from
            # cluster are present. This positions in linkage matrix also
            # denote IDs of merged nodes (merged node id = position in linkage mtx + max_orig_point_id)
            points_present = np.isin(trunc_linkage, clust_points)

            # Sum the matrix in order to find positions where
            # both points belong to current cluster
            present_points_sum = np.sum(points_present,axis=1)
            loc_of_twos = np.where(present_points_sum==2)[0]

            # Get link locations
            links_to_add = list(loc_of_twos) 

            # Variable that will be changed to True
            # if new links are added to the dict
            added_new = False

            # Iterate through the link
            for link in links_to_add:

                # Get true ids of the links
                link_aug = link + max_orig_point_id

                # Add new links
                if link_aug not in cluster_link_dict:
                    added_new=True
                    cluster_link_dict[link_aug] = clust

            # If no new links are added this means that all
            # links associated with current cluster are already
            # added.
            # In this case break current loop and proceed to the next cluster.
            if not added_new:
                break

            # Add merged links for next itteration
            new_clust_points = loc_of_twos + max_orig_point_id
            clust_points = np.concatenate([clust_points, new_clust_points])

    # Get collor pallete having one color per cluster
    colors = plt.cm.rainbow(np.linspace(0, 1, len(set(clusters))))
    
    # Transform colors to hex format (dedrogram function requires it)
    colors_hex = [matplotlib.colors.rgb2hex(c) for c in colors]
    color_dict = {key: colors_hex[cluster_link_dict[key]-1] for key in cluster_link_dict}
    link_color_func = lambda x: color_dict[x] if x in color_dict else 'black'
    
    # Prepare legend
    patches = [
        mpatches.Patch(color=colors_hex[i], label=str(unique_clusters[i])) 
        for i in range(len(colors_hex))
    ]
    
    if labels is None:
        labels = dataset_df.index
    
    # Plot the dendrogram
    dendrogram(
        linkage_matrix, 
        link_color_func=link_color_func,
        orientation=orientation, 
        labels=labels,
        leaf_font_size=leaf_font_size
    )
    
    # Plot the legend
    plt.legend(handles=patches, loc=legend_position)
    plt.title(title)
    
    # Show the dendrogram
    plt.show()
    
    return colors_hex


def plot_silouethes_agglomer(
    data_df, clusters, dendr_colors=None, embedding_mtx=None, 
    figsize=(12,5), distance_measure='euclidean'):
    """
    Plot silouethe scores and a given embedding.

    :param data_df: Dataset dataframe.
    :param clusters: Cluster ids.
    :param dendr_colors: Dendrogram colors or other color pallete.
    :param embedding_mtx: Embedding matrix that will be used for plotting the scatterplot.
    :param figsize: Figure size.
    :param distance_measure: Distance measure.
    :return: Overall silhouette score.
    """
    
    y_lower = 10

    # Calculate average silhouette score
    silhouette_scr = silhouette_score(data_df, clusters, metric=distance_measure)
    
    # Calculate silhouette score for each data point
    sample_silhouette_values = silhouette_samples(data_df, clusters, metric=distance_measure)

    # Plot clustering and silouethes
    if embedding_mtx is not None:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    else:
        fig, ax1 = plt.subplots(1, 1, figsize=figsize)

    num_clust = np.unique(clusters).shape[0]

    # Adjust for case when clusters start at 1
    if 0 in clusters:
        adjust_factor = 0
    else:
        adjust_factor = 1

    # Plot siluethe scores for points belonging to each cluster
    for clust_i in range(num_clust):
        
        # Get points bellogning to the current cluster
        ith_cluster_silhouette_values = sample_silhouette_values[
            clusters == clust_i + adjust_factor
        ]
        
        # Sort points by silhouette value
        ith_cluster_silhouette_values.sort()
        
        # Get size of current cluster
        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        
        # Get upper value of y cooridnate for current cluster
        y_upper = y_lower + size_cluster_i
        
        # Fill values between y_lower and y_upper with silhouette score values
        # for data points

        if dendr_colors:
            color = dendr_colors[clust_i]
        else:
            color = cm.nipy_spectral(float(clust_i) / num_clust)

        ax1.fill_betweenx(
            np.arange(y_lower, y_upper),
            0,
            ith_cluster_silhouette_values,
            facecolor=color,
            edgecolor=color,
            alpha=0.7
        )
        
        # Label the silhouette plots with their cluster numbers at the middle
        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(clust_i + adjust_factor))

        # Compute the new y_lower for next plot
        y_lower = y_upper + 10

    # Set title and labels silhouette subplot
    ax1.set_title("The silhouette plot for the various clusters.")
    ax1.set_xlabel("The silhouette coefficient values")
    ax1.set_ylabel("Cluster label")

    # The vertical line for average silhouette score of all the values
    ax1.axvline(x=silhouette_scr, color="red", linestyle="--")

    # Clear the yaxis labels / ticks
    ax1.set_yticks([]) 
    # Set x-ticks
    ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

    # Map cluster labels to cluster colors
    if dendr_colors:
        colors = [dendr_colors[clust_i-adjust_factor] for clust_i in clusters]
    else:
        colors = [cm.nipy_spectral(float(clust_i-adjust_factor) / num_clust) for clust_i in clusters]
    
    if embedding_mtx is not None:

        # 2nd Plot showing the actual clusters formed
        ax2.scatter(
            embedding_mtx[:, 0], 
            embedding_mtx[:, 1],
            marker=".", s=30, lw=0, 
            alpha=0.7, c=colors, 
            edgecolor="k"
        )

        # Set title and labels for scatterplot
        ax2.set_title("The visualization of the clustered data.")
        ax2.set_xlabel("dim1")
        ax2.set_ylabel("dim2")

    # Add main title
    plt.suptitle(
        "Silhouette analysis for KMeans clustering",
        fontsize=14,
        fontweight="bold",
    )

    # Show the plot
    plt.show()
    
    return silhouette_scr