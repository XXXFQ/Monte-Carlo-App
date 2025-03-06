import tkinter as tk

from .application import Application

def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

__all__ = [
    'main',
]