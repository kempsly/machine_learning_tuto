import numpy as np

from sklearn.metrics import silhouette_samples, silhouette_score, adjusted_rand_score
from hdbscan.validity import validity_index

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.cm as cm


def plot_silouethes_dens(
    data_df, clusters, colors=None, embedding_mtx=None, 
    figsize=(12,5), distance_measure='euclidean'):
    """
    Plot silouethe scores and a given clustering.

    :param data_df: Dataset dataframe.
    :param clusters: Cluster ids.
    :param dendr_colors: Dendrogram colors or other color pallete.
    :param embedding_mtx: Embedding matrix that will be used for plotting the scatterplot.
    :param figsize: Figure size.
    :param distance_measure: Distance measure.
    :param legend_adjust_2: _description_, defaults to 0
    :return: 
    """
    
    if -1 in clusters:
        clusters += 1
        legend_adjust = -1
    else:
        legend_adjust = 0

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


    # Plot siluethe scores for points belonging to each cluster
    for clust_i in range(num_clust):
        
        # Get points bellogning to the current cluster
        ith_cluster_silhouette_values = sample_silhouette_values[
            clusters == clust_i
        ]
        
        # Sort points by silhouette value
        ith_cluster_silhouette_values.sort()
        
        # Get size of current cluster
        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        
        # Get upper value of y cooridnate for current cluster
        y_upper = y_lower + size_cluster_i
        
        # Fill values between y_lower and y_upper with silhouette score values
        # for data points

        if colors:
            color = colors[clust_i]
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
        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(clust_i + legend_adjust))

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
    if colors:
        colors = [colors[clust_i] for clust_i in clusters]
    else:
        colors = [cm.nipy_spectral(float(clust_i) / num_clust) for clust_i in clusters]
    
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


def print_clustering_stats(clusterer, clust_data, data_labels):
    """
    Prints clustering stats for the full dataset and
    for portion of the dataset containing non-noise data points.
    
    Stats are based on metrics such as DBCV, silhouette scores
    and ARI(uses ground truth information).

    :param clusterer: Fitted clustering object (DBSCAN/HDBSCAN)
    :param clust_data: Clustered dataset.
    :param data_labels: True labels.
    """
    
    np_labels = np.array(clusterer.labels_)
    non_noise_idx = np.where(np_labels != -1)

    non_noise_labels = np_labels[non_noise_idx]
    clust_labels_sub = data_labels[non_noise_idx]
    clust_data_sub = clust_data[non_noise_idx]
    noise_size = np_labels.shape[0] - non_noise_labels.shape[0]
    
    print('ARI : {}'.format(adjusted_rand_score(np_labels, data_labels)))
    print('ARI sub : {}'.format(adjusted_rand_score(non_noise_labels, clust_labels_sub)))
    print('noise size : {}'.format(noise_size))
    print('Silouethe : {}'.format(silhouette_score(clust_data, np_labels)))
    print('Silouethe sub : {}'.format(silhouette_score(clust_data_sub, clust_labels_sub)))
    print('DBCV : {}'.format(validity_index(clust_data, np_labels)))