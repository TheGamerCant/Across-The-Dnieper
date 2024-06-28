import customtkinter
from customtkinter import *
import tkinter
from tkinter import Canvas, Image
from PIL import Image, ImageTk
import os

class MyFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<ButtonPress-2>", self.on_start_drag)
        self.bind("<B2-Motion>", self.on_drag,)

        current_directory = os.getcwd()
        provinces_bmp_path = os.path.join(current_directory, "map", "provinces.bmp")
        self._img = Image.open(provinces_bmp_path)
        self.img_width, self.img_height = self._img.size
        
        self.canvas_width = (self.winfo_screenwidth())//5*3
        self.canvas_height = self.winfo_screenheight()-30

        if self.canvas_width > self.img_width:
            self.canvas_width = self.img_width 

        if self.canvas_height > self.img_height:
            self.canvas_height = self.img_height 

        self.canvas = tkinter.Canvas(master = self, width=(self.canvas_width), height=(self.canvas_height))
        self.canvas.pack(pady=4, padx=4)
        self.display_img()

    
    def display_img(self):
        self.photo_image = ImageTk.PhotoImage(self._img)
        self.canvas.create_image(0, 0, anchor="nw", image=self.photo_image)

    def on_start_drag(self, event):
        self.start_x = event.x
        self.start_y = event.y
        print ("Start drag")

    def on_drag(self, event):
        if self.start_x is not None and self.start_y is not None:
            delta_x = event.x - self.start_x
            delta_y = event.y - self.start_y
            self.canvas.move(ALL, delta_x, delta_y)



class App(customtkinter.CTk):
    def __init__(self,screen_width, screen_height,provincesArray, statesArray, strategicRegionsArray, buildingsArray, terrainArray, triggersArray):
        super().__init__()
        self.geometry(f"{screen_width}x{screen_height}")

        self.fullscreen_state = True
        self.attributes("-fullscreen", self.fullscreen_state)
        self.bind("<Escape>", self.toggle_fullscreen)

        self.my_frame = MyFrame(master=self, width=(screen_width//3*2), height=(screen_height-30))
        self.my_frame.pack(padx=15, pady=15,anchor="nw" )

    def toggle_fullscreen(self,event=None):
        self.fullscreen_state = not self.fullscreen_state
        self.attributes("-fullscreen", self.fullscreen_state)
        return "break"

def tkinter_main(provincesArray, statesArray, strategicRegionsArray, buildingsArray, terrainArray, triggersArray):
    root = CTk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()

    
    customtkinter.set_appearance_mode("light")
    #customtkinter.set_default_color_theme("__code__/__assets__/customtkinter_profile.json")
    app = App(screen_width,screen_height,provincesArray, statesArray, strategicRegionsArray, buildingsArray, terrainArray, triggersArray)
    app.mainloop()