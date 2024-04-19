# %%
from subprocess import run
import sys
from pathlib import Path

import cantera as ct
import pandas as pd
import numpy as np
import os
import tqdm

file_csv = 'df_strage_20Pulses_20kHz.csv'
path_csv = os.path.join('input', file_csv)

# %%
gas = ct.Solution('gri30.yaml')

# %% [markdown]
# # ROPの行列を取得する

# %%
species_names = gas.species_names
reaction_names = gas.reaction_equations()

# %% [markdown]
# # 時系列データに対する処理

# %%
os.path.exists(path_csv)
df_csv = pd.read_csv(path_csv, index_col=0, dtype=np.float64)
df_csv.head()

# %%
columns_series = reaction_names.copy()
columns_series.insert(0, 't(sec)')
# print(columns_series)

# %%
df_save = pd.DataFrame(index=columns_series)

print('Obtaining ROP for file: ' + path_csv)

for i, row in tqdm.tqdm(df_csv.iterrows(), total=df_csv.shape[0]):

    time = row['t(sec)']
    T = row['T(K)']
    P = row['P(atm)']
    X = row['H2':].to_numpy()
    
    # set TPX on solution object
    gas.TPX = T, P*ct.one_atm, X
    net_rop = gas.net_rates_of_progress
    series_rop = pd.Series(net_rop, index=reaction_names)

    series_time = pd.Series([time], index=['t(sec)'])
    series_row = pd.concat([series_time, series_rop])

    df_save = pd.concat([df_save, series_row], axis=1)
    
    # break

df_save.head()

# %%
file_export = 'reactions_rop_' + file_csv.split('.csv')[0] + '.csv'
path_export = os.path.join('output', file_export)
df_save.to_csv(path_export)
print('Reactions ROP is exported, file: ', path_export)
