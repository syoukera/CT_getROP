# %%
from subprocess import run
import sys
from pathlib import Path

import cantera as ct
import pandas as pd
import numpy as np
import os
import tqdm

# %% [markdown]
# # ROPの行列を取得する

# %%
gas = ct.Solution('gri30.yaml')
species_names = gas.species_names
# print(species_names)

# %%
reaction_names = gas.reaction_equations()
# print(reaction_names)

# %%
stoich_coeffs = gas.product_stoich_coeffs - gas.reactant_stoich_coeffs
stoich_coeffs

# %%
df_stoich = pd.DataFrame(stoich_coeffs, columns=reaction_names, index=species_names)
df_stoich.head()

# %%
species_target = 'O'
df_stoich_target = df_stoich.loc[species_target, :]
df_stoich_target.head()

# %% [markdown]
# # ropのデータを読み込む

# %%
file_csv = 'df_strage_20Pulses_20kHz.csv'
path_csv = os.path.join('input', file_csv)

file_rop = 'reactions_rop_' + file_csv.split('.csv')[0] + '.csv'
path_export = os.path.join('output', file_rop)

# %%
print(os.path.exists(path_export), path_export)
df_rop = pd.read_csv(path_export, index_col=0).T
df_rop.head()

# %%
df_rop_target = df_rop.iloc[:, 1:]*df_stoich_target
df_rop_target = pd.concat((df_rop['t(sec)'], df_rop_target), axis=1)
df_rop_target.head()

# %%
file_base = file_csv.split('.csv')[0]
file_export = f'species_rop_{species_target}_{file_base}.csv'
path_export = os.path.join('output', file_export)
df_rop_target.to_csv(path_export)
print('Species ROP is exported to file: ', path_export)


