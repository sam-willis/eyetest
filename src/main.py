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

        self.ig = ImageGenerator()

        file = Menu(menu)
        file.add_command(label='Results', command=self.ig.print_results)
        file.add_command(label='Exit', command=self.client_exit)
        menu.add_cascade(label='File', menu=file)

        self.master.bind("<Key>", self.regResponce)

        self.PIL_image = self.ig.generate_char_image()
        self.render = ImageTk.PhotoImage(self.PIL_image)
        self.img = Label(self, image=self.render)

        self.img.pack(fill=BOTH, expand=YES)
        self.img.bind('<Configure>', self._resize_image)

    def _resize_image(self, event):
        new_width = event.width
        new_height = event.height
        resized_PIL_image = self.PIL_image.resize((new_width, new_height))
        self.render = ImageTk.PhotoImage(resized_PIL_image)
        self.img.configure(image=self.render)

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
