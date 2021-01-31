import functools
import tkinter as tk
from PIL import Image, ImageTk
from scrapper import next_image, save_image, TEMP_PATH, SAVED_PATH

def button_handler(func):
    """Handle bad response code and raise error when encounter"""
    @functools.wraps(func)
    def inner(self, *args, **kwargs):
        if self.button_used:
            return
        self.button_used = True
        self.reset_error()
        try:
            func(self, *args, **kwargs)
        except Exception as err:
            self.set_error(err)
        finally:
            self.button_used = False
    return inner

class ImageBoxApp(tk.Tk):
    current_image_id = None
    current_image = None
    current_tk_image = None
    saving_name = None
    error_str = None
    button_used = False

    display_x = 760
    display_y = 460

    def __init__(self):
        tk.Tk.__init__(self)
        self.create_widgets()
        self.next_image()

    @property
    def image_display_size(self):
        img_x = self.current_image.width
        img_y = self.current_image.height
        x_ratio = img_x/self.display_x
        y_ratio = img_y/self.display_y
        if x_ratio > y_ratio:
            between_ratio = img_x/img_y
            img_x = int(img_x * 1/x_ratio)
            img_y = int(img_x/between_ratio)
        else:
            between_ratio = img_y/img_x
            img_y = int(img_y * 1/y_ratio)
            img_x = int(img_y/between_ratio)
        return (img_x,img_y)

    @property
    def current_temp_image_path(self):
        return TEMP_PATH.format(self.current_image_id)

    def create_widgets(self):
        # saving label
        self.save_label = tk.Label(self, text ="name of the file to save :")
        self.save_label.place(x=190,y=550,width=250, height=50)
 
        # saving name
        self.saving_name = tk.StringVar()
        self.entry_text = tk.Entry(self,textvariable=self.saving_name, bg='white', highlightbackground='blue') #,highlightcolor= "green")
        self.entry_text.place(x=400,y=565,width=250, height=20)

        # next button
        self.next_button = tk.Button(self, text='next', bg='grey', cursor="hand2", command=self.next_image)
        self.next_button.place(x=140,y=500,width=250, height=50)

        # saving button
        self.save_button = tk.Button(self, text='save', bg='green', cursor="hand2", command=self.save_image)
        self.save_button.place(x=410,y=500,width=250, height=50)

        # image place
        self.image_displayer = tk.Canvas(self)
        self.image_displayer.place(x=20,y=20,width=self.display_x, height=self.display_y)

        # error text field
        self.error_str = tk.StringVar()
        # self.error_str.set('aaaaaa')
        self.error_label = tk.Label(self,textvariable=self.error_str)
        self.error_label.configure(foreground='red')
        self.error_label.place(x=100,y=480,width=600, height=10)

    @button_handler
    def next_image(self):
        self.current_image_id = next_image()
        self.saving_name.set(self.current_image_id)
        self.image_displayer.create_rectangle(0,0,self.display_x, self.display_y, fill='grey')
        self.current_image = Image.open(self.current_temp_image_path)
        self.current_image = self.current_image.resize(self.image_display_size)
        self.current_tk_image = ImageTk.PhotoImage(self.current_image)
        self.image_displayer.create_image(self.display_x/2, self.display_y/2,image=self.current_tk_image)

    @button_handler
    def save_image(self):
        save_image(self.current_image_id,self.saving_name.get())
        self.button_used = False
        self.next_image()

    def set_error(self,err):
        self.error_str.set(str(err))

    def reset_error(self):
        self.error_str.set('')