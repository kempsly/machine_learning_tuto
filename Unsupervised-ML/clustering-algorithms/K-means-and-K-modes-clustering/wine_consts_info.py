SOY_FEATURE_DESCRIPTION = {
       'date': 'Represents the specific time of soybean sample collection, crucial for understanding seasonal impacts on plant health.',
       'plant-stand': 'Qualitatively assesses the uniformity and health of the plant population, informing about possible early-stage diseases or growth issues.',
       'precip': 'Captures the water level conditions around the sampling time, providing insights into potential water-related stress factors.',
       'temp': 'Reflects the average climatic temperature at the time of observation, crucial for assessing environmental stress conditions.',
       'hail': 'A binary indicator that identifies whether the plant has undergone hail damage, which could affect overall plant health.',
       'crop-hist': 'Denotes the type of crop previously grown in the same field, essential for understanding soil quality and disease carryover risks.',
       'area-damaged': 'Quantifies the spatial extent of observable damage, useful for gauging the disease\'s progression.',
       'severity': 'Categorizes the observable symptoms into different severity levels, aiding in diagnostic precision.',
       'seed-tmt': 'Indicates whether the seeds underwent any treatment before planting, offering clues to possible resistance against diseases.',
       'germination': 'Measures the proportion of seeds that successfully sprouted, a potential early indicator of crop health.',
       'leaves': 'Evaluates leaf condition, which is often the first site of symptom expression in many plant diseases.',
       'lodging': 'A binary flag that notes whether the plant is upright or has fallen, often indicative of structural weakness or disease.',
       'stem-cankers': 'Details the characteristics of stem cankers if present, essential for identifying specific stem diseases.',
       'canker-lesion': 'Documents the type and appearance of canker lesions on the stem, crucial for diagnostic accuracy.',
       'fruiting-bodies': 'A binary indicator of the presence of fruiting bodies, suggesting advanced stages of certain fungal diseases.',
       'external decay': 'Flags the presence of decay on the plant\'s exterior, indicative of severe fungal or bacterial infection.',
       'mycelium': 'A binary indicator for the presence of fungal mycelium, a sign of fungal diseases.',
       'int-discolor': 'Flags internal discoloration, often indicative of systemic infections.',
       'sclerotia': 'Indicates the presence of sclerotial bodies, commonly associated with advanced fungal diseases.',
       'fruit-pods': 'Evaluates the overall health of the fruit pods, crucial for assessing the final yield quality.',
       'roots': 'Assesses root health, providing insights into soil-borne diseases and nutritional deficiencies.'
}

WINE_FEATURES = {
       'alcohol': 'Measures the alcohol content in wine.\n' + 
              '- Low (<11%): Lighter, potentially less body.\n' + 
              '- Medium (11-14%): Balanced, more body and complexity.\n' + 
              '- High (>14%): Fuller-bodied, may feel "hot" if not balanced.',
                     
       'malic_acid': 'Indicates the acidity level from malic acid.\n' + 
              '- Low (<0.2 g/L): Less tartness, potentially sweeter.\n' + 
              '- High (>0.5 g/L): Tart, "green apple" like acidity.',
                     
       'ash': 'Represents the non-volatile residue in wine.\n' + 
              '- Typical range is 1.5-3.0 g/L; doesn\'t directly influence taste.',
              
       'alcalinity_of_ash': 'Measures the alcalinity of the ash content.\n' + 
              '- Low (<15): Higher acidity, crisp.\n' + 
              '- High (>25): Lower acidity, might taste flat.',
                            
       'magnesium': 'Indicates the magnesium level in wine.\n' + 
              '- Standard range 70-120 ppm; doesn\'t directly affect taste.',
                     
       'total_phenols': 'Represents the total phenolic content.\n' + 
              '- Low (<500 mg/L): Less complex, might age poorly.\n' + 
              '- High (>1500 mg/L): More complexity, better aging potential.',
                     
       'flavanoids': 'Indicates the flavanoid phenolic content.\n' + 
              '- Low (<100 mg/L): Less complexity, poorer aging.\n' + 
              '- High (>500 mg/L): More complexity, better aging potential.',
                     
       'nonflavanoid_phenols': 'Measures the non-flavanoid phenolic content.\n' + 
              '- Low (<20 mg/L): Better aging potential.\n' + 
              '- High (>50 mg/L): Could affect mouthfeel negatively.',
                            
       'proanthocyanins': 'Indicates the proanthocyanin content.\n' + 
              '- Low (<200 mg/L): Lighter color.\n' + 
              '- High (>500 mg/L): Darker color, more aging potential.',
                            
       'color_intensity': 'Measures the color intensity of the wine.\n' + 
              '- Low: Lighter color, often lighter flavor.\n' + 
              '- High: Darker color, often bolder flavor.',
                            
       'hue': 'Indicates the hue, or color tint, of the wine.\n' + 
              '- Lower : Younger or less quality in red wines.\n' + 
              '- High : Older, potentially higher quality especially in red wines.',
              
       'od280/od315_of_diluted_wines': 'Measures the antioxidant content using absorbance ratio.\n' + 
              '- Low (<1.5): Lower antioxidant content.\n' + 
              '- High (>3.0): Higher antioxidant content, might indicate better aging potential.',
                                          
       'proline': 'Indicates the proline level, an amino acid.\n' + 
              '- Low (<500 mg/L): Could indicate less ripe grapes or lower quality.\n' + 
              '- High (>1000 mg/L): Could indicate riper grapes or higher quality.'
}

