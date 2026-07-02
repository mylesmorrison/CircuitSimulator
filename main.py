import tkinter as tk
from ui.gui import CircuitApp


def main():
    root = tk.Tk()
    CircuitApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()