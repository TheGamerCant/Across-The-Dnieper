import customtkinter
from customtkinter import *
import tkinter
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import os
import math
from func import rgbToHex

class EditorCanvas(tkinter.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg="white", **kwargs)
        global currentButtonOperation
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

        self.top_left_x = 0
        self.top_left_y = 0
        self.bottom_right_x = 0
        self.bottom_right_y = 0
        self.photo_image = None
        self.zoom_factor = float(0.000)
        self.width = 0
        self.height = 0
        self.white_space_width = 0
        self.white_space_height = 0

        self.bind("<Motion>", self.on_mouse_motion)
        self.real_mouse_coords_x = 0
        self.real_mouse_coords_y = 0
        self.current_prov_grid_coords = []
        self.rect_outline = None

    def recieve_img_data(self,top_left_x, top_left_y, bottom_right_x, bottom_right_y):
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.bottom_right_x = bottom_right_x
        self.bottom_right_y = bottom_right_y

        self._img_cropped = self._img.crop((top_left_x, top_left_y, bottom_right_x, bottom_right_y))

        self.width = bottom_right_x - top_left_x
        self.height = bottom_right_y - top_left_y

        width_ratio = self.canvas_width / self.width
        height_ratio = self.canvas_height / self.height
        if width_ratio < height_ratio:
            self.zoom_factor = math.floor(width_ratio)
        else:
            self.zoom_factor = math.floor(height_ratio)

        self.width = int(round(self.width*self.zoom_factor))
        self.height = int(round(self.height*self.zoom_factor))
        self._img_cropped = self._img_cropped.resize((self.width, self.height), Image.Resampling.NEAREST)

        #print (self.zoom_factor, self.width, self.height)
        self.photo_image = ImageTk.PhotoImage(self._img_cropped)
        self.create_image(self.canvas_width//2, self.canvas_height//2, anchor="center", image=self.photo_image)

        self.white_space_width = (self.canvas_width - self.width)//2
        self.white_space_height = (self.canvas_height - self.height)//2

    def on_mouse_motion(self, event):
        self.real_mouse_coords_x = event.x
        self.real_mouse_coords_y = event.y

        if self.photo_image!= None and self.real_mouse_coords_x >= self.white_space_width and self.real_mouse_coords_x <= \
                (self.canvas_width - self.white_space_width)and self.real_mouse_coords_y >= self.white_space_height and \
                self.real_mouse_coords_y <= (self.canvas_height - self.white_space_height):
            rect_top_left_x = (self.real_mouse_coords_x - self.white_space_width)//self.zoom_factor
            rect_top_left_y = (self.real_mouse_coords_y - self.white_space_height)//self.zoom_factor
            if rect_top_left_x > (self.bottom_right_x - self.top_left_x-1):
                rect_top_left_x-=1
            if rect_top_left_y > (self.bottom_right_y - self.top_left_y-1):
                rect_top_left_y-=1
            self.current_prov_grid_coords = [rect_top_left_x, rect_top_left_y]
            rect_top_left_x = self.white_space_width + (rect_top_left_x*self.zoom_factor)
            rect_top_left_y = self.white_space_height + (rect_top_left_y*self.zoom_factor)
            self.delete(self.rect_outline)
            self.rect_outline = self.create_rectangle(rect_top_left_x, rect_top_left_y, rect_top_left_x+self.zoom_factor, rect_top_left_y+self.zoom_factor, outline="gray51")

        #print(self.real_mouse_coords_x,self.real_mouse_coords_y)

class MapCanvas(tkinter.Canvas):
    def __init__(self, master, send_img_data_callback, send_selected_colour_callback, **kwargs):
        super().__init__(master, bg="white", **kwargs)
        global currentButtonOperation
        self.send_img_data_callback = send_img_data_callback
        self.send_selected_colour_callback = send_selected_colour_callback
        current_directory = os.getcwd()
        provinces_bmp_path = os.path.join(current_directory, "map", "provinces.bmp")
        self._img = Image.open(provinces_bmp_path)
        #self._img_array = np.array(self._img)
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
        if currentButtonOperation == "Select Colour":
            pass
        elif self.left_button_pressed==True:
            self.coords(self.rect,self.init_lc_coords_x, self.init_lc_coords_y, self.real_mouse_coords_x\
                        + self._img_top_left_x, self.real_mouse_coords_y + self._img_top_left_y)
    
    def on_left_click(self, event):
        if currentButtonOperation == "Select Colour":
            pass
        else:
            self.init_lc_coords_x = self.real_mouse_coords_x + self._img_top_left_x
            self.init_lc_coords_y = self.real_mouse_coords_y + self._img_top_left_y
            self.rect = self.create_rectangle(self.init_lc_coords_x, self.init_lc_coords_y, self.init_lc_coords_x, self.init_lc_coords_y, outline="white")
            self.left_button_pressed=True

    def on_left_click_release(self, event):
        if currentButtonOperation == "Select Colour":
            r,g,b = self._img.getpixel((self.real_mouse_coords_x, self.real_mouse_coords_y))
            self.send_selected_colour_callback(r,g,b)
        else:
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

        self.canvas = EditorCanvas(master = self, width=(self.canvas_width), height=(self.canvas_height), borderwidth=0)
        self.canvas.pack(pady=4, padx=4)
    
    def send_img_data_forward(self, top_left_x, top_left_y, bottom_right_x, bottom_right_y):
        self.canvas.recieve_img_data(top_left_x, top_left_y, bottom_right_x, bottom_right_y)

class BorderFrameForMap(customtkinter.CTkFrame):
    def __init__(self, master, send_img_data_callback, send_selected_colour_callback,**kwargs):
        super().__init__(master, **kwargs)
        self.send_img_data_callback = send_img_data_callback
        self.send_selected_colour_callback = send_selected_colour_callback
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

        self.canvas = MapCanvas(self, self.send_img_data_to_display, self.send_selected_colour_rgb_data_to_display, width=(self.canvas_width), height=(self.canvas_height), borderwidth=0)
        self.canvas.pack(pady=4, padx=4)

    def send_img_data_to_display(self, top_left_x, top_left_y, bottom_right_x, bottom_right_y):
        self.send_img_data_callback(top_left_x, top_left_y, bottom_right_x, bottom_right_y)
        
    def send_selected_colour_rgb_data_to_display(self, r,g,b):
        self.send_selected_colour_callback(r,g,b)

class App(customtkinter.CTk):
    def __init__(self,screen_width, screen_height, provincesArrayHexID):
        super().__init__()
        self.geometry(f"{screen_width}x{screen_height}")

        self.fullscreen_state = True
        self.attributes("-fullscreen", self.fullscreen_state)
        self.bind("<Escape>", self.toggle_fullscreen)

        current_directory = os.getcwd()
        assets_folder_path = os.path.join(current_directory, "__code__", "__assets__")
        self.undo_photo_image = Image.open(assets_folder_path+"\\undo.dds")
        self.undo_photo_image = ImageTk.PhotoImage(self.undo_photo_image)
        self.select_colour_photo_image = Image.open(assets_folder_path+"\\select_colour.dds")
        self.select_colour_photo_image = ImageTk.PhotoImage(self.select_colour_photo_image)
        self.paint_bucket_photo_image = Image.open(assets_folder_path+"\\paint_bucket.dds")
        self.paint_bucket_photo_image = ImageTk.PhotoImage(self.paint_bucket_photo_image)
        self.pencil_photo_image = Image.open(assets_folder_path+"\\pencil.dds")
        self.pencil_photo_image = ImageTk.PhotoImage(self.pencil_photo_image)

        self.undo_button = customtkinter.CTkButton(master = self,text='', image=self.undo_photo_image, border_width=2, fg_color="transparent", hover_color="deep sky blue", border_color="deep sky blue", command=self.undo_button_press)
        self.undo_button.place(relx=1.00,rely=0, x=-146, y=6)

        self.select_colour_button = customtkinter.CTkButton(master = self,text='', image=self.select_colour_photo_image, border_width=2, fg_color="transparent", hover_color="deep sky blue", border_color="deep sky blue", command=self.select_colour_button_press)
        self.select_colour_button.place(relx=1.00,rely=0, x=-146, y=86)

        self.current_colour_square = tkinter.Canvas(self, width = 40, height = 40, background="black", borderwidth=0)
        self.current_colour_square.place(relx=1.00,rely=0, x=-210, y=101)

        self.paint_bucket_button = customtkinter.CTkButton(master = self,text='', image=self.paint_bucket_photo_image, border_width=2, fg_color="transparent", hover_color="deep sky blue", border_color="deep sky blue", command=self.paint_bucket_button_press)
        self.paint_bucket_button.place(relx=1.00,rely=0, x=-146, y=166)

        self.pencil_button = customtkinter.CTkButton(master = self,text='', image=self.pencil_photo_image, border_width=2, fg_color="transparent", hover_color="deep sky blue", border_color="deep sky blue", command=self.pencil_button_press)
        self.pencil_button.place(relx=1.00,rely=0, x=-146, y=246)

        self.map_frame = BorderFrameForMap(self, self.send_img_data_to_display, self.send_selected_colour_rgb_data_to_display, width=(screen_width//3*2), height=((screen_height-30)//2))
        self.map_frame.place(relx=0,rely=0, x = 8)

        self.editor_frame = BorderFrameForEditor(self, width=(screen_width//3*2), height=((screen_height-30)//2))
        self.editor_frame.place(relx=0,rely=0.5, x = 8)
      

    def toggle_fullscreen(self,event=None):
        self.fullscreen_state = not self.fullscreen_state
        self.attributes("-fullscreen", self.fullscreen_state)
        return "break"
    
    def send_img_data_to_display(self, top_left_x, top_left_y, bottom_right_x, bottom_right_y):
        self.editor_frame.send_img_data_forward(top_left_x, top_left_y, bottom_right_x, bottom_right_y)

    def send_selected_colour_rgb_data_to_display(self,r,g,b):
        hexadecimal = str("#" + rgbToHex(r,g,b))
        self.current_colour_square.config(background=hexadecimal)

    def clear_buttons(self):
        self.undo_button.configure(fg_color="transparent")
        self.select_colour_button.configure(fg_color="transparent")
        self.paint_bucket_button.configure(fg_color="transparent")
        self.pencil_button.configure(fg_color="transparent")
        global currentButtonOperation
        currentButtonOperation = "None"

    def undo_button_press (self):
        global currentButtonOperation
        if currentButtonOperation == "Undo":
            self.clear_buttons()
        else:
            self.clear_buttons()
            currentButtonOperation = "Undo"
            self.undo_button.configure(fg_color="deep sky blue")
        

    def select_colour_button_press (self):
        global currentButtonOperation
        if currentButtonOperation == "Select Colour":
            self.clear_buttons()
        else:
            self.clear_buttons()
            currentButtonOperation = "Select Colour"
            self.select_colour_button.configure(fg_color="deep sky blue")

    def paint_bucket_button_press (self):
        global currentButtonOperation
        if currentButtonOperation == "Paint Bucket":
            self.clear_buttons()
        else:
            self.clear_buttons()
            currentButtonOperation = "Paint Bucket"
            self.paint_bucket_button.configure(fg_color="deep sky blue")

    def pencil_button_press (self):
        global currentButtonOperation
        if currentButtonOperation == "Pencil":
            self.clear_buttons()
        else:
            self.clear_buttons()
            currentButtonOperation = "Pencil"
            self.pencil_button.configure(fg_color="deep sky blue")

def tkinter_main(provincesArrayHexID):
    root = CTk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()

    global currentButtonOperation
    currentButtonOperation = "None"
    
    customtkinter.set_appearance_mode("light")
    #customtkinter.set_default_color_theme("__code__/__assets__/customtkinter_profile.json")
    app = App(screen_width,screen_height, provincesArrayHexID)
    app.mainloop()