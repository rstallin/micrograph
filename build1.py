from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageDraw, ImageTk

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.canvas = None
        self.image_tk = None
        self.calibration = [] # keep track of calibration coordinates
        self.cal_check = False # if in calibration, store coordinates somewhere

        self.pack()
        self.create_widgets()


    def create_widgets(self):
        # Add a Label widget
        self.label = Label(self, text="Click the Button to browse the Files", font=('Georgia 13'))
        self.label.pack(pady=10)

        # Create a Button
        self.browse_button = ttk.Button(self, text="Browse", command=self.open_file)
        self.browse_button.pack(pady=20)

    def open_file(self):
        file = filedialog.askopenfile(mode='rb', filetypes=[('PNG Images', '*.png')])
        if file:
            image = Image.open(file)
            self.image_tk = ImageTk.PhotoImage(image)
            self.show_image()

    def show_image(self):
        # remove all previous widgets
        self.clear()


        # Display the image in a Tkinter window
        wid = self.image_tk.width()
        height = self.image_tk.height()
        self.master.geometry("{}x{}".format(wid,height+200))
        self.canvas = Canvas(self.master, width=wid, height=height, bg="white")

        # Draw the image on the canvas
        self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)

        # Bind the mouse click event to the canvas
        self.canvas.bind("<Button-1>", self.click_handler)

    def clear(self):
        # destroy all widgets that aren't master frame
        for widget in self.winfo_children():
            widget.destroy()

    # Define a function to handle mouse clicks
    def click_handler(self, event):
        # Get the coordinates of the mouse click
        x, y = event.x, event.y

        # Draw a red dot at the clicked location
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red")

        # Print the clicked coordinates
        print("Clicked at: ({}, {})".format(x, y))


    def distance(self, p1, p2):
        if type(p1) == tuple:
            dx = p1[0]-p2[0]
            dy = p1[1]-p2[1]
            return math.sqrt(dx**2 + dy**2)
        else: return abs(p1-p2)


root = Tk()
app = Application(master=root)
app.mainloop()
