#!/usr/bin/env python
# coding: utf-8

# (urban-trees)=
# # Urban Trees

# ![urban_trees.jpg](img/urban_trees.jpg)

# In December 2022 signs were placed beside some trees in my town. They were metal plaques with the name of the corresponding tree species engraved on them, the botanical denomination plus the Basque and Spanish common names.
# 
# When I saw the first sign, I thought that they were not going to last long. They would be vandalised and taken away sooner rather than later. The thought of it saddened me because I have always been fond of urban trees, and now that I had the opportunity of learning about some unknown identities, I was sure this information would vanish soon.
# 
# So I took action and decided to register them myself. I made a couple of forays, during which I scoured the town to find the plaques. It was fun, sort of like playing a *Where's Wally* gymkhana. I wrote the names and the location in a file and made this mini-project. Now I do not worry anymore about the fate of these signs, because the data they contain is safe and sound in the cloud.

# In[34]:


# Import packages
import pandas as pd
import folium

# Read the data
trees = pd.read_csv("data/zuhaitzak.csv")
trees


# In[35]:


# Construct a folium map
urretxu = folium.Map(location=[43.090918759887956, -2.315669883437965], zoom_start=15)

# Create locations and markers
for row in trees.iterrows():
    row_values = row[1]
    location = [row_values["lat"], row_values["lng"]]
    popup = "<b>" + row_values["name"] + "</b>" + "\n"            + "<i>" + row_values["name_eu"] + "</i>" + "\n"            + row_values["name_es"]
    marker = folium.Marker(location=location, popup=popup, tooltip="Click me!")
    marker.add_to(urretxu)
    
# Display the map
urretxu


# In[ ]:




