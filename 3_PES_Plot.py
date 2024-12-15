from shapely import Polygon, MultiPolygon
import geopandas as gpd 
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

# add in the solar energy production in MW per PSE 
Sum_by_PSE = gpd.read_file(r'C:\Users\HP\ProjectsForPortfolio\NationalPVGen\DataFromAPI\TW_by_PSE_2023-2024.csv', headers=False) # bring in data collected from API
Sum_by_PSE['generation_tw'] = pd.to_numeric(Sum_by_PSE['generation_tw']) # convert from obj to intr
Sum_by_PSE_Sorted = Sum_by_PSE.sort_values(by='pes_id')

#define values for color mapping and color bar
min = Sum_by_PSE_Sorted['generation_tw'].min() # min for colorbar 
max = Sum_by_PSE_Sorted['generation_tw'].max() # max for colorbar
norm = mpl.colors.Normalize(vmin=min, vmax=max)
cmap = mpl.cm.inferno 
colors = cmap(norm(Sum_by_PSE_Sorted['generation_tw'])) # convert PES to colours that we use later

# read GEOJSON
unsorted_GJS = gpd.read_file(r'C:\Users\HP\ProjectsForPortfolio\NationalPVGen\Coordinates\gb-dno-license-areas-20240503-as-geojson.geojson')
sorted_GJS = unsorted_GJS.sort_values(by='ID').reset_index(drop=True)

#Plot, fill and label Ploygons
n = 0 # variable to define color and label for polygon 
fig, ax = plt.subplots(figsize=(15, 30), facecolor='white', layout="constrained")  # Create a figure and axes
for PES_Geom in sorted_GJS['geometry']:
    if isinstance(PES_Geom, Polygon):  # Single Polygon
        x, y = PES_Geom.exterior.xy  # Get the exterior coordinates of the polygon
        ax.fill(x, y, alpha=0.5, fc='blue', ec='black')  # Fill with color
    elif isinstance(PES_Geom, MultiPolygon):  # MultiPolygon
        for polygon in PES_Geom.geoms:  # Decompose into individual polygons
            x, y = polygon.exterior.xy
            ax.fill(x, y, alpha=0.5, fc=colors[n], ec='black')  # Fill with color
    centroid = PES_Geom.centroid
    ax.text(centroid.x+3000, centroid.y+7000, f'{sorted_GJS.at[n,'ID']}, {Sum_by_PSE_Sorted.at[n,'generation_tw']}TW', fontsize=8, ha='left', color='black', verticalalignment='bottom', bbox=dict(boxstyle='round,pad=0.3',
                      fc='white', ec='gray', lw=1))
    n+=1

#creation of text for key    
n=0 
key_text = 'KEY (PSE ID and Region)\n'
for x in sorted_GJS['Area']:
    key_text+= str(sorted_GJS.at[n,'ID']) + ': ' + x + ' \n'
    n+=1

#make key
plt.text(.8, .66, f'{key_text}', style='normal',
        bbox={'facecolor': 'whitesmoke', 'alpha': 0.9, 'pad': 10},
        ha='left', va='center', transform=ax.transAxes) 

#creation of text for sources
source_text = '- PES Boundaries from https://www.neso.energy/data-portal/gis-boundaries-gb-dno-license-areas \n- Generation Data from https://www.solar.sheffield.ac.uk/api/ '

#add sources
plt.text(.0, .005, f'{source_text}', style='italic',
        bbox={'facecolor': 'whitesmoke', 'alpha': 0.5, 'pad': 5},
        ha='left', va='bottom', transform=ax.transAxes)

#dates
start_date = pd.to_datetime(Sum_by_PSE_Sorted['start_date']).dt.strftime('%Y-%m')[0]
end_date = pd.to_datetime(Sum_by_PSE_Sorted['end_date']).dt.strftime('%Y-%m')[0]

#define the title
ax.set_title(f'Solar Generation by PES from [{start_date}] to [{end_date}]', fontsize=18, color='black')
ax.axis('scaled')
ax.set_axis_off()

#define the colorbar
cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
             ax=ax, orientation='vertical').set_label(label='Terawatts (TW)',size=12,weight='regular')

# plt.subplots_adjust(left=0.3) 

plt.show()

