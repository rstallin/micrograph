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
        self.img_dim = None
        self.calibration = [] # keep track of calibration coordinates
        self.mode = 0

        self.ent_calibrate = None
        self.var = StringVar(self, value="mm")
        self.scale = None
        self.DX = 0

        self.pack()
        self.create_widgets()

    def calibrate(self):
        self.calibration = []
        print(self.scale)  #################################################################################
        if len(self.calibration) == 2:
            self.DX = self.scale/self.distance()
            print(self.DX)




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
            self.img_dim = [self.image_tk.width(), self.image_tk.height()]
            self.show_image()

    def show_image(self):
        self.win_init()

        self.canvas = Canvas(self.master, width=self.img_dim[0], height=self.img_dim[1], bg="white")

        # Draw the image on the canvas
        self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)
        self.canvas.place(x=0,y=0)

        # Bind the mouse click event to the canvas
        self.canvas.bind("<Button-1>", self.click_handler)

    def win_init(self):
        # remove all previous widgets
        self.clear()

        wid = self.img_dim[0]
        height = self.img_dim[1]
        # Display the image in a Tkinter window
        self.master.geometry("{}x{}".format(wid+150,height+75))

        btn_calibrate = Button(text="Calibrate",width=10,height=2, bg="white", fg="black", command=self.calibrate)
        btn_calibrate.place(x=wid,y=0)

        btn_generate = Button(text="Generate",width=10,height=2, bg="white", fg="black", justify="center")
        btn_generate.place(x=wid,y=50)

        btn_calculate = Button(text="Calculate",width=10,height=2, bg="white", fg="black", justify="center")
        btn_calculate.place(x=wid,y=100)

        self.ent_calibrate = Entry(bg="black",fg="white", width=10)
        self.ent_calibrate.place(x=0,y=height)

        btn_ok = Button(text="OK",width=2,height=2, command=self.ok)
        btn_ok.place(x=200,y=height)

        drop = OptionMenu(self.master, self.var, "mm", "um", "nm", "pm")
        drop.place(x=125,y=height)

    def ok(self):
        self.scale = self.magnitude()

    def magnitude(self):
        dist = 0
        if self.ent_calibrate.get():
            dist = int(self.ent_calibrate.get())
        v = self.var.get()

        if v == "mm":
            return dist/(10**3)
        elif v == "um":
            return dist/(10**6)
        elif v == "nm":
            return dist/(10**9)
        else:
            return dist/(10**12)




    def clear(self):
        # destroy all widgets that aren't master frame
        for widget in self.winfo_children():
            widget.destroy()

    # Define a function to handle mouse clicks
    def click_handler(self, event):
        # Get the coordinates of the mouse click
        x, y = event.x, event.y

        if self.mode == 0:
            # Draw a red dot at the clicked location
            if len(self.calibration) < 2:
                self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red")
                self.calibration.append((x,y))

            # Print the clicked coordinates
            print(self.calibration)


    def distance(self):
        c = self.calibration
        dx = c[0][0] - c[1][0]
        dy = c[1][0] - c[1][1]
        return math.sqrt(dx**2 + dy**2)



    def test_lbl(self):
        lbl_test = Label(self,text="working")
        lbl_test.pack()




root = Tk()
app = Application(master=root)
app.mainloop()
