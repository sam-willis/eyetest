from tkinter import *
from PIL import ImageTk
from ImageGenerator import ImageGenerator


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        self.master.title("GUI")
        self.pack(fill=BOTH, expand=1)

        menu = Menu(self.master)
        self.master.config(menu=menu)

        self.ig = ImageGenerator(width=1920, height=1120)
        #self.ig = ImageGenerator(width=1368, height=828)

        file = Menu(menu)
        file.add_command(label='Results', command=self.ig.print_results)
        file.add_command(label='Exit', command=self.client_exit)
        menu.add_cascade(label='File', menu=file)

        self.master.bind("<Key>", self.regResponce)

        self.PIL_image = self.ig.generate_char_image()
        self.render = ImageTk.PhotoImage(self.PIL_image)
        self.img = Label(self, image=self.render)

        self.img.pack(fill=BOTH, expand=YES)

    def showImg(self):
        self.PIL_image = self.ig.generate_char_image()
        self.render = ImageTk.PhotoImage(self.PIL_image)
        self.img.configure(image=self.render)

    def regResponce(self, event):
        self.ig.update(event.char)
        self.showImg()

    def client_exit(self):
        exit()


root = Tk()
root.geometry("400x300")
app = Window(root)

root.mainloop()
