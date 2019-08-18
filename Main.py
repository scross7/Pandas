#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies and Setup
import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings("ignore")

# File to Load (Remember to Change These)
file_to_load = "Resources/purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
purchase_data = pd.read_csv(file_to_load)


# In[2]:


purchase_data.head()


# In[3]:


# Rename columns to to replace " " with "_"
cols = purchase_data.columns
cols = cols.map(lambda x: x.replace(' ', '_') if isinstance(x, (str)) else x)
purchase_data.columns = cols
purchase_data.head()


# In[4]:


# Display the total number of players
total_players = purchase_data.SN.nunique()
total_players_dict = [{"Total Players" : total_players}]
total_players = pd.DataFrame(total_players_dict)
total_players


# In[5]:


### Purchasing Analysis (Total) ###

# Run basic calculations to obtain number of unique items, average price, number of purchases and total revenue
unique_items = purchase_data.Item_ID.nunique()

# Format price columns
pd.options.display.float_format = "${:,.2f}".format
avg_price = purchase_data.Price.mean()

total_purchases = purchase_data.Purchase_ID.count()

total_revenue = purchase_data.Price.sum()

basic_calc_dict = [{"Number of Unique Items" : unique_items, 
                   "Average Price" : avg_price, 
                   "Number of Purchases" : total_purchases, 
                   "Total Revenue" : total_revenue}]

basic_calc = pd.DataFrame(basic_calc_dict)

basic_calc


# In[6]:


### Gender Demographics ###

# Filter data by SN for unique entires
unique_SN = purchase_data.drop_duplicates('SN')

unique_gender = unique_SN.Gender.value_counts()
unique_gender = pd.DataFrame(unique_gender)

total_gender = unique_SN.Gender.count()
unique_gender

# Percentage and Count of Male, Female and  Players
pd.options.display.float_format = "{:,.2f}".format
gender_percent = (unique_gender/total_gender)*100
unique_gender["Percentage of Players"] = gender_percent
unique_gender.rename(columns = {'Gender':'Total Count'}, inplace = True)

unique_gender


# In[7]:


### Purchasing Analysis (Gender) ###

# purchase count
gender_count = purchase_data.Gender.value_counts()
gender_count = pd.DataFrame(gender_count)
gender_count.sort_index()
gender_count.index.name = "Gender"
gender_count.rename(columns = {'Gender':'Purchase Count'}, inplace = True)

# total purchase price
total_purch = purchase_data.groupby(['Gender'])['Price'].sum()
gender_count['Total Purchase Value'] = pd.Series(total_purch)

# avg. purchase price
avg_purch_price = gender_count['Total Purchase Value']/gender_count['Purchase Count']
gender_count['Average Purchase Price'] = pd.Series(avg_purch_price)

# avg. total purchase per person = sum(female purchases) / sum(unique females)
avg_total_pp = gender_count['Total Purchase Value']/unique_gender['Total Count']
gender_count['Avg Total Purchase per Person'] = pd.Series(avg_total_pp)
gender_count

# re-order columns
gender_count = gender_count[['Purchase Count', 'Average Purchase Price', 
                             'Total Purchase Value', 'Avg Total Purchase per Person']]

# set column formatting
format_mapping = {'Purchase Count': '{:,.0f}', 'Average Purchase Price': '${:,.2f}', 
                'Total Purchase Value': '${:,.2f}', 'Avg Total Purchase per Person': '${:,.2f}'}

for key, value in format_mapping.items():
    gender_count[key] = gender_count[key].apply(value.format)
    
# sort index
gender_count = gender_count.sort_index()
    
gender_count


# In[8]:


### Age Demographics ###

# Filter data by SN for unique entires
age_unique_SN = purchase_data.drop_duplicates('SN')

# Establish bins for ages
bins = [0, 9, 14, 19, 24, 29, 34, 39, 200]
group_names = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]
age_unique_SN["Total Count"] = pd.cut(age_unique_SN["Age"], bins, labels=group_names)

# Create new dataframe
age_demo = age_unique_SN["Total Count"].value_counts()
age_demo = pd.DataFrame(age_demo)

age_demo = age_demo.sort_index()

# Find percentages
age_demo_sum = age_demo["Total Count"].sum()

age_demo_perc = (age_demo["Total Count"]/age_demo_sum)*100
age_demo['Percentage of Players'] = pd.Series(age_demo_perc)

age_demo


# In[9]:


### Purchasing Analysis (Age) ###

# Create new dataframe
purch = pd.DataFrame(purchase_data)

# Add column with bins
bins = [0, 9, 14, 19, 24, 29, 34, 39, 200]
group_names = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]
purch["Age Bins"] = pd.cut(purch["Age"], bins, labels=group_names)

# Count bins and set index as age bins, rename first column
age_bin_count = purch["Age Bins"].value_counts()
age_bin_count = pd.DataFrame(age_bin_count)
age_bin_count.sort_index()
age_bin_count.rename(columns = {'Age Bins':'Purchase Count'}, inplace = True)

# Total Purchase Value
total_purch = purch.groupby(['Age Bins'])['Price'].sum()
age_bin_count['Total Purchase Value'] = pd.Series(total_purch)

# Avg. Purchase Price
avg_purch_price = age_bin_count['Total Purchase Value']/age_bin_count['Purchase Count']
age_bin_count['Average Purchase Price'] = pd.Series(avg_purch_price)

# avg. total purchase per person = sum(female purchases) / sum(unique females)
avg_total_pp = age_bin_count['Total Purchase Value']/age_demo['Total Count']
age_bin_count['Avg Total Purchase per Person'] = pd.Series(avg_total_pp)

# re-order columns
age_bin_count = age_bin_count[['Purchase Count', 'Average Purchase Price', 
                             'Total Purchase Value', 'Avg Total Purchase per Person']]

# set column formatting
format_mapping = {'Purchase Count': '{:,.0f}', 'Average Purchase Price': '${:,.2f}', 
                'Total Purchase Value': '${:,.2f}', 'Avg Total Purchase per Person': '${:,.2f}'}

for key, value in format_mapping.items():
    age_bin_count[key] = age_bin_count[key].apply(value.format)
    
# sort index
age_bin_count = age_bin_count.sort_index()
    
age_bin_count


# In[10]:


### Top Spenders ###

# Create dataframe with SN index and summing on price to get total value
top_spend = purchase_data.groupby(['SN'])['Price'].sum()
top_spend = pd.DataFrame(top_spend)
top_spend.rename(columns = {'Price':'Total Purchase Value'}, inplace = True)

# Value counts on SN to get purchase count
purch_count = purchase_data.SN.value_counts()
top_spend['Purchase Count'] = pd.Series(purch_count)
top_spend['Average Purchase Price'] = top_spend['Total Purchase Value'] / top_spend['Purchase Count']

# Re-order columns formatting and sort
top_spend = top_spend[['Purchase Count', 'Average Purchase Price', 'Total Purchase Value']]

top_spend = top_spend.sort_values(by=['Total Purchase Value'], ascending=False)

format_mapping = {'Purchase Count': '{:,.0f}', 'Average Purchase Price': '${:,.2f}', 
                'Total Purchase Value': '${:,.2f}'}

for key, value in format_mapping.items():
    top_spend[key] = top_spend[key].apply(value.format)

top_spend.head(5)


# In[11]:


purchase_data.head()


# In[12]:


### Most Popular Items ###

# Find the unique values for item id, name and price
popular = purchase_data.drop_duplicates(['Item_ID','Item_Name'])
popular = popular[['Item_ID','Item_Name','Price']]
popular.rename(columns = {'Price':'Item Price'}, inplace = True)
popular

# Find the number of each item that was purcahsed
item_count = purchase_data.Item_ID.value_counts()
item_count = pd.DataFrame(item_count)
item_count = item_count.reset_index()
item_count.rename(columns = {'index':'Item_ID', 'Item_ID':'Purchase Count'}, inplace = True)
item_count

# Merge the two dataframes together, matching on item id
merge = pd.merge(popular, item_count, on="Item_ID")
merge.rename(columns = {'Item_ID': 'Item ID', 'Item_Name':'Item Name'}, inplace = True)

merge['Total Purchase Value'] = merge['Item Price'] * merge['Purchase Count']

# Re-order columns and formatting, set new index and sort columns
merge = merge[['Item ID','Item Name','Purchase Count', 'Item Price', 'Total Purchase Value']]

merge = merge.sort_values(by=['Purchase Count'], ascending=False)

purch_merge = merge.set_index(['Item ID','Item Name'])

format_mapping = {'Purchase Count': '{:,.0f}', 'Item Price': '${:,.2f}', 
                'Total Purchase Value': '${:,.2f}'}

for key, value in format_mapping.items():
    purch_merge[key] = purch_merge[key].apply(value.format)

purch_merge.head()


# In[13]:


### Most Profitable Items ###

# Sort by total purchase value in descending order
merge = merge.sort_values(by=['Total Purchase Value'], ascending=False)

# Set new index and formatting
total_merge = merge.set_index(['Item ID','Item Name'])

format_mapping = {'Purchase Count': '{:,.0f}', 'Item Price': '${:,.2f}', 
                'Total Purchase Value': '${:,.2f}'}

for key, value in format_mapping.items():
    total_merge[key] = total_merge[key].apply(value.format)

total_merge.head()


# Include a written description of three observable trends based on the data.
# 
# 1. 3/5 of the most "profitable" items are also the most popular items. Although, profitability is not necessarily linked to the higher prices items as they may be more expensive to ship, produce, store, etc.
# 
# 2. If the company were looking for an age group to market to, it appears the male, 20-24 age group would be the best fit as they spend more money, purchase the most items and make up the largest percentage of players.
# 
# 3. Average Purchase Price and Average Purchase per Person seems to be consistent across age demographics.
# 
# 4. Further analysis could be done to reduce the number of items sold and maintain profitability. 183 items is a large inventory and many of these items only sold one item. Analysis could show if there is a correlation between repeat customers and larger overall purchases for the more rarely purchased items.
