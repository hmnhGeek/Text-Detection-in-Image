from Tkinter import *
import ttk
from tkFileDialog import *
import pytesseract
from PIL import Image
import os

class Page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


# define pages here which inherit from page class. Below is an example page.
class HomePage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.config(background = "black")

        self.chos = Label(self, text = "No file chosen", bg = "black", fg = "white")
        self.chos.pack(pady = 60)
        
        self.choose = Button(self, text = "Choose File", command = self.choose_file, bd = 0, bg = 'white')
        self.choose.pack(pady = 40, padx = 10)

        self.sho = Button(self, text = "Show Text", command = self.show_results, bd = 0, bg = 'white')
        self.sho.pack(pady = 10, padx = 10)
        self.sho.config(state = "disabled")

    def choose_file(self):
        try:
            f = askopenfile()
            filename = f.name
            f.close()

            self.chos['text'] = filename
            os.remove('text.txt')

            txt = file('text.txt', 'w')
            txt.write(pytesseract.image_to_string(Image.open(filename)))
            txt.close()

            self.sho.config(state = "normal")

        except:
            pass

    def show_results(self):
        rp.update()
        rp.show()


class ResultPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.config(background = "black")
        self.scrollbar = Scrollbar(self)
        self.scrollbar.pack(side = RIGHT, fill = Y)
        self.area = Text(self, yscrollcommand = self.scrollbar.set, background = 'black', foreground = 'white'
                    , font = ('Courier New', 11), insertbackground = 'yellow', insertwidth = 5, selectbackground = 'red'
                    )
        
        self.area.pack(expand=True, fill='both')
        self.scrollbar.config(command = self.area.yview)

        self.back = Button(self, text = "Go Back", command = self.goback, bd = 0, bg = "white")
        self.back.pack(pady = 10)

    def update(self):
        with open('text.txt' , 'r') as f:
            text = f.read()

        self.area.config(state = "normal")
        self.area.delete('1.0', END)
        self.area.insert(END, text)
        self.area.config(state = "disabled")

    def goback(self):
        hp.show()

class MainView(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        '''
            Say if you defined a page class PageOne(). Initialise
            its object here. Like self.p1 = PageOne(self).

            self.container = Frame(self)
            self.container.pack(side = 'top', fill = 'both', expand = True)

            Then define the container here.
            self.p1.place(in_ = self.container, x = 0, y = 0, relwidth = 1, relheight = 1)

            Then show the page.
            self.p1.show()
        '''

        hp = HomePage(self)
        rp = ResultPage(self)

        global hp, rp        

        self.container = Frame(self)
        self.container.pack(side = 'top', fill = 'both', expand = True)

        hp.place(in_ = self.container, x = 0, y = 0, relwidth = 1, relheight = 1)
        rp.place(in_ = self.container, x = 0, y = 0, relwidth = 1, relheight = 1)
        
        hp.show()


def save_run():
    f = asksaveasfile()

    with open('text.txt', 'r') as fi:
        data = fi.read()

    f.write(data)
    f.close()

if __name__ == '__main__':
    root = Tk()

    main = MainView(root)
    main.pack(side = 'top', fill = 'both', expand = True)

    root.wm_geometry('500x500')
    
    root.resizable(height = 0, width = 0)

    root.title('Text Detector')

    menubar = Menu(root, bg = "white")
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Save", command=save_run)
    filemenu.add_command(label="Exit", command=root.destroy)
    
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)

    root.mainloop()
        
        
