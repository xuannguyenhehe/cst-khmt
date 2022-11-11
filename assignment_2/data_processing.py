import pandas as pd

sheet1 = pd.read_excel('map.xlsx', sheet_name='Sheet1')
sheet2 = pd.read_excel('map.xlsx', sheet_name='Sheet2')

df1 = pd.DataFrame(sheet1)
df1[['Lat', 'Long']] = df1['Long'].str.split(',', 1, expand=True)

df2 = pd.DataFrame(sheet2)


# Join two table 
result = pd.merge(df2, df1, how="left", left_on="Source", right_on="STT")
result = result.drop(columns=['STT'])
result.rename(columns = {'Name':'source_name', 'Long':'source_long', 'Lat':'source_lat'}, inplace = True)
result = pd.merge(result, df1, how="left", left_on="Destination", right_on="STT")
result = result.drop(columns=['STT'])
result.rename(columns = {'Name':'dest_name', 'Long':'dest_long', 'Lat':'dest_lat'}, inplace = True)

from haversine import haversine, Unit
def calulate_distance(df_row):
  dist = haversine((float(df_row['source_lat']), float(df_row['source_long'])), (float(df_row['dest_lat']), float(df_row['dest_long'])))
  return dist

result['distance'] = result.apply(calulate_distance, axis=1)
result.to_excel('input.xlsx')