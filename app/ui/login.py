import tkinter as tk
from tkinter import messagebox
import random
from app.ui.homepage import show_home_page


def show_login(root):
    """Hiển thị giao diện đăng nhập vào hệ thống Ký túc xá"""
    # Xóa mọi widget cũ (nếu có)
    for widget in root.winfo_children():
        widget.destroy()

    # === Cấu hình cửa sổ ===
    root.title("🔐 Đăng nhập hệ thống Quản lý Ký túc xá")
    root.geometry("420x600")
    root.configure(bg="#eef2ff")

    # === Khung đăng nhập ===
    frame = tk.Frame(root, bg="white", bd=1, relief="solid", padx=20, pady=25)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # === Tiêu đề ===
    tk.Label(frame, text="ĐĂNG NHẬP HỆ THỐNG", font=("Segoe UI", 16, "bold"),
             fg="#1e40af", bg="white").pack(pady=(0, 20))

    # === Nhập CMND/CCCD ===
    tk.Label(frame, text="CMND / CCCD:", font=("Segoe UI", 11), bg="white", anchor="w").pack(fill="x")
    entry_cmnd = tk.Entry(frame, font=("Segoe UI", 11))
    entry_cmnd.pack(fill="x", ipady=6, pady=(0, 10))

    # === Nhập mật khẩu ===
    tk.Label(frame, text="Mật khẩu:", font=("Segoe UI", 11), bg="white", anchor="w").pack(fill="x")
    entry_mk = tk.Entry(frame, font=("Segoe UI", 11), show="*")
    entry_mk.pack(fill="x", ipady=6, pady=(0, 5))

    # === Nút hiện/ẩn mật khẩu ===
    show_var = tk.BooleanVar(value=False)

    def toggle_password():
        entry_mk.config(show="" if show_var.get() else "*")

    tk.Checkbutton(frame, text="Hiện mật khẩu", variable=show_var,
                   bg="white", font=("Segoe UI", 9),
                   command=toggle_password).pack(anchor="w")

    # === Mã xác thực ===
    tk.Label(frame, text="Mã xác thực:", font=("Segoe UI", 11), bg="white", anchor="w").pack(fill="x", pady=(10, 0))
    ma_xac_thuc = tk.StringVar()

    lbl_ma = tk.Label(frame, text="", font=("Segoe UI", 14, "bold"),
                      bg="#1e3a8a", fg="white", width=12)
    lbl_ma.pack(pady=(5, 5))

    def tao_ma():
        ma = str(random.randint(10000, 99999))
        ma_xac_thuc.set(ma)
        lbl_ma.config(text=ma)

    tao_ma()  # tạo mã ban đầu

    # Ô nhập mã
    entry_ma = tk.Entry(frame, font=("Segoe UI", 11))
    entry_ma.pack(fill="x", ipady=6, pady=(5, 5))

    # Nút làm mới mã
    tk.Button(frame, text="↻ Làm mới mã", font=("Segoe UI", 10, "bold"),
              bg="#e0e7ff", relief="flat", command=tao_ma).pack(pady=(0, 10))

    # === Xử lý đăng nhập ===
    def dang_nhap():
        cmnd = entry_cmnd.get().strip()
        mk = entry_mk.get().strip()
        ma_nhap = entry_ma.get().strip()

        if not cmnd or not mk or not ma_nhap:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin!")
            return

        if ma_nhap != ma_xac_thuc.get():
            messagebox.showerror("Sai mã xác thực", "Mã xác thực không đúng!")
            tao_ma()
            entry_ma.delete(0, tk.END)
            return

        # ==== Kiểm tra tài khoản (tạm thời giả lập) ====
        if cmnd == "123456789" and mk == "admin":
            messagebox.showinfo("Thành công", f"Chào mừng Nguyễn Minh Triết quay lại hệ thống!")
            show_home_page(root, username="Admin", role="Quản trị viên")
        else:
            messagebox.showerror("Đăng nhập thất bại", "Sai CMND/CCCD hoặc mật khẩu!")

    # === Nút đăng nhập ===
    tk.Button(frame, text="🔑 Đăng nhập", font=("Segoe UI", 12, "bold"),
              bg="#1e40af", fg="white", relief="flat",
              command=dang_nhap).pack(fill="x", pady=(15, 5), ipady=5)

    # === Nút quên mật khẩu ===
    tk.Button(frame, text="Quên mật khẩu", font=("Segoe UI", 10),
              bg="#dbeafe", fg="#1e3a8a", relief="flat",
              command=lambda: messagebox.showinfo("Quên mật khẩu", "Liên hệ quản trị viên để được cấp lại tài khoản.")).pack(
        fill="x", ipady=4, pady=(5, 0))

    # === Footer ===
    tk.Label(frame, text="© 2025 Hệ thống Quản lý Ký túc xá Đại học An Giang",
             bg="white", fg="#9ca3af", font=("Segoe UI", 9)).pack(pady=10)
