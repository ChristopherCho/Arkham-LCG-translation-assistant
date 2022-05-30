from tkinter import Tk

from gui import GUIApp

if __name__=="__main__":
    root = Tk()
    root.title("Image change")
    app = GUIApp(root)
    root.mainloop()