import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("artwork_data.csv")
s = df["artist"] == "Bacon, Francis"
s.value_counts()


df.loc[:,'width']= pd.to_numeric(df['width'],errors ='coerce')
df.loc[:,'height']= pd.to_numeric(df["height"], errors ="coerce")
area = df["height"]*df["width"]
df = df.assign(area = area)
#creating small data frame
small_df = df.iloc[49980:50019, :].copy()
grouped = small_df.groupby("artist")
for name, group_df in grouped:
    print(name, group_df)
    break


# transform
def fill_values(series):
    values_counted = series.value_counts()
    if values_counted.empty:
        return series
    most_frequent = values_counted.index[0]
    new_medium = series.fillna(most_frequent)
    return new_medium


def transform_df(source_df):
    group_dfs = []
    for name, group_df in source_df.groupby("artist"):
        filled_df = group_df.copy()
        filled_df.loc[:, "medium"] = fill_values(group_df["medium"])
        group_dfs.append(filled_df)

    new_df = pd.concat(group_dfs)
    return new_df

filled_df = transform_df(small_df)
grouped_medium = df.groupby("artist")["medium"]
df.loc[:,"medium"]= grouped_medium.transform(fill_values)

#min
grouped_acq_year =df.groupby("artist")['acquisitionYear']
min_acquisition_year = grouped_acq_year.agg(np.min)

#Filter
groupde_titles = df.groupby('title')
condition = lambda x: len(x.index)>1
filtered_df = groupde_titles.filter (condition)

#Basic Excel
small_df.to_excel("cols.xlsx", columns = ["artist","title","year"])

#Multiple worksheets
writer = pd.ExcelWriter("multiple_sheets.xlsx", engine = "xlsxwriter")
small_df.to_excel(writer,sheet_name = "preview", index = False)
df.to_excel (writer, sheet_name = "Complete", index = False)
writer.save()

#Conditional Formating
artist_counts = df["artist"].value_counts()
artist_counts.head()
writer = pd.ExcelWriter("colors.xlsx", engine = 'xlsxwriter')
artist_counts.to_excel(writer, sheet_name ="Artist Counts")
sheet = writer.sheets['Artist Counts']
cells_range = 'B2:B{}'.format(len(artist_counts.index))
sheet.conditional_format(cells_range, {"type": "2_color_scale",
                                       "min_value":"10",
                                       "min_type":"percentile",
                                       "max_value":"99",
                                       "max_type":"percentile"})
writer.save()

acquisition_years = df.groupby("acquisitionYear").size()

#Set Fonts
title_font = {"family": "source san pro",
             "color": "darkblue",
             "weight": "normal",
             "size":20,
             }
labels_font = {"family":"consolas",
              "color": "darkred",
              "weight": "normal",
              "size":10,
              }
#plotting
#Add log scale
#Add grid
fig = plt.figure()
subplot = fig.add_subplot(1,1,1)
acquisition_years.plot(ax = subplot, rot= 45, logy = True, grid = True)
subplot.set_xlabel("Acquisition Year")
subplot.set_ylabel("Artworks Acquired")
subplot.locator_params(nbins = 40, axis = "x")
fig.show()
