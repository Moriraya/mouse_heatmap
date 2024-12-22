import os
import pandas as pd
from pathlib import Path
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
folder_path = f"D:\\Users\\Marina\\Documents\\школа\\mouse_move" # movement data generated from the mouse logger application

grid_size = 100
dataframes = {}
heatmap_data = {}
average_speed = {}

for file_name in os.listdir(folder_path):
    if file_name.endswith(".csv"):
        file_path = os.path.join(folder_path, file_name)
        df_name = file_name.split(".")[0]
        dataframes[df_name] = pd.read_csv(file_path, sep=",", header="infer")

for df_name in dataframes:
    df = dataframes[df_name]
    speeds = []
    for i in range(1, len(df)):
        dx = df.loc[i,'X'] - df.loc[i - 1,'X']
        dy = df.loc[i,'Y'] - df.loc[i - 1,'Y']
        dt = df.loc[i,'timestamp'] - df.loc[i - 1,'timestamp']
        speed = ((dx**2 + dy**2)**0.5) / dt if dt > 0 else 0
        speeds.append(speed)
    
    average_speed[df_name] = sum(speeds) / len(speeds) if speeds else 0
    print(f'Average speed of mouse movement: {average_speed[df_name]:.2f} pixels/second')

for df_name in dataframes:
    df = dataframes[df_name]
    heatmap_data [df_name] = np.zeros((grid_size, grid_size))
    x_bins = np.linspace(0, df['X'].max(), grid_size + 1)
    y_bins = np.linspace(0, df['Y'].max(), grid_size + 1)
    df['X_bin'] = np.digitize(df['X'], x_bins) - 1
    df['Y_bin'] = np.digitize(df['Y'], y_bins) - 1
    df['X_bin'] = df['X_bin'].clip(0, grid_size - 1)
    df['Y_bin'] = df['Y_bin'].clip(0, grid_size - 1)
    for x_bin, y_bin in zip(df['X_bin'], df['Y_bin']):
        heatmap_data[df_name][y_bin, x_bin] += 1

fig, axs = plt.subplots(1, 2, figsize=(12, 6))
i = 0
for df_name in heatmap_data:
    axs[i].imshow(heatmap_data[df_name], cmap='coolwarm', interpolation='nearest')
    axs[i].set_title(f'{df_name} Av.speed: {average_speed[df_name]:.2f} p/sec')
    axs[i].axis('off')
    i += 1

plt.tight_layout()
plt.show()

