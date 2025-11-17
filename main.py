import tkinter as tk
from tkinter import messagebox
from app.ui.login import show_login
from app.db import get_connection  

#  HÀM KIỂM TRA KẾT NỐI SQL SERVER
def check_db_connection():
    """
    Kiểm tra kết nối tới SQL Server trước khi mở GUI.
    Trả về True nếu kết nối thành công, False nếu thất bại.
    """
    conn = get_connection()
    if conn:
        conn.close()
        return True
    else:
        messagebox.showerror(
            "Lỗi kết nối",
            "❌ Không thể kết nối tới SQL Server!\n"
            "Vui lòng kiểm tra cấu hình server trong file db.py."
        )
        return False

#  CHƯƠNG TRÌNH CHÍNH
def main():
    if not check_db_connection():
        return  # Dừng chương trình nếu không kết nối được

    root = tk.Tk()
    root.geometry("900x600")
    root.configure(bg="#eef5ff")
    show_login(root)
    root.mainloop()

# ============================================================
if __name__ == "__main__":
    main()
