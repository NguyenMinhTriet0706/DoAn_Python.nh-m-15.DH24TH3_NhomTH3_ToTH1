import tkinter as tk
from tkinter import ttk, messagebox

# ==========================
# TRANG CHỦ QUẢN LÝ KÝ TÚC XÁ
# ==========================
def show_home_page(root, username="Admin", role="Quản trị viên"):
    """Trang chủ sau khi đăng nhập thành công"""
    # Xóa giao diện cũ
    for widget in root.winfo_children():
        widget.destroy()

    # ====== CẤU HÌNH CỬA SỔ ======
    root.title("🏫 Trang chủ - Hệ thống Quản lý Ký túc xá")
    root.geometry("1100x700")
    root.configure(bg="#f0f4ff")

    # ====== HEADER ======
    header = tk.Frame(root, bg="#1e3a8a", height=90)
    header.pack(fill="x")
    tk.Label(
        header,
        text="HỆ THỐNG QUẢN LÝ KÝ TÚC XÁ",
        bg="#1e3a8a",
        fg="white",
        font=("Segoe UI", 22, "bold")
    ).pack(pady=20)
    tk.Label(
        header,
        text=f"Xin chào {username} ({role})",
        bg="#1e3a8a",
        fg="#cbd5e1",
        font=("Segoe UI", 12)
    ).pack()

    # ====== MAIN CONTAINER ======
    main = tk.Frame(root, bg="#f0f4ff", padx=20, pady=20)
    main.pack(expand=True, fill="both")

    # ====== STYLE ======
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Card.TButton",
        font=("Segoe UI", 13, "bold"),
        padding=20,
        relief="flat",
        background="#2563eb",
        foreground="white",
        borderwidth=0,
    )
    style.map(
        "Card.TButton",
        background=[("active", "#1e40af"), ("pressed", "#1e3a8a")],
        foreground=[("active", "white")]
    )

    style.configure(
        "Logout.TButton",
        font=("Segoe UI", 12, "bold"),
        padding=10,
        relief="flat",
        background="#dc2626",
        foreground="white",
        borderwidth=0,
    )
    style.map("Logout.TButton", background=[("active", "#b91c1c")])

    # ====== KHUNG CHỨC NĂNG ======
    features_frame = tk.Frame(main, bg="#f0f4ff")
    features_frame.pack(expand=True, pady=40)

    # Danh sách chức năng
    buttons = [
        ("👨‍🎓 Quản lý Sinh viên", "Theo dõi, thêm mới và cập nhật hồ sơ sinh viên", lambda: open_student_module(root)),
        ("👨‍🔧 Quản lý Nhân viên", "Quản lý thông tin và ca trực nhân viên", lambda: open_staff_module(root)),
        ("🏢 Quản lý Dịch vụ", "Xem, thêm, sửa thông tin các dịch vụ", lambda: open_service_module(root)),
        ("🚪 Quản lý Phòng", "Theo dõi số lượng, tình trạng, và phân bổ phòng", lambda: open_room_module(root)),
        ("💰 Quản lý Hóa đơn", "Tạo và theo dõi hóa đơn tiền phòng, điện nước", lambda: open_bill_module(root)),
        ("📑 Quản lý Thanh Toán", "Lưu trữ và theo dõi thanh toán", lambda: open_pay_module(root)),
    ]

    # ====== TẠO LƯỚI CÁC CARD ======
    for i, (title, desc, cmd) in enumerate(buttons):
        row, col = divmod(i, 3)

        card = tk.Frame(features_frame, bg="white", bd=0, relief="ridge")
        card.grid(row=row, column=col, padx=30, pady=25, ipadx=10, ipady=10)
        card.configure(highlightthickness=1, highlightbackground="#cbd5e1")

        ttk.Button(card, text=title, style="Card.TButton", command=cmd).pack(padx=10, pady=10)
        tk.Label(card, text=desc, bg="white", fg="#475569", font=("Segoe UI", 10)).pack(padx=15, pady=5)

    # Căn đều lưới
    for i in range(3):
        features_frame.grid_columnconfigure(i, weight=1)

    # ====== FOOTER ======
    footer = tk.Frame(root, bg="#1e3a8a", height=50)
    footer.pack(side="bottom", fill="x")
    ttk.Button(
        footer,
        text="🚪 Đăng xuất",
        style="Logout.TButton",
        command=lambda: go_back_to_login(root)
    ).pack(side="right", padx=20, pady=10)
    tk.Label(
        footer,
        text="© 2025 Ký túc xá Đại học An Giang | Phần mềm quản lý bởi Python & Tkinter",
        bg="#1e3a8a",
        fg="#cbd5e1",
        font=("Segoe UI", 10)
    ).pack(side="left", padx=20)


# ==========================
# HÀM MỞ MODULE CON
# ==========================
def open_student_module(root):
    try:
        from app.modules.students import show_student_management
        show_student_management(root)
    except ImportError:
        messagebox.showerror("Lỗi", "Không thể mở module Quản lý Sinh viên.")

        

def open_staff_module(root):
    try:
        from app.modules.staffs import show_staff_management
        show_staff_management(root)
    except ImportError as e:
        messagebox.showerror("Lỗi Import", f"Không thể mở module Quản lý Nhân viên.\n{e}")

def open_service_module(root):
    messagebox.showinfo("🏢 Quản lý Dịch vụ", "Mở giao diện Quản lý Dịch vụ!")

def open_room_module(root):
    messagebox.showinfo("🚪 Quản lý Phòng", "Mở giao diện Quản lý Phòng!")

def open_bill_module(root):
    messagebox.showinfo("💰 Quản lý Hóa đơn", "Mở giao diện Quản lý Hóa đơn!")

def open_pay_module(root):
    messagebox.showinfo("📑 Quản lý Thanh Toán", "Mở giao diện Quản lý Thanh Toán!")

def go_back_to_login(root):
    messagebox.showinfo("Đăng xuất", "Bạn chắc chắn muốn đăng xuất?")
    from app.ui.login import show_login; show_login(root)



