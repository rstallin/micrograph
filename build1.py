from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile, asksaveasfile
from PIL import Image, ImageDraw, ImageTk
import math
from random import randint
from openpyxl import Workbook, load_workbook
from datetime import datetime

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.canvas = None
        self.image_tk = None
        self.img_dim = None
        self.mode = 0
        self.pack()
        self.create_open_window()

        self.calibration = [] # keep track of calibration coordinates
        self.ent_calibrate = None
        self.btn_calibrate = None
        self.btn_generate = None
        self.btn_add = None
        self.btn_ok = None
        self.drop = None
        self.var = StringVar(self, value="mm")
        self.lbl_trials = None
        self.lbl_avg_d = None

        self.DX = None
        self.line_len = None 
        
        self.wb = None 
        self.wb_name = None
        
        self.data = []
        self.num_pts = 0



    def create_open_window(self):
        self.master.geometry("200x200+500+200")
        # create initial file select window
        self.label = Label(self, text="Click button to browse files")
        self.label.pack(pady=10)
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
        self.master.geometry("{}x{}+{}+{}".format(wid+175,height+75,100,50))

        # initialize widgets for UI
        self.btn_calibrate = Button(text="Calibrate",width=10,height=2, bg="white", fg="black", command=self.calibrate)
        self.btn_calibrate.place(x=wid,y=0)

        self.btn_generate = Button(text="Generate",width=10,height=2, bg="white", fg="black", command=self.generate)
        self.btn_generate.place(x=wid,y=50)

        self.ent_calibrate = Entry(bg="#D3D3D3",fg="black", insertbackground="black", width=10)
        self.ent_calibrate.place(x=0,y=height+10)

        self.drop = OptionMenu(self.master, self.var, "mm", u'\u03BC'+"m", "nm", "pm")
        self.drop.place(x=125,y=height+10)

        self.btn_ok = Button(text="OK",width=2,height=2, command=self.ok)
        self.btn_ok.place(x=200,y=height+10)

        self.btn_add = Button(text="Add",width=4,height=2,bg="white",fg="black", command=self.add)
        self.btn_add.place(x=wid,y=110)

        self.btn_export = Button(text="Export", width=4, height=2,bg="white",fg="black", command=self.export)
        self.btn_export.place(x=wid+70,y=110)

        self.lbl_trials = Label(text="Number of Trials: " + str(self.get_rows()))
        self.lbl_trials.place(x=wid+10,y=160)

        self.lbl_avg_d = Label(text="Avg Diameter: " + str(self.get_avg()) + " (" + self.var.get() + ")")
        self.lbl_avg_d.place(x=wid+10,y=180)

        # gray out buttons until calibration done
        self.toggle_to("disabled")
        self.btn_generate.config(state="disabled")
        self.btn_add.config(state="disabled")
        self.btn_export.config(state="disabled")



    def calibrate(self):
        self.mode = 1
        notice1 = Label(text="click 2 points to calibrate").place(x=0,y=self.img_dim[1]+40)

        # reset buttons and scale, delete shapes
        self.calibration = []
        self.data = []
        self.toggle_to("normal")
        self.btn_generate.config(state="disabled")
        self.btn_add.config(state="disabled")
        self.btn_export.config(state="disabled")

        self.canvas.delete("calibration")
        self.canvas.delete("line")
        self.canvas.delete("count")
        self.update_lbl()

    def generate(self):
        self.mode = 2

        # reset to 0
        self.num_pts = 0

        # define central bounding box x/3 and y/3 for center of line
        bx = self.img_dim[0] // 3
        by = self.img_dim[1] // 3

        # pick point in bound box
        p = (randint(bx,2*bx), randint(by,by*2))

        # random angle for bounding circle around point
        o1 = randint(0,360)*math.pi/180
        r = min([bx,by])

        # coords of ends of line
        e1x = p[0] + round(r*math.cos(o1))
        e1y = p[1] + round(r*math.sin(o1))
        e2x = p[0] - round(r*math.cos(o1))
        e2y = p[1] - round(r*math.sin(o1))

        # display new line and delete old line
        self.canvas.delete("count")
        self.canvas.delete("line")
        self.canvas.create_line(e1x, e1y, e2x, e2y, fill="yellow", tags="line", width=2)

        # store length of line (converted to scale)
        dist = self.distance((e1x,e1y), (e2x,e2y))
        self.line_len = round(dist*self.DX*self.get_magnitude())

        # add button is now usable
        self.btn_add.config(state="normal")

        self.update_lbl()

    def ok(self):
        scale = self.magnitude()
        self.DX = scale/self.distance(self.calibration[0], self.calibration[1])
        self.toggle_to("disabled")
        self.btn_generate.config(state="normal")
        self.canvas.delete("calibration")

        self.update_lbl()

    def add(self):
        self.data.append([None, self.line_len, self.num_pts, self.line_len/self.num_pts])
        self.generate()
        self.btn_export.config(state="normal")
        self.num_pts += 1

        self.update_lbl()

    def export(self):
        location = filedialog.asksaveasfilename()
        self.wb_name = str(location)+".xlsx"
        self.create_excel()
        ws = self.wb.active
        rows = len(self.data)
        for x in range(rows):
            d = self.data[x]
            d[0] = x+1
            ws.append(d)
        self.wb.save(self.wb_name)



    # Define a function to handle mouse clicks
    def click_handler(self, event):
        # Get the coordinates of the mouse click
        x, y = event.x, event.y

        if self.mode == 1:
            # Draw a red dot at the clicked location
            if len(self.calibration) < 2:
                self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red", tags="calibration")
                self.calibration.append((x,y))
                if len(self.calibration) == 2:
                    self.btn_ok.config(state="normal")
        if self.mode == 2:
            self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="red", tags="count")
            self.num_pts += 1
            self.btn_add.config(state="normal")

    def update_lbl(self):
        self.lbl_trials["text"] = "Number of Trials: " + str(self.get_rows())
        self.lbl_avg_d["text"] = "Avg Diameter: " + str(self.get_avg()) + " (" + self.var.get() + ")"

    def toggle_to(self, to):
        # toggle state of all elements connected to calibration
        self.ent_calibrate.config(state=to)
        self.btn_ok.config(state=to)
        self.drop.config(state=to)

        # not ok until 2 points selected for calibration
        if len(self.calibration) != 2:
            self.btn_ok.config(state="disabled")

    def clear(self):
        # destroy all widgets that aren't master frame
        for widget in self.winfo_children():
            widget.destroy()



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

    def distance(self, p1, p2):
        dx = p1[0] - p2[0]
        dy = p1[1] - p2[1]
        return math.sqrt(dx**2 + dy**2)

    def get_avg(self):
        avg = 0
        if self.get_rows() > 0:
            tot = 0
            for x in self.data:
                tot += x[3]
            avg = tot/self.get_rows()
        return round(avg,2)

    def get_rows(self):
        return len(self.data)

    def create_excel(self):
        self.wb = Workbook()
        ws = self.wb.active
        units = " (" + self.var.get() + ")"
        ws.append(["Trial #", "Line Length" + units, "# of Points", "Average Diameter" + units])
        self.wb.save(self.wb_name)



root = Tk()
root.title("FimageJ")
app = Application(master=root)
app.mainloop()
