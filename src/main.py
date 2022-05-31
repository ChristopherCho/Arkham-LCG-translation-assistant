from tkinter import Tk
from argparse import ArgumentParser

from gui import GUIApp

if __name__=="__main__":
    parser = ArgumentParser()
    parser.add_argument("--chromedriver", type=str, default='data/chromedriver_windows.exe', help="Path to chromedriver")
    parser.add_argument("--image_scale", type=float, default=2.5, help="Ratio to scale up/down image from original (300 * 420)")
    parser.add_argument("--save_original_size", action="store_true", help="Whether to save image in original size (300 * 420)")

    args = parser.parse_args()

    root = Tk()
    root.title("Image change")
    app = GUIApp(root, args)
    root.mainloop()