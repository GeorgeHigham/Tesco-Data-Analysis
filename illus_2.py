import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

variable_1 = "f_spirits"
variable_2 = "f_wine"
variable_3 = "f_beer"
variable_4 = "f_soft_drinks"
variable_5 = "f_tea_coffee"
variable_6 = "f_water"

var_list = [variable_1, variable_2, variable_3, variable_4, variable_5, variable_6]

fir_dat = pd.read_csv("Area-level grocery purchases/year_borough_grocery.csv")
var_1_df = pd.DataFrame(index=fir_dat["area_id"])
var_2_df = pd.DataFrame(index=fir_dat["area_id"])
var_3_df = pd.DataFrame(index=fir_dat["area_id"])
var_4_df = pd.DataFrame(index=fir_dat["area_id"])
var_5_df = pd.DataFrame(index=fir_dat["area_id"])
var_6_df = pd.DataFrame(index=fir_dat["area_id"])

folder_name = "Area-level grocery purchases"
for file in os.listdir(folder_name):
    if "borough" in file and "year" not in file:
        df = pd.read_csv(f"{folder_name}/{file}")
        var_1_df[file[:3]] = df[variable_1].values
        var_2_df[file[:3]] = df[variable_2].values
        var_3_df[file[:3]] = df[variable_3].values
        var_4_df[file[:3]] = df[variable_4].values
        var_5_df[file[:3]] = df[variable_5].values
        var_6_df[file[:3]] = df[variable_6].values
    else:
        pass

month_lst = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

var_1_df = var_1_df[month_lst]
var_2_df = var_2_df[month_lst]
var_3_df = var_3_df[month_lst]
var_4_df = var_4_df[month_lst]
var_5_df = var_5_df[month_lst]
var_6_df = var_6_df[month_lst]

plot_df = pd.DataFrame({
    variable_1: var_1_df.mean().values,
    variable_2: var_2_df.mean().values,
    variable_3: var_3_df.mean().values,
    variable_4: var_4_df.mean().values,
    variable_5: var_5_df.mean().values,
    variable_6: var_6_df.mean().values
})

sm_df = pd.DataFrame()

for i in var_list:
    sm_df[i] = plot_df[i].rolling(2).sum()

plot_df.index = month_lst
norm_df=(plot_df-plot_df.min())/(plot_df.max()-plot_df.min())
sm_norm_df = (sm_df-sm_df.min())/(sm_df.max()-sm_df.min())
sm_norm_df.index = month_lst
sm_norm_df = sm_norm_df.set_axis(['Spirits', 'Wine', 'Beer', 'Soft Drinks', 'Tea/Coffee', 'Water'], axis=1)
alcohol_df = sm_norm_df.iloc[:, :3]
non_alcohol_df = sm_norm_df.iloc[:, 3:] 

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 6))
alcohol_df.plot.line(ax=axes[0], lw=3, xticks=range(0,12), figsize=(15,7), color=['teal', 'purple', 'gold'], fontsize=16).legend(loc='center left',bbox_to_anchor=(1.0, 0.5), fontsize=16)
non_alcohol_df.plot.line(ax=axes[1],lw=3, xticks=range(0,12), figsize=(15,7), color=['yellowgreen', 'saddlebrown', 'dodgerblue'], fontsize=16).legend(loc='center left',bbox_to_anchor=(1.0, 0.5), fontsize=16)
plt.subplots_adjust(wspace=0.4)
plt.subplots_adjust(left=0.03, right=0.8, top=0.85, bottom=0.1)

plt.show()
