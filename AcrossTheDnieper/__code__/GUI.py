import customtkinter
from customtkinter import *
import tkinter
from tkinter import Canvas
from PIL import Image
import os

class MyFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        current_directory = os.getcwd()
        print(current_directory)

        self.canvas = tkinter.Canvas(master = self, bg="white", height=500, width=700)
        self.canvas.pack(pady=20, padx=20)
        # add widgets onto the frame, for example:
        #self.label = customtkinter.CTkLabel(self)
        #self.label.grid(row=0, column=0, padx=20)


class App(customtkinter.CTk):
    def __init__(self,screen_width, screen_height,provincesArray, statesArray, strategicRegionsArray, buildingsArray, terrainArray, triggersArray):
        super().__init__()
        self.geometry(f"{screen_width}x{screen_height}")

        self.fullscreen_state = True
        self.attributes("-fullscreen", self.fullscreen_state)
        self.bind("<Escape>", self.toggle_fullscreen)

        self.my_frame = MyFrame(master=self, width=(screen_width//3*2), height=(screen_height-36))
        self.my_frame.pack(side= LEFT, padx=18, pady=18)

    def toggle_fullscreen(self,event=None):
        self.fullscreen_state = not self.fullscreen_state
        self.attributes("-fullscreen", self.fullscreen_state)
        return "break"

def tkinter_main(provincesArray, statesArray, strategicRegionsArray, buildingsArray, terrainArray, triggersArray):
    root = CTk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()

    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")
    app = App(screen_width,screen_height,provincesArray, statesArray, strategicRegionsArray, buildingsArray, terrainArray, triggersArray)
    app.mainloop()