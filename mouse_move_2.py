import mouse
import keyboard
import os
from pathlib import Path

events = []                 #This is the list where all the events will be stored
mouse.hook(events.append)   #starting the mouse recording
keyboard.wait("a")          #Waiting for 'a' to be pressed
mouse.unhook(events.append) #Stopping the mouse recording
# mouse.play(events)          #Playing the recorded events
# print(type(events))
file_path = f"D:\\Users\\Marina\\Documents\\школа\\mouse_move\\mouse_2.csv"
if not os.path.exists(file_path):
     with open(file_path, 'w+'): pass

file = open(file_path, 'w+', encoding='utf-8')
file.write(f"timestamp,X,Y\n")
for event in events:
    file.write(f"{event.time}, {event.x}, {event.y}\n")