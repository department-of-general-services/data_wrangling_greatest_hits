#!/usr/bin/env python
# coding: utf-8

# # Separate block_lot into block and lot
# Here's a typical problem that can face an analyst working for a Baltimore City agency. Let's say we're interested in analyzing buildings at the block level, but we recieve the data with block and lot combined into just one column. 
# 
# If the block was always the first `n` characters, then it would be easy enough to break the two columns apart in Excel. But the block can be the first three, four, or five characters, depending on various conditions. And the lot can be either the last three or four characters, depending on the conditions. 
# 
# Python turns out to be a great tool for solving this problem, in just a few lines of code. 

# ### Import libraries
# In this case, Pandas is all we need.

# In[1]:


import pandas as pd
from pathlib import Path


# ### Inspect the `block_lot` column
# Consider the output below: 
# 
# - In row 0, the block is the first four digits.
# - In row 1, the block is the first three digits. 
# - In row 2, the block is the first five digits. 
# 
# We'll need to develop logic that accurately captures all of these possibilities.

# In[8]:


buildings_path = Path.cwd() / 'data' / 'buildings.csv'
buildings = pd.read_csv(buildings_path)
buildings[['bl_id', 'block_lot']].head(6)


# ### Define functions
# The two functions below both use the structure of the block-lot data to define a series of "if-then" statements that allow us to accurately break the string down into independent block and lot columns. 

# In[3]:


def get_block_code(blocklot):
    """
    Separates out block data from block and lot 
    
    Args:
        blocklot (str): The original block and lot data from the file

    Returns:
        block (str): The block-level information only 
    """
    if len(blocklot) == 6:         # if the string is only six characters long,
        return blocklot[:3]        # take only the first three chars.
    elif blocklot[4].isalpha():    # but if the fifth char is a letter,
        return blocklot[:5]        # then we take the first five chars.
    else:
        return blocklot[:4]        # otherwise take the first four chars.


def get_lot_code(blocklot):
  if blocklot[-1].isalpha():   # if the last character is a letter,
    return blocklot[-4:]       # take the last four chars.
  else:
    return blocklot[-3:]       # otherwise take the last three.


# In[6]:


buildings['block'] = buildings.apply(lambda x: get_block_code(x['block_lot']), axis=1) 
buildings['lot'] = buildings.apply(lambda x: get_lot_code(x['block_lot']), axis=1) 

buildings[['block_lot', 'block', 'lot']].head()


# In[ ]:


# buildings.drop('Block Lot', inplace=True, axis=1)
# buildings.to_csv('buildings_sep.csv', index=False)

