#!/usr/bin/env python
# coding: utf-8

# # Separate `block_lot` into `block` and `lot`
# Here's a typical problem that can face an analyst working for a Baltimore City agency. Let's say we're interested in analyzing buildings at the block level only, but we recieve the data with block and lot combined into just a single column. 
# 
# If the block was always the first `n` characters, then it would be easy enough to break the two columns apart in traditional spreadsheet software such as Excel. But the block can be the first three, four, or five characters, depending on various conditions. And the lot can be either the last three or four characters, again depending on characteristics of the block-lot value. 
# 
# Python turns out to be a great tool for solving this problem, in just a few lines of code. 

# ### Import libraries
# In this case, Pandas and the pathlib library are all we need.

# In[1]:


import pandas as pd
from pathlib import Path


# ### Inspect the `block_lot` column
# Consider the output below: 
# 
# - In row 0, the block is the first four digits, and the lot is the remainder.
# - In row 1, the block is the first three digits, and the lot is the remainder. 
# - In row 2, the block is the first five digits, and the lot is the remainder. 
# 
# We'll need to develop logic that accurately recognizes all of these possible configurations and accurately separates the block from the lot in each.

# In[11]:


buildings_path = Path.cwd() / 'data' / 'buildings.csv'
buildings = pd.read_csv(buildings_path)
buildings[['bl_id', 'block_lot']].head(6)


# ### Define a function we'll apply to each row
# The function below uses the structure of the block-lot data to define a series of "if-then" statements that allow us to accurately break the string down into independent block and lot columns. 
# 
# Perhaps the trickiest part of this function is that it returns both the block and the lot, stored together in a tuple. Keep that in mind for the next step.

# In[18]:


def split_block_lot(blocklot):
    """
    Separates out block data from block and lot 
    
    Args:
        blocklot (str): The original block and lot data from the file

    Returns:
        [block, lot] (str): A list with the block and lot stored separately as strings
    """
    if len(blocklot) == 6:                  # if the string is only six characters long,
        return [blocklot[:3], blocklot[3:]] # take only the first three chars.
    elif blocklot[4].isalpha():             # but if the fifth char is a letter,
        return [blocklot[:5], blocklot[5:]] # then we take the first five chars.
    else:
        return [blocklot[:4], blocklot[4:]] # otherwise take the first four chars.


# ### Apply the function to each row
# Here we use the `apply()` method of a Pandas dataframe to apply the `split_block_lot()` function to every row of the `buildings` table. This function has a useful paramaeter, `result_type`, which splits list-like data across multiple columns. In this case, that's exactly what we're after, and this parameter allows us to do this action in a single step, instead of assigning the `block` and `lot` in two separate actions. 

# In[20]:


buildings[['block', 'lot']] = buildings.apply(lambda x: split_block_lot(x['block_lot']), 
                                              axis=1, 
                                              result_type='expand') 

buildings[['block_lot', 'block', 'lot']].head(10)

