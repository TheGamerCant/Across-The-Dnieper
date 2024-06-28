import customtkinter
from customtkinter import *
import tkinter
from tkinter import Image
from PIL import Image, ImageTk
import numpy as np
import os
import math

class EditorCanvas(tkinter.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg="white", **kwargs)
        current_directory = os.getcwd()
        provinces_bmp_path = os.path.join(current_directory, "map", "provinces.bmp")
        self._img = Image.open(provinces_bmp_path)
        self.img_width, self.img_height = self._img.size
        self.canvas_width = (self.winfo_screenwidth())//5*3
        self.canvas_height = (self.winfo_screenheight()-30)//2
        if self.canvas_width > self.img_width:
            self.canvas_width = self.img_width 
        if self.canvas_height > self.img_height:
            self.canvas_height = self.img_height 

        self.zoom_factor = float(0.000)

    def recieve_img_data(self,top_left_x, top_left_y, bottom_right_x, bottom_right_y):
        self._img_cropped = self._img.crop((top_left_x, top_left_y, bottom_right_x, bottom_right_y))

        width = bottom_right_x - top_left_x
        height = bottom_right_y - top_left_y

        width_ratio = self.canvas_width / width
        height_ratio = self.canvas_height / height
        if width_ratio < height_ratio:
            width = int(round(width*width_ratio))
            height = int(round(height*width_ratio))
            self.zoom_factor = width_ratio
        else:
            width = int(round(width*height_ratio))
            height = int(round(height*height_ratio))
            self.zoom_factor = height_ratio
        self._img_cropped = self._img_cropped.resize((width, height), Image.Resampling.NEAREST)

        self.photo_image = ImageTk.PhotoImage(self._img_cropped)
        self.create_image(self.canvas_width//2, self.canvas_height//2, anchor="center", image=self.photo_image)

class MapCanvas(tkinter.Canvas):
    def __init__(self, master, send_img_data_callback, **kwargs):
        super().__init__(master, bg="white", **kwargs)
        self.send_img_data_callback = send_img_data_callback
        current_directory = os.getcwd()
        provinces_bmp_path = os.path.join(current_directory, "map", "provinces.bmp")
        self._img = Image.open(provinces_bmp_path)
        self._img_array = np.array(self._img)
        self.img_width, self.img_height = self._img.size
        self.real_mouse_coords_x = 0
        self.real_mouse_coords_y = 0
        self._img_top_left_x = 0
        self._img_top_left_y = 0
        self.canvas_width = (self.winfo_screenwidth())//5*3
        self.canvas_height = (self.winfo_screenheight()-30)//2
        if self.canvas_width > self.img_width:
            self.canvas_width = self.img_width 
        if self.canvas_height > self.img_height:
            self.canvas_height = self.img_height 
        self.a = (self.img_width-self.canvas_width)*-1
        self.b = (self.img_height-self.canvas_height)*-1
        self.left_button_pressed=False
        self.init_lc_coords_x = None
        self.init_lc_coords_y = None

        #print (self.img_width, self.img_height, self.canvas_width, self.canvas_height)

        self.bind("<ButtonPress-2>", self.on_start_drag)
        self.bind("<B2-Motion>", self.on_drag,)
        self.bind("<ButtonPress-1>", self.on_left_click)
        self.bind("<ButtonRelease-1>", self.on_left_click_release,)
        self.bind("<Motion>", self.on_mouse_motion)

        self.display_provinces()

    
    def display_provinces(self):
        self.photo_image = ImageTk.PhotoImage(self._img)
        self.create_image(0, 0, anchor="nw", image=self.photo_image)

    def on_start_drag(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        if self.start_x is not None and self.start_y is not None:
            delta_x = event.x - self.start_x
            delta_y = event.y - self.start_y
            self.start_x = event.x
            self.start_y = event.y
            self._img_top_left_x+=delta_x
            self._img_top_left_y+=delta_y

            if self._img_top_left_x > 0 or self._img_top_left_y > 0:
                if self._img_top_left_x < 0 and self._img_top_left_y > 0:
                    self.move(ALL, delta_x, 0)
                    self._img_top_left_y = 0
                elif self._img_top_left_x > 0 and self._img_top_left_y < 0:
                    self.move(ALL, 0, delta_y)
                    self._img_top_left_x = 0
                else:
                    self._img_top_left_x = 0
                    self._img_top_left_y = 0
        
            elif self._img_top_left_x < self.a or self._img_top_left_y < self.b:
                if self._img_top_left_x > self.a and self._img_top_left_y < self.b:
                    self.move(ALL, delta_x, 0)
                    self._img_top_left_y = self.b
                elif self._img_top_left_x < self.a and self._img_top_left_y > self.b:
                    self.move(ALL, 0, delta_y)
                    self._img_top_left_x = self.a
                else:
                    self._img_top_left_x = self.a
                    self._img_top_left_y = self.b
            else:
                self.move(ALL, delta_x, delta_y)

    def on_mouse_motion(self, event):
        self.real_mouse_coords_x = event.x - self._img_top_left_x
        self.real_mouse_coords_y = event.y - self._img_top_left_y
        if self.left_button_pressed==True:
            self.coords(self.rect,self.init_lc_coords_x, self.init_lc_coords_y, self.real_mouse_coords_x\
                                 + self._img_top_left_x, self.real_mouse_coords_y + self._img_top_left_y)
    
    def on_left_click(self, event):
        self.init_lc_coords_x = self.real_mouse_coords_x + self._img_top_left_x
        self.init_lc_coords_y = self.real_mouse_coords_y + self._img_top_left_y
        self.rect = self.create_rectangle(self.init_lc_coords_x, self.init_lc_coords_y, self.init_lc_coords_x, self.init_lc_coords_y, outline="white")
        self.left_button_pressed=True

    def on_left_click_release(self, event):
        self.left_button_pressed=False
        self.send_img_data_callback(self.init_lc_coords_x-self._img_top_left_x, self.init_lc_coords_y-self._img_top_left_y, self.real_mouse_coords_x, self.real_mouse_coords_y)
        self.delete(self.rect)

class BorderFrameForEditor(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        current_directory = os.getcwd()
        provinces_bmp_path = os.path.join(current_directory, "map", "provinces.bmp")
        self._img = Image.open(provinces_bmp_path)
        self.img_width, self.img_height = self._img.size
        self._img.close()
        self.canvas_width = (self.winfo_screenwidth())//5*3
        self.canvas_height = (self.winfo_screenheight()-30)//2

        if self.canvas_width > self.img_width:
            self.canvas_width = self.img_width 

        if self.canvas_height > self.img_height:
            self.canvas_height = self.img_height 

        self.canvas = EditorCanvas(master = self, width=(self.canvas_width), height=(self.canvas_height))
        self.canvas.pack(pady=4, padx=4)
    
    def send_img_data_forward(self, top_left_x, top_left_y, bottom_right_x, bottom_right_y):
        self.canvas.recieve_img_data(top_left_x, top_left_y, bottom_right_x, bottom_right_y)

class BorderFrameForMap(customtkinter.CTkFrame):
    def __init__(self, master, send_img_data_callback,**kwargs):
        super().__init__(master, **kwargs)
        self.send_img_data_callback = send_img_data_callback
        current_directory = os.getcwd()
        provinces_bmp_path = os.path.join(current_directory, "map", "provinces.bmp")
        self._img = Image.open(provinces_bmp_path)
        self.img_width, self.img_height = self._img.size
        self._img.close()
        self.canvas_width = (self.winfo_screenwidth())//5*3
        self.canvas_height = (self.winfo_screenheight()-30)//2
        if self.canvas_width > self.img_width:
            self.canvas_width = self.img_width 
        if self.canvas_height > self.img_height:
            self.canvas_height = self.img_height 

        self.canvas = MapCanvas(self, self.send_data_to_display, width=(self.canvas_width), height=(self.canvas_height))
        self.canvas.pack(pady=4, padx=4)

    def send_data_to_display(self, top_left_x, top_left_y, bottom_right_x, bottom_right_y):
        self.send_img_data_callback(top_left_x, top_left_y, bottom_right_x, bottom_right_y)

class App(customtkinter.CTk):
    def __init__(self,screen_width, screen_height,provincesArray, statesArray, strategicRegionsArray, buildingsArray, terrainArray, triggersArray):
        super().__init__()
        self.geometry(f"{screen_width}x{screen_height}")

        self.fullscreen_state = True
        self.attributes("-fullscreen", self.fullscreen_state)
        self.bind("<Escape>", self.toggle_fullscreen)

        self.map_frame = BorderFrameForMap(self, self.send_data_to_display, width=(screen_width//3*2), height=((screen_height-30)//2))
        self.map_frame.pack(padx=15, pady=15,anchor="nw" )

        self.editor_frame = BorderFrameForEditor(self, width=(screen_width//3*2), height=((screen_height-30)//2))
        self.editor_frame.pack(padx=15, pady=15,anchor="sw" )

    def toggle_fullscreen(self,event=None):
        self.fullscreen_state = not self.fullscreen_state
        self.attributes("-fullscreen", self.fullscreen_state)
        return "break"
    
    def send_data_to_display(self, top_left_x, top_left_y, bottom_right_x, bottom_right_y):
        self.editor_frame.send_img_data_forward(top_left_x, top_left_y, bottom_right_x, bottom_right_y)

def tkinter_main(provincesArray, statesArray, strategicRegionsArray, buildingsArray, terrainArray, triggersArray):
    root = CTk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()

    
    customtkinter.set_appearance_mode("light")
    #customtkinter.set_default_color_theme("__code__/__assets__/customtkinter_profile.json")
    app = App(screen_width,screen_height,provincesArray, statesArray, strategicRegionsArray, buildingsArray, terrainArray, triggersArray)
    app.mainloop()