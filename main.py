import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QDial, QMessageBox, QSpinBox, QComboBox, QListWidget, QCheckBox, QApplication, QMainWindow, QPushButton, QWidget, QLineEdit, QLabel, QVBoxLayout, QSlider, QTableWidget
import mouse
import keyboard
import os
from pathlib import Path
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

folder_path = "D:/Users/Marina/Documents/школа/mouse_move/"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Приложение")


        widget = QListWidget()
        widget.addItems(["Генерим хитмап мыши от Алисы",
                         "Генерим хитмап мыши от Боба",
                         "Генерим хитмап мыши от Евы",
                         "Анализируем хитмапы на похожесть",
                         "Выход"])
        widget.itemClicked.connect(self.index_changed)
        self.setCentralWidget(widget)
    
    def index_changed(self, i):
        if i.text() == "Генерим хитмап мыши от Алисы":
            print("call alice")
            mousemove("alice")
        elif i.text() == "Генерим хитмап мыши от Боба":
            print("call bob")
            mousemove("bob")
        elif i.text() == "Генерим хитмап мыши от Евы":
            print("call eva")
            mousemove("eva")
        elif i.text() == "Анализируем хитмапы на похожесть":
            print("evaluate")
            evaluate()
        elif i.text() == "Выход":
            exit()


def mousemove(name):
    QMessageBox.information(main,f"Запись движений мыши для {name}","Закройтей это диалоговое окно, начнется запись. Чтобы закончить, нажми 'a'")
    #main.statusBar().showMessage("Запись движений мыши для "+name+" началась. Чтобы закончить, нажми 'a'")
    events = []                 #This is the list where all the events will be stored
    mouse.hook(events.append)   #starting the mouse recording
    keyboard.wait("a")          #Waiting for 'a' to be pressed
    mouse.unhook(events.append) #Stopping the mouse recording
    main.statusBar().showMessage("Запись движений мыши для "+name+" закончена",2000)

    # mouse.play(events)          #Playing the recorded events
    # print(type(events))
    #file_path = f"D:\\Users\\Marina\\Documents\\школа\\mouse_move\\alice.csv"
    file_path = folder_path + name + ".csv"
    if not os.path.exists(file_path):
        with open(file_path, 'w+'): pass

    file = open(file_path, 'w+', encoding='utf-8')
    file.write("timestamp,X,Y\n")
    for event in events:
        file.write(f"{event.time}, {event.x}, {event.y}\n")

def evaluate():
    grid_size = 10
    dataframes = {}
    heatmap_data = {}
    average_speed = {}
    heatmap_data_pd = {}

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
        print(f'Average speed of {df_name} mouse movement: {average_speed[df_name]:.2f} pixels/second')
        # print(df_name)
        # print(df)

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
        # print(df_name)
        # print(heatmap_data[df_name])
        heatmap_data_pd[df_name] = pd.DataFrame(heatmap_data[df_name])
        print("heatmap_data_pd[df_name]:")
        print(heatmap_data_pd[df_name])

    fig, axs = plt.subplots(1, len(dataframes), figsize=(12, 6))
    i = 0
    for df_name in heatmap_data:
        axs[i].imshow(heatmap_data[df_name], cmap='coolwarm', interpolation='nearest')
        axs[i].set_title(f'{df_name} Av.speed: {average_speed[df_name]:.2f} p/sec')
        axs[i].axis('off')
        i += 1

    plt.tight_layout()
    plt.show()

    alice_eva_df = pd.concat([dataframes['alice'], dataframes['eva']], axis=0, ignore_index=True)
    alice_eva_correlation = alice_eva_df.corr()
    print("alice_eva_df:")
    print(alice_eva_df)
    print("alice_eva_correlation:")
    print(alice_eva_correlation)
    bob_eva_df = pd.concat([dataframes['bob'], dataframes['eva']], axis=0, ignore_index=True)
    bob_eva_correlation = bob_eva_df.corr()
    print("bob_eva_df:")
    print(bob_eva_df)
    print("bob_eva_correlation:")
    print(bob_eva_correlation)

    alice_eva_hitmap = pd.concat([heatmap_data_pd['alice'], heatmap_data_pd['eva']], axis=0, ignore_index=True)
    alice_eva_hitmap_correlation = alice_eva_hitmap.corr()
    print("alice_eva_hitmap:")
    print(alice_eva_hitmap)
    print(alice_eva_hitmap_correlation)
    bob_eva_hitmap = pd.concat([heatmap_data_pd['bob'], heatmap_data_pd['eva']], axis=0, ignore_index=True)
    bob_eva_hitmap_correlation = bob_eva_hitmap.corr()
    print("bob_eva_hitmap:")
    print(bob_eva_hitmap)
    print(bob_eva_hitmap_correlation)
    


'''

        self.label = QLabel()

        self.input = QLineEdit()
        self.input.textChanged.connect(self.label.setText)

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.label)

        container = QWidget()   
        container.setLayout(layout)

        self.setCentralWidget(container)

'''

'''
        button = QPushButton("Нажми меня!")
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)

        self.setFixedSize(QSize(800, 600))

        self.setCentralWidget(button)

    def the_button_was_clicked(self):
        print("Кнопка нажата")    
'''

if __name__ == '__main__':
  app = QApplication(sys.argv)
  main = MainWindow()
  main.resize(350,120)
  #main.showMaximized()
  main.show()
  sys.exit(app.exec())
