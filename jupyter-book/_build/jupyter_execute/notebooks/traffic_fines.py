#!/usr/bin/env python
# coding: utf-8

# (traffic-fines)=
# # Traffic Fines

# ![img/traffic_fines.jpg](img/traffic_fines.jpg)

# Jan, 2023

# ## Background
# To make a data project, first you need data. One possibility is to collect it yourself, making it a *quantifying* project for a start. Another alternative is to directly ask for the data to the people who have it. And then, there is sometimes the option of downloading it from the internet as [open data](https://en.wikipedia.org/wiki/Open_data), which is what I did for this project.
# 
# I was curious about what the local government was publishing as open data. The datasets I found were not particularly exciting, much of it was about municipal finances and some demographics. But I came across the information of traffic fines during the last few years, and I thought I would give it a try.
# 
# With open data, institutions aim to become more transparent to the public. The data is shared, it is available for anyone to take a look at it, but usually it is not that simple. You need a data project to make sense of it. Once you convert the numbers into graphics and insightful information, only then the data comes alive and you can figure out what is going on.

# ## The data
# I downloaded the CSV files from this link, containing traffic fines in my town from 2018 to 2022.
# 
# [https://www.gipuzkoairekia.eus/](https://www.gipuzkoairekia.eus/es/datu-irekien-katalogoa/-/openDataSearcher/detail/detailView/b4db402e-6fd6-48f9-bd0a-a137902a3f1a)

# In[66]:


# Import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import contextily
from IPython.display import Markdown

# Read the data
usecols=[0, 4, 5, 6, 7, 8] # Useful columns
fines_2018 = pd.read_csv("data/multas_2018.csv", sep=";", decimal=",", usecols=usecols)
fines_2019 = pd.read_csv("data/multas_2019.csv", sep=";", decimal=",", usecols=usecols)
fines_2020 = pd.read_csv("data/multas_2020.csv", sep=";", decimal=",", usecols=usecols)
fines_2021 = pd.read_csv("data/multas_2021.csv", sep=";", decimal=",", usecols=usecols)
fines_2022 = pd.read_csv("data/multas_2022.csv", sep=";", decimal=",", usecols=usecols)

# Concatenate the data from different years into a unique dataset
fines = pd.concat([fines_2018, fines_2019, fines_2020, fines_2021, fines_2022])

# Rename columns
fines = fines.rename(columns={"AÑO": "year",
                              "NOMBRE CALLE": "street",
                              "CALIFICACION": "category",
                              "NRO MULTAS": "fines",
                              "IMPORTE PAGADO": "paid",
                              "IMPORTE PENDIENTE DE PAGO EN EJECUTIVA": "unpaid"})
print(fines)


# As shown in the dataframe above, the number of fines related to the year and street is already aggregated into three different categories:
# - LEVE, for mild traffic offences.
# - GRAVE, for serious ones.
# - MUY GRAVE, for very serious ones.

# ## Data validation
# Data inspection shows some missing values.

# In[67]:


# Dataframe inspection
fines.info()


# Only 3 rows out of 340 have missing values, and with few fine quantities, so I just drop them.

# In[68]:


# Rows with NaN values
print(fines[fines["street"].isna()])


# In[69]:


# Discard rows with NaN values
fines = fines[~fines["street"].isna()]


# In[70]:


# Check dataframe
fines.info()


# As data types are already correct, no further measures are needed.

# ## Exploratory Data Analysis

# ### Fines by street
# QUESTION: Which are the streets with the greater number of fines? Locate the hotspots.

# In[71]:


# Group by streets and fine category, then sum up fines
fines_streets = fines.groupby(["street", "category"])["fines"].sum().unstack()

# Rearrange column order: LEVE, GRAVE, MUY GRAVE
fines_streets = fines_streets.iloc[:, [1, 0, 2]]

# Create new column with the total amount of fines: LEVE + GRAVE + MUY GRAVE
fines_streets["total"] = fines_streets.sum(axis=1)

# Sort values by total amount of fines
fines_streets = fines_streets.sort_values("total", ascending=False)

print(fines_streets)


# In[72]:


# Define color palette
palette = ["tab:blue", "tab:orange", "tab:red"]

# Plot
fig, ax = plt.subplots(figsize=(8, 12))

fines_streets.sort_values("total").drop("total", axis=1).plot(ax=ax, kind="barh",
                                                              stacked=True, color=palette)

ax.grid(axis="x")
ax.set_axisbelow(True)
ax.set_title("Number of fines 2018-2022", size=11)
ax.set_xlabel("# of fines", fontsize=11)
ax.set_ylabel("")
ax.legend(fontsize=11, loc='center')
sns.despine()

plt.show()


# I decided to put this information into a choropleth. That for, I first needed to form a map with the streets and neighborhoods of the town. I draw each polygon by hand using https://geojson.io/.

# In[73]:


# Read geographical data of streets into a geopandas dataframe
zelai = gpd.read_file("geojson/zelai_arizti_parkea.geojson")
zelai["street"] = "ZELAI-ARIZTI PARKEA"
sekundino = gpd.read_file("geojson/sekundino_esnaola_kalea.geojson")
sekundino["street"] = "SEKUNDINO ESNAOLA KALEA"
ospitalea = gpd.read_file("geojson/eskualdeko_ospitalea.geojson")
ospitalea["street"] = "ESKUALDEKO OSPITALEA"
geltokien = gpd.read_file("geojson/geltokien_enparantza.geojson")
geltokien["street"] = "GELTOKIEN ENPARANTZA"
piedad = gpd.read_file("geojson/piedad_kalea.geojson")
piedad["street"] = "PIEDAD KALEA"
bidezar = gpd.read_file("geojson/bidezar_kalea.geojson")
bidezar["street"] = "BIDEZAR KALEA"
kalebarren = gpd.read_file("geojson/kalebarren.geojson")
kalebarren["street"] = "KALEBARREN"
elizkale = gpd.read_file("geojson/elizkale.geojson")
elizkale["street"] = "ELIZKALE"
gregorio = gpd.read_file("geojson/san_gregorio_kalea.geojson")
gregorio["street"] = "SAN GREGORIO KALEA"
legazpi = gpd.read_file("geojson/legazpi_kalea.geojson")
legazpi["street"] = "LEGAZPI KALEA"
elkano = gpd.read_file("geojson/elkano_kalea.geojson")
elkano["street"] = "ELKANO KALEA"
euskadi = gpd.read_file("geojson/euskadi_enparantza.geojson")
euskadi["street"] = "EUSKADI ENPARANTZA"
urdaneta = gpd.read_file("geojson/urdaneta_hiribidea.geojson")
urdaneta["street"] = "URDANETA HIRIBIDEA"
jai = gpd.read_file("geojson/jai_alai_kalea.geojson")
jai["street"] = "JAI-ALAI KALEA"
orbegozo = gpd.read_file("geojson/esteban_orbegozo_ibilaldia.geojson")
orbegozo["street"] = "ESTEBAN ORBEGOZO IBILALDIA"
leturia = gpd.read_file("geojson/leturiatarren_enparantza.geojson")
leturia["street"] = "LETURIATARREN ENPARANTZA"
iparragirre = gpd.read_file("geojson/iparragirre_hiribidea.geojson")
iparragirre["street"] = "IPARRAGIRRE HIRIBIDEA"
soraluze = gpd.read_file("geojson/soraluze_kalea.geojson")
soraluze["street"] = "SORALUZE KALEA"
okendo = gpd.read_file("geojson/okendo_kalea.geojson")
okendo["street"] = "OKENDO KALEA"
txurruka = gpd.read_file("geojson/txurruka_kalea.geojson")
txurruka["street"] = "TXURRUKA KALEA"
ibaiondo = gpd.read_file("geojson/ibaiondo.geojson")
ibaiondo["street"] = "IBAIONDO"
artiz = gpd.read_file("geojson/artiz_auzoa.geojson")
artiz["street"] = "ARTIZ AUZOA"
euskalerria = gpd.read_file("geojson/euskalerria_hiribidea.geojson")
euskalerria["street"] = "EUSKALERRIA HIRIBIDEA"
oraa = gpd.read_file("geojson/antonino_oraa_kalea.geojson")
oraa["street"] = "ANTONINO ORAA KALEA"
urola = gpd.read_file("geojson/urola_kalea.geojson")
urola["street"] = "UROLA KALEA"
beloki = gpd.read_file("geojson/beloki_hiribidea.geojson")
beloki["street"] = "BELOKI HIRIBIDEA"
loiola = gpd.read_file("geojson/inigo_de_loiola_kalea.geojson")
loiola["street"] = "IÑIGO DE LOIOLA KALEA"
busca = gpd.read_file("geojson/busca_sagastizabal_parkea.geojson")
busca["street"] = "BUSCA SAGASTIZABAL PARKEA"
etxeberri = gpd.read_file("geojson/etxeberri_auzoa.geojson")
etxeberri["street"] = "ETXEBERRI AUZOA"
filipinas = gpd.read_file("geojson/islas_filipinas_kalea.geojson")
filipinas["street"] = "ISLAS FILIPINAS KALEA"
antio = gpd.read_file("geojson/antio.geojson")
antio["street"] = "ANTIO"
ipar = gpd.read_file("geojson/ipar_haizea_auzoa.geojson")
ipar["street"] = "IPAR HAIZEA AUZOA"
izazpi = gpd.read_file("geojson/izazpi_auzoa.geojson")
izazpi["street"] = "IZAZPI AUZOA"
antzine = gpd.read_file("geojson/antzine_hiribidea.geojson")
antzine["street"] = "ANTZIÑE HIRIBIDEA"
legazpi_auzo = gpd.read_file("geojson/legazpi_auzunea.geojson")
legazpi_auzo["street"] = "LEGAZPI AUZUNEA"
isidro = gpd.read_file("geojson/san_isidro_kalea.geojson")
isidro["street"] = "SAN ISIDRO KALEA"
nafarroa = gpd.read_file("geojson/nafarroa_enparantza.geojson")
nafarroa["street"] = "NAFARROA ENPARANTZA"
barandi = gpd.read_file("geojson/joxe_miel_barandiaran_auzunea.geojson")
barandi["street"] = "JOXE MIEL BARANDIARAN AUZUNEA"
urtubi = gpd.read_file("geojson/urtubi_auzoa.geojson")
urtubi["street"] = "URTUBI AUZOA"
lorategia = gpd.read_file("geojson/hiri_lorategia.geojson")
lorategia["street"] = "HIRI LORATEGIA"
elgarrestamendi = gpd.read_file("geojson/elgarrestamendi_kalea.geojson")
elgarrestamendi["street"] = "ELGARRESTAMENDI KALEA"
argixao = gpd.read_file("geojson/argixao_auzoa.geojson")
argixao["street"] = "ARGIXAO AUZOA"
industrialdea = gpd.read_file("geojson/zumarragako_industrialdea.geojson")
industrialdea["street"] = "ZUMARRAGAKO INDUSTRIALDEA"
eitza = gpd.read_file("geojson/eitza_berri.geojson")
eitza["street"] = "EITZA BERRI"
jaka = gpd.read_file("geojson/anjel_cruz_jaka_auzunea.geojson")
jaka["street"] = "ANGEL CRUZ JAKA AUZUNEA"

# Concatenate all dataframes into a unique one
zumarraga = pd.concat([zelai, sekundino, ospitalea, geltokien, piedad, bidezar,
                       kalebarren, elizkale, gregorio, legazpi, elkano, euskadi,
                       urdaneta, jai, orbegozo, leturia, iparragirre, soraluze,
                       okendo, txurruka, ibaiondo, artiz, euskalerria, oraa,
                       urola, beloki, loiola, busca, filipinas, antio, ipar,
                       izazpi, antzine, legazpi_auzo, isidro, nafarroa, barandi,
                       urtubi, lorategia, elgarrestamendi, argixao,
                       industrialdea, eitza, jaka,
                       # etxeberri,
                      ])

# Create a projected reference system to plot with a basemap
zumarraga_3857 = zumarraga.copy()
zumarraga_3857.geometry = zumarraga_3857.geometry.to_crs(epsg=3857)

# Plot with a basemap
fig, ax = plt.subplots()
legend_kwds = {'title': 'Streets & neighbourhoods', 'fontsize': 8,
               'loc': 'upper left', 'bbox_to_anchor': (1, 1.03), 'ncol': 2}
zumarraga_3857.plot(ax=ax, column="street", legend=True, legend_kwds=legend_kwds)
contextily.add_basemap(ax,
                       source=contextily.providers.OpenStreetMap.Mapnik,
                       # source=contextily.providers.CartoDB.PositronNoLabels,
                      )
ax.set_axis_off()

plt.show()


# Having made the map, it was all about merging it with the fines dataframe to get the couple of choropleths shown below.

# In[74]:


# Merge geographical dataframe with fine by streets dataframe
zumarraga_fines = zumarraga.merge(fines_streets, how="left",
                                  left_on="street", right_on=fines_streets.index)

# Plot a choropleth by total number of fines
fig, ax = plt.subplots()
zumarraga_fines.plot(ax=ax, column="total", legend=True, cmap="Greys",
                    legend_kwds={'label': "# of fines", "shrink": 0.7})
ax.set_title("Neighborhoods by TOTAL number of fines", size=11)
ax.set_axis_off()
plt.show()


# In[75]:


# Plot a choropleth by total number of serious (GRAVE) fines
fig, ax = plt.subplots()
zumarraga_fines.plot(ax=ax, column="GRAVE", legend=True, cmap="Oranges",
                    legend_kwds={'label': "# of fines", "shrink": 0.7})
ax.set_title("Neighborhoods by serious 'GRAVE' number of fines", size=11)
ax.set_axis_off()
plt.show()


# ### Fines by year
# QUESTION: How have the number of fines evolved during the last few years?

# In[76]:


# Group by year and fine category, then sum up fines
fines_years = fines.groupby(["year", "category"])["fines"].sum().unstack()

# Rearrange column order: LEVE, GRAVE, MUY GRAVE
fines_years = fines_years.iloc[:, [1, 0, 2]]

# Create new column with the total amount of fines: LEVE + GRAVE + MUY GRAVE
fines_years["total"] = fines_years.sum(axis=1)

print(fines_years)


# In[77]:


# Plot
fig, ax = plt.subplots(figsize=(6, 4))

fines_years.drop(["total"], axis=1).plot(ax=ax, kind="bar",
                                         stacked=True, color=palette)

ax.grid(axis="y")
ax.set_axisbelow(True)
ax.tick_params(axis='x', labelsize=12, rotation=0)
ax.tick_params(axis='y', labelsize=12)
ax.set_title("Number of fines", fontsize=12)
ax.set_xlabel("", fontsize=12)
ax.set_ylabel("# of fines", fontsize=12)
ax.legend(bbox_to_anchor=(1.0, 0.5), loc='center left', fontsize=10)
sns.despine()

plt.show()


# ### Fines by year and street
# QUESTION: How have the number of fines evolved during the last years in the top 10 fine-prone streets?

# In[78]:


# Group by year, street and fine category, then sum up fines
fines_years_streets = fines.groupby(["year", "street", "category"])["fines"].sum().unstack()

# Rearrange column order: LEVE, GRAVE, MUY GRAVE
fines_years_streets = fines_years_streets.iloc[:, [1, 0, 2]]

# Create new column with the total amount of fines
fines_years_streets["total"] = fines_years_streets.sum(axis=1)

print(fines_years_streets)


# In[79]:


# Create a list with the names of the top 10 fine streets
fines_streets_top10 = fines_streets.iloc[:10].index

# Filter top 10 streets
fines_years_streets = fines_years_streets.reset_index()
fines_years_streets_top10 = fines_years_streets[fines_years_streets["street"]                                                .isin(fines_streets_top10)]

# Plot
fig, ax = plt.subplots(figsize=(7.5, 5))

sns.pointplot(ax=ax, x="year", y="total", data=fines_years_streets_top10,
              hue="street")

ax.grid(axis="y")
ax.set_axisbelow(True)
ax.tick_params(axis='x', labelsize=14, rotation=0)
ax.tick_params(axis='y', labelsize=14)
ax.set_title("Evolution of fines in top 10 fine-prone streets", fontsize=14)
ax.set_xlabel("", fontsize=13)
ax.set_ylabel("# of fines", fontsize=14)
ax.legend(bbox_to_anchor=(1.0, 0.5), loc='center left', fontsize=12)
sns.despine()

plt.show()


# ### Money collected from fines
# QUESTION: How much money does the municipality collect from fines?
# 
# The data comes with two columns related to the amount of money:
# - "IMPORTE PAGADO": which I have renamed as "paid".
# - "IMPORTE PENDIENTE DE PAGO EN EJECUTIVA": which I have renamed as "unpaid".
# 
# For the sake of clarity, I have added together both columns (I have supposed pending payments will eventually be processed).

# In[80]:


# Create new column with the total amount
fines["paid_unpaid"] = fines["paid"] + fines["unpaid"]

# Group by year and fine category, then sum up fines
fines_money = fines.groupby(["year", "category"])["paid_unpaid"].sum().unstack()

# Rearrange column order: LEVE, GRAVE, MUY GRAVE
fines_money = fines_money.iloc[:, [1, 0, 2]]

# Create new column with the total amount of money raised
fines_money["total"] = fines_money.sum(axis=1)

print(fines_money)


# In[81]:


# Plot
fig, ax = plt.subplots(figsize=(6, 4))

fines_money.drop(["total"], axis=1).plot(ax=ax, kind="bar",
                                         stacked=True, color=palette)

ax.grid(axis="y")
ax.set_axisbelow(True)
ax.tick_params(axis='x', labelsize=12, rotation=0)
ax.tick_params(axis='y', labelsize=12)
ax.set_title("Revenue from fines", fontsize=12)
ax.set_xlabel("", fontsize=12)
ax.set_ylabel("euros (€)", fontsize=12)
ax.legend(bbox_to_anchor=(1.0, 0.5), loc='center left', fontsize=10)
sns.despine()

plt.show()


# Finally, I find it interesting to summarise this graphic into one single figure: how much money do they collect roughly per year?

# In[82]:


# How much money do they collect on average per year?
avg_year = fines_money["total"].mean()

# The same value roughly
avg_year_rough = round(avg_year, -3)

display(Markdown(f"The amount of money collected per year is roughly **{avg_year_rough:.0f} €**"))


# ## Conclusions
# This project was about shedding light on a freely available open data set. In this case, I downloaded the files of traffic fines in my town. The analysis consisted in exploring ways of representing the data to get a clear picture of its contents. This kind of work should be useful for the people involved, to watch out for trends and follow up new policies. And for the public, to effectively make the information transparent for all of us.
