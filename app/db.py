import mysql.connector
from tkinter import *
from tkinter import messagebox

def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="triet070605",  # thay bằng password MySQL của bạn
            database="QUANLYKTX"
        )
        if conn.is_connected():
            messagebox.showinfo("Thành công", "Kết nối MySQL thành công!")
            return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi", f"Kết nối thất bại: {err}")
        return None

# Giao diện nhỏ kiểm tra kết nối
root = Tk()
root.title("Kết nối MySQL")
root.geometry("300x150")

btn = Button(root, text="Kết nối CSDL", command=connect_db)
btn.pack(pady=40)

root.mainloop()
