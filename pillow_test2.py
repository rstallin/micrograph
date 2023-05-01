import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageDraw, ImageTk

# Create an instance of tkinter frame
win = tk.Tk()

# Set the geometry of tkinter frame
win.geometry("700x350")



def open_file():
    file = filedialog.askopenfile(mode='rb', filetypes=[('PNG Images', '*.png')])
    global image_tk
    if file:
        image = Image.open(file)
        image_tk = ImageTk.PhotoImage(image)
        l1 = tk.Label(win)
        
        l1.image = image_tk
        l1['image'] = image_tk
    

# Add a Label widget
label = tk.Label(win, text="Click the Button to browse the Files", font=('Georgia 13'))
label.pack(pady=10)

# Create a Button
ttk.Button(win, text="Browse", command=open_file).pack(pady=20)

win.mainloop()