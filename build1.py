from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageDraw, ImageTk
import math
from random import randint

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.canvas = None
        self.image_tk = None
        self.img_dim = None
        self.mode = 0

        self.calibration = [] # keep track of calibration coordinates
        self.ent_calibrate = None
        self.btn_calibrate = None
        self.btn_generate = None
        self.btn_calculate = None
        self.btn_ok = None
        self.drop = None
        self.var = StringVar(self, value="mm")
        self.DX = None

        self.pack()
        self.create_widgets()

    def calibrate(self):
        self.calibration = []
        self.mode = 1
        self.toggle_to("normal")
        self.canvas.delete("calibration")
        self.canvas.delete("line")
        notice1 = Label(text="click 2 points to calibrate", name="notice1").place(x=0,y=self.img_dim[1]+40)
        self.btn_generate.config(state="disabled")
        self.btn_calculate.config(state="disabled")

    def generate(self):
        self.mode = 2

        # define bounding box x/3 and y/3
        bx = self.img_dim[0] // 3
        by = self.img_dim[1] // 3

        # pick point in bound box
        p = (randint(bx,2*bx), randint(by,by*2))

        # random angle and opposite angle for bounding circle around point
        o1 = randint(0,360)*math.pi/180
        # 
        r = min([bx,by])
        e1x = p[0] + round(r*math.cos(o1))
        e1y = p[1] + round(r*math.sin(o1))
        e2x = p[0] - round(r*math.cos(o1))
        e2y = p[1] - round(r*math.sin(o1))

        # display new line and delete old line

        self.canvas.delete("line")
        self.canvas.create_line(e1x, e1y, e2x, e2y, fill="yellow", tags="line", width=2)
        dist = self.distance((e1x,e1y), (e2x,e2y))
        line_len = round(dist*self.DX*self.get_magnitude())
        print(str(line_len) + self.var.get())

        

    def toggle_to(self, to):
        self.ent_calibrate.config(state=to)
        self.btn_ok.config(state=to)
        self.drop.config(state=to)

        if len(self.calibration) != 2:
            self.btn_ok.config(state="disabled")



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

        # set dimensions of frame
        self.master.geometry("{}x{}".format(wid+150,height+75))

        # initialize buttons for UI
        self.btn_calibrate = Button(text="Calibrate",width=10,height=2, bg="white", fg="black", command=self.calibrate)
        self.btn_calibrate.place(x=wid,y=0)

        self.btn_generate = Button(text="Generate",width=10,height=2, bg="white", fg="black", command=self.generate)
        self.btn_generate.place(x=wid,y=50)

        self.btn_calculate = Button(text="Calculate",width=10,height=2, bg="white", fg="black", justify="center")
        self.btn_calculate.place(x=wid,y=100)

        self.ent_calibrate = Entry(bg="#D3D3D3",fg="black", insertbackground="black", width=10)
        self.ent_calibrate.place(x=0,y=height+10)

        self.btn_ok = Button(text="OK",width=2,height=2, command=self.ok)
        self.btn_ok.place(x=200,y=height+10)

        self.drop = OptionMenu(self.master, self.var, "mm", u'\u03BC'+"m", "nm", "pm")
        self.drop.place(x=125,y=height+10)

        # gray out buttons until calibration done
        self.toggle_to("disabled")
        self.btn_generate.config(state="disabled")
        self.btn_calculate.config(state="disabled")


    def ok(self):
        scale = self.magnitude()
        self.DX = scale/self.distance(self.calibration[0], self.calibration[1])
        self.toggle_to("disabled")
        self.btn_generate.config(state="normal")
        self.btn_calculate.config(state="normal")
        # self.delete('notice1')

    def magnitude(self):
        dist = 0
        if self.ent_calibrate.get():
            dist = int(self.ent_calibrate.get())
        return dist/self.get_magnitude()
        

    def get_magnitude(self):
        v = self.var.get()
        if v == "mm":
            return 10**3
        elif v == u'\u03BC'+"m":
            return 10**6
        elif v == "nm":
            return 10**9
        else:
            return 10**12




    def clear(self):
        # destroy all widgets that aren't master frame
        for widget in self.winfo_children():
            widget.destroy()

    # Define a function to handle mouse clicks
    def click_handler(self, event):
        # Get the coordinates of the mouse click
        x, y = event.x, event.y

        # if self.mode == 0:
        #     self.canvas.create_line(0,0, 100, 100, fill="yellow")

        if self.mode == 1:
            # Draw a red dot at the clicked location
            if len(self.calibration) < 2:
                self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red", tags="calibration")
                self.calibration.append((x,y))
                if len(self.calibration) == 2:
                    self.btn_ok.config(state="normal")


    def distance(self, p1, p2):
        dx = p1[0] - p2[0]
        dy = p1[1] - p2[1]
        return math.sqrt(dx**2 + dy**2)



    def test_lbl(self):
        lbl_test = Label(self,text="working")
        lbl_test.pack()




root = Tk()
app = Application(master=root)
app.mainloop()
