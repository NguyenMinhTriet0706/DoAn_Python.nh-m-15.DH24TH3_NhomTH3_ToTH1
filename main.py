import tkinter as tk
from app.ui.login import show_login

def main():
    root = tk.Tk()
    root.geometry("900x600")
    root.configure(bg="#eef5ff")
    show_login(root)
    root.mainloop()

if __name__ == "__main__":
    main()
