import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
import dataframe_image as dfi
import matplotlib.ticker as ticker


inc_dat = pd.read_csv("london_income_borough.csv")
gro_dat = pd.read_csv("Area-level grocery purchases/year_borough_grocery.csv")
gr_dat = gro_dat.loc[:, gro_dat.columns != 'area_id']
norm_dat = (gr_dat-gr_dat.min())/(gr_dat.max()-gr_dat.min())
norm_dat['area_id'] = gro_dat['area_id']
merged_dat = norm_dat.set_index("area_id").join(inc_dat.set_index("Code"))

y_1 = 'alcohol'
y_2 = 'h_nutrients_calories_norm'
y_3 = 'energy_tot'
y_4 = 'f_energy_fibre'

y_axis_scatter_1 = merged_dat[y_1]
y_axis_scatter_2 = merged_dat[y_2]
y_axis_scatter_3 = merged_dat[y_3]
y_axis_scatter_4 = merged_dat[y_4]
x_axis_scatter = merged_dat['Mean £']

# dropping outlier from data
y_axis_scatter_1 = y_axis_scatter_1.drop('E09000033', axis=0)
y_axis_scatter_2 = y_axis_scatter_2.drop('E09000033', axis=0)
y_axis_scatter_3 = y_axis_scatter_3.drop('E09000033', axis=0)
y_axis_scatter_4 = y_axis_scatter_4.drop('E09000033', axis=0)
x_axis_scatter = x_axis_scatter.drop('E09000033', axis=0)

def model_func(x, a, b):
    return a*x**-1 + b

popt1, pcov = curve_fit(model_func, x_axis_scatter, y_axis_scatter_1)
popt2, pcov = curve_fit(model_func, x_axis_scatter, y_axis_scatter_2)
popt3, pcov = curve_fit(model_func, x_axis_scatter, y_axis_scatter_3)
popt4, pcov = curve_fit(model_func, x_axis_scatter, y_axis_scatter_4)

a1, b1= popt1
a2, b2= popt2
a3, b3= popt3
a4, b4= popt4

x_plot = np.linspace(24000,180000, len(y_axis_scatter_1))
y_plot_1 =np.array(sorted([a1*(x**-1) + b1 for x in x_plot]))
y_plot_2 =np.array(sorted([a2*(x**-1) + b2 for x in x_plot]))
y_plot_3 =np.array(sorted([a3*(x**-1) + b3 for x in x_plot], reverse=True))
y_plot_4 =np.array(sorted([a4*(x**-1) + b4 for x in x_plot]))

def y_transform(x_list, a, b):
    y = [a*(x**-1) + b for x in x_list]
    return y

exp_y_1 = y_transform(x_axis_scatter, a1, b1)
exp_y_2 = y_transform(x_axis_scatter, a2, b2)
exp_y_3 = y_transform(x_axis_scatter, a3, b3)
exp_y_4 = y_transform(x_axis_scatter, a4, b4)

R2_1 = r2_score(y_axis_scatter_1, exp_y_1)
R2_2 = r2_score(y_axis_scatter_2, exp_y_2)
R2_3 = r2_score(y_axis_scatter_3, exp_y_3)
R2_4 = r2_score(y_axis_scatter_4, exp_y_4)

fig,axs = plt.subplots(2,2)
for row in axs:
    for ax in row:
        ax.set_xlabel('Income', fontsize=12)
axs[0,0].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x)))
axs[0,1].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x)))
axs[1,0].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x)))
axs[1,1].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x)))
axs[0,0].plot(x_plot, y_plot_1, color='darkred', linewidth=2.5)
axs[0,1].plot(x_plot, y_plot_2, color='navy', linewidth=2.5)
axs[1,0].plot(x_plot, y_plot_3, color='orange', linewidth=2.5)
axs[1,1].plot(x_plot, y_plot_4, color='darkgreen', linewidth=2.5)
axs[0,0].scatter(x_axis_scatter, y_axis_scatter_1, color='salmon')
axs[0,1].scatter(x_axis_scatter, y_axis_scatter_2, color='lightblue')
axs[1,0].scatter(x_axis_scatter, y_axis_scatter_3, color='moccasin')
axs[1,1].scatter(x_axis_scatter, y_axis_scatter_4, color='lightgreen')
axs[0,0].set_ylabel("Alcohol Volume", fontsize=12)
axs[0,1].set_ylabel("Energy Source Diversity", fontsize=12)
axs[1,0].set_ylabel("Total Energy", fontsize=12)
axs[1,1].set_ylabel("Energy from Fibre", fontsize=12)
fig.suptitle('Fitting a Curve for Income Data vs Normalised Shopping Data', fontsize=24)

plt.tight_layout()
plt.show()

pd.options.display.float_format = '{:,.2f}'.format
results = {'Slope Coefficient': [a1, a2, a3, a4],
        'R Squared': [R2_1, R2_2, R2_3, R2_4]}
results_df = pd.DataFrame(results, index=["Alcohol Volume", "Energy Source Diversity", "Total Energy", "Energy from Fibre"])


