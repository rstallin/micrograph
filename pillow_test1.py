import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import math

# Open the image
image = Image.open("micrograph.png")

root = tk.Tk()

# Create an object of tkinter ImageTk
image_tk = ImageTk.PhotoImage(image)

# keep track of dots on micrograph
count = []

def distance(p1,p2):
    if type(p1) == tuple:
        dx = p1[0]-p2[0]
        dy = p1[1]-p2[1]
        return math.sqrt(dx**2 + dy**2)
    else: return abs(p1-p2)


# Define a function to handle mouse clicks
def click_handler(event):
    # Get the coordinates of the mouse click
    x, y = event.x, event.y
    sz = 4
    
    # create oval upon click
    canvas.create_oval(x-sz,y-sz,x+sz,y+sz, fill="red")
    
    global count
    count.append((x,y))
    if len(count) == 2:
        dist = distance(count[0],count[1])
        count.append(dist)
        print(count)
        count = []





# Display the image in a Tkinter window

root.geometry("{}x{}".format(*image.size))
canvas = tk.Canvas(root, width=image.size[0], height=image.size[1], bg = "white")
canvas.pack()


# Draw the image on the canvas
canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)

# Bind the mouse click event to the canvas
canvas.bind("<Button-1>", click_handler)


# Start the Tkinter event loop
root.mainloop()

