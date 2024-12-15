# UKSolarGenerationByPES
Pull UK solar generation data via API and represent with heatmap
First, run 1_PES_PVGenAPI.py to draw data from the API for each PES region. Adjust date ranges if desired
Then run 2_process_PES_data.py to process data (i.e. convert to integer, convert from MW to GW, and group by PES area)
Finally, run 3_PES_Plot.py to output the heatmap
