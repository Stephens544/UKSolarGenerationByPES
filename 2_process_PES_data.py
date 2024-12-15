import os
import pandas as pd
import geopandas as gpd 

print(f'starting to read file... (this could take a couple of minutes depending on data set size)')
# add in the solar energy production in MW per PSE 
df1 = gpd.read_file(r'C:\Users\HP\ProjectsForPortfolio\NationalPVGen\DataFromAPI\PSE_API_2023-2024.csv') # bring in data collected from API
print(f'File has been read, now processing data.')
df1["generation_mw"] = pd.to_numeric(df1["generation_mw"]) # convert from obj to intr
df1["generation_mw"] = df1["generation_mw"].truediv(1000000) # convert from MW to TW 
df1.rename(columns={'generation_mw':'generation_tw'}, inplace=True) # change column name 
Sum_by_PSE = df1.groupby('pes_id')['generation_tw'].sum().reset_index() # sum generation by PES  
Sum_by_PSE['generation_tw'] = Sum_by_PSE['generation_tw'].round(1) # round down TW to 2 decimal places
Sum_by_PSE['start_date'] = df1['datetime_gmt'].min()
Sum_by_PSE['end_date'] = df1['datetime_gmt'].max()

#save file
if not os.path.isfile(r'C:\Users\HP\ProjectsForPortfolio\NationalPVGen\DataFromAPI\TW_by_PSE_2023-2024.csv'):
    Sum_by_PSE.to_csv(r'C:\Users\HP\ProjectsForPortfolio\NationalPVGen\DataFromAPI\TW_by_PSE_2023-2024.csv', header='column_names')
    print(f"CSV with TW by PSE Region created successfully")
