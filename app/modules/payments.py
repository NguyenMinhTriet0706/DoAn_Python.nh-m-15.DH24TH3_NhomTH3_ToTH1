import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date
from app.db import fetch_all, execute_non_query
import os

#  BIẾN TOÀN CỤC
entries = {}
tree = None
add_btn, update_btn, delete_btn, print_btn = None, None, None, None
search_entry = None
master_data_list = []

FIELD_KEYS = ["ma_tt", "ma_hd", "ma_dv", "so_luong", "don_gia",
              "thang", "nam", "ngay_tt", "trang_thai", "nguoi_thuc_hien", "ghi_chu", "thanh_tien"]
FIELD_LABELS = ["Mã TT:", "Mã Hóa Đơn:", "Mã Dịch vụ:", "Số lượng:", "Đơn giá:",
                "Tháng:", "Năm:", "Ngày TT:", "Trạng thái:", "Người thực hiện:", "Ghi chú:", "Thành tiền:"]

#  SHOW MODULE 
def show_payment_management(root):
    global entries, tree, add_btn, update_btn, delete_btn, print_btn, search_entry, master_data_list
    entries = {}
    master_data_list = []

    # Xóa nội dung root cũ
    for widget in root.winfo_children():
        widget.destroy()

    root.title("💵 Quản lý Thanh Toán - Ký túc xá")
    root.geometry("1350x700")
    root.configure(bg="#f0f4ff")

    #  STYLE 
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#f0f4ff")
    style.configure("White.TFrame", background="white")
    style.configure("TLabel", background="white", font=("Segoe UI", 11))
    style.configure("Title.TLabel", background="white", font=("Segoe UI", 14, "bold"), foreground="#1e3a8a")
    style.configure("TEntry", padding=5, font=("Segoe UI", 11))
    btn_padding = (10, 7)
    style.configure("Primary.TButton", font=("Segoe UI", 11, "bold"), padding=btn_padding,
                    background="#0ea5e9", foreground="white")
    style.map("Primary.TButton", background=[("active", "#0284c7"), ("disabled", "#9ca3af")])
    style.configure("Danger.TButton", font=("Segoe UI", 11, "bold"), padding=btn_padding,
                    background="#e11d48", foreground="white")
    style.map("Danger.TButton", background=[("active", "#be123c"), ("disabled", "#9ca3af")])
    style.configure("Secondary.TButton", font=("Segoe UI", 11, "bold"), padding=btn_padding,
                    background="#6b7280", foreground="white")
    style.map("Secondary.TButton", background=[("active", "#4b5563")])
    style.configure("Back.TButton", font=("Segoe UI", 11, "bold"), padding=(10, 8),
                    background="#1e3a8a", foreground="white")
    style.map("Back.TButton", background=[("active", "#2563eb")])

    #  HEADER 
    header = tk.Frame(root, bg="#1e3a8a", height=70)
    header.pack(fill="x", side="top")
    header.pack_propagate(False)
    tk.Label(header, text="💵 QUẢN LÝ THANH TOÁN", bg="#1e3a8a", fg="white",
             font=("Segoe UI", 20, "bold")).pack(side="left", padx=30)
    ttk.Button(header, text="⬅ Quay lại Trang chủ", command=lambda: go_back_to_home(root),
               style="Back.TButton").pack(side="right", padx=20, pady=10)

    #  MAIN LAYOUT 
    main_frame = tk.Frame(root, bg="#f0f4ff")
    main_frame.pack(fill="both", expand=True, padx=20, pady=15)

    #  LEFT PANEL (FORM) 
    left_frame = tk.Frame(main_frame, bg="white", bd=2, relief="groove")
    left_frame.pack(side="left", fill="y", padx=(0, 15), pady=5)
    left_frame.pack_propagate(False)
    left_frame.configure(width=450)

    tk.Label(left_frame, text="📋 Thông tin Thanh Toán", font=("Segoe UI", 14, "bold"),
             bg="white", fg="#1e3a8a").pack(pady=10)

    form_frame = tk.Frame(left_frame, bg="white")
    form_frame.pack(fill="both", expand=True, padx=10, pady=5)
    create_payment_form(form_frame)

    #  BUTTON FRAME 
    btn_frame = tk.Frame(left_frame, bg="white")
    btn_frame.pack(side="bottom", pady=10, padx=15, fill="x")
    btn_frame.grid_columnconfigure((0, 1), weight=1)

    global add_btn, update_btn, delete_btn, print_btn
    add_btn = ttk.Button(btn_frame, text="➕ Thêm", style="Primary.TButton", command=add_payment)
    add_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    update_btn = ttk.Button(btn_frame, text="✎ Cập nhật", style="Primary.TButton", command=update_payment,
                            state="disabled")
    update_btn.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    delete_btn = ttk.Button(btn_frame, text="🗑️ Xóa", style="Danger.TButton", command=delete_payment,
                            state="disabled")
    delete_btn.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
    print_btn = ttk.Button(btn_frame, text="🖨️ In Thanh Toán", style="Secondary.TButton", command=print_payment,
                           state="disabled")
    print_btn.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    ttk.Button(btn_frame, text="↻ Làm mới", style="Secondary.TButton", command=clear_form).grid(row=2, column=0,
                                                                                               columnspan=2,
                                                                                               padx=5, pady=5,
                                                                                               sticky="ew")
    save_btn = ttk.Button(btn_frame, text="💾 Lưu TXT", style="Secondary.TButton", command=save_payments_to_txt)
    save_btn.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    #  RIGHT PANEL (TREE) 
    right_frame = tk.Frame(main_frame, bg="white", bd=2, relief="groove")
    right_frame.pack(side="right", fill="both", expand=True, pady=5)

    tk.Label(right_frame, text="📑 Danh sách Thanh Toán", bg="white", font=("Segoe UI", 14, "bold"),
             fg="#1e3a8a").pack(anchor="w", padx=15, pady=(10, 5))

    search_frame = tk.Frame(right_frame, bg="white")
    search_frame.pack(fill="x", padx=15, pady=5)
    global search_entry
    search_entry = ttk.Entry(search_frame, width=35)
    search_entry.pack(side="left", padx=5)
    ttk.Button(search_frame, text="🔍 Tìm kiếm", style="Primary.TButton", command=search_payment).pack(side="left",
                                                                                                      padx=5)
    search_entry.bind("<Return>", lambda e: search_payment())

    tree_container = tk.Frame(right_frame, bg="white")
    tree_container.pack(fill="both", expand=True, padx=10, pady=10)
    tree_scroll_y = ttk.Scrollbar(tree_container, orient="vertical")
    tree_scroll_y.pack(side="right", fill="y")
    tree_scroll_x = ttk.Scrollbar(tree_container, orient="horizontal")
    tree_scroll_x.pack(side="bottom", fill="x")

    global tree
    tree = ttk.Treeview(tree_container, columns=FIELD_KEYS, show="headings",
                        yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set, height=20)
    for key, label in zip(FIELD_KEYS, FIELD_LABELS):
        tree.heading(key, text=label.replace(":", ""))
        tree.column(key, width=120, anchor="center")
    tree.pack(fill="both", expand=True)
    tree_scroll_y.config(command=tree.yview)
    tree_scroll_x.config(command=tree.xview)
    tree.bind("<<TreeviewSelect>>", on_tree_select)

    # Lấy dữ liệu từ database
    populate_data_from_db()

#  TẠO FORM
def create_payment_form(frame):
    global entries
    for i, (label, key) in enumerate(zip(FIELD_LABELS, FIELD_KEYS)):
        tk.Label(frame, text=label, bg="white", anchor="w").grid(row=i, column=0, sticky="w", padx=5, pady=3)
        if key == "trang_thai":
            entry = ttk.Combobox(frame, values=["Chưa xác nhận", "Đang xử lý", "Đã xác nhận"], state="readonly")
        elif key == "ngay_tt":
            entry = DateEntry(frame, width=18, background='darkblue', foreground='white', borderwidth=2,
                              year=date.today().year)
        elif key == "thanh_tien":
            entry = ttk.Entry(frame, state="readonly")
        else:
            entry = ttk.Entry(frame)
        entry.grid(row=i, column=1, sticky="w", padx=5, pady=3)
        entries[key] = entry

#  CÁC HÀM CRUD 
def get_form_data():
    result = []
    for k in FIELD_KEYS:
        if k == "ngay_tt":
            result.append(entries[k].get_date().strftime("%Y-%m-%d"))
        elif k == "thanh_tien":
            continue  
        else:
            result.append(entries[k].get().strip())
    return tuple(result)

def clear_form():
    for k in FIELD_KEYS:
        if k in entries:
            if k == "trang_thai":
                entries[k].set("")
            elif k == "ngay_tt":
                entries[k].set_date(date.today())
            elif k == "thanh_tien":
                entries[k].config(state="normal")
                entries[k].delete(0, "end")
                entries[k].config(state="readonly")
            else:
                entries[k].delete(0, "end")
    if add_btn: add_btn.config(state="normal")
    if update_btn: update_btn.config(state="disabled")
    if delete_btn: delete_btn.config(state="disabled")
    if print_btn: print_btn.config(state="disabled")
    if tree.selection():
        tree.selection_remove(tree.selection()[0])

def refresh_tree():
    tree.delete(*tree.get_children())
    for row in master_data_list:
        tree.insert("", "end", values=row)

def on_tree_select(event):
    selected = tree.selection()
    if not selected:
        return
    values = tree.item(selected[0], "values")
    for i, k in enumerate(FIELD_KEYS):
        if k == "trang_thai":
            entries[k].set(values[i])
        elif k == "ngay_tt":
            y, m, d = map(int, values[i].split('-'))
            entries[k].set_date(date(y, m, d))
        elif k == "thanh_tien":
            entries[k].config(state="normal")
            entries[k].delete(0, "end")
            entries[k].insert(0, values[i])
            entries[k].config(state="readonly")
        else:
            entries[k].delete(0, "end")
            entries[k].insert(0, values[i])
    add_btn.config(state="disabled")
    update_btn.config(state="normal")
    delete_btn.config(state="normal")
    print_btn.config(state="normal")

# Thêm thanh toán
def add_payment():
    data = get_form_data()
    if not data[0] or not data[1]:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập Mã TT và Mã Hóa Đơn")
        return
    query = """
    INSERT INTO thanhtoan (ma_tt, ma_hd, ma_dv, so_luong, don_gia, thang, nam, ngay_tt, trang_thai, nguoi_thuc_hien, ghi_chu)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    try:
        execute_non_query(query, data)
        messagebox.showinfo("Thành công", f"Đã thêm Thanh Toán {data[0]}")
        populate_data_from_db()
        clear_form()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi thêm: {e}")

# Cập nhật thanh toán
def update_payment():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn thanh toán để cập nhật.")
        return
    data = get_form_data()
    query = """
    UPDATE thanhtoan
    SET ma_hd=?, ma_dv=?, so_luong=?, don_gia=?, thang=?, nam=?, ngay_tt=?, trang_thai=?, nguoi_thuc_hien=?, ghi_chu=?
    WHERE ma_tt=?
    """
    try:
        execute_non_query(query, data[1:] + (data[0],))
        messagebox.showinfo("Thành công", f"Đã cập nhật Thanh Toán {data[0]}")
        populate_data_from_db()
        clear_form()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi cập nhật: {e}")

# Xóa thanh toán
def delete_payment():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn thanh toán để xóa.")
        return
    confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa thanh toán này không?")
    if not confirm:
        return
    index = tree.index(selected[0])
    ma_tt = master_data_list[index][0]
    query = "DELETE FROM thanhtoan WHERE ma_tt=?"
    try:
        execute_non_query(query, (ma_tt,))
        messagebox.showinfo("Thành công", f"Đã xóa Thanh Toán {ma_tt}")
        populate_data_from_db()
        clear_form()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi xóa: {e}")

def search_payment():
    term = search_entry.get().lower()
    tree.delete(*tree.get_children())
    for row in master_data_list:
        if term in str(row).lower():
            tree.insert("", "end", values=row)

def populate_data_from_db():
    global master_data_list
    query = """
    SELECT ma_tt, ma_hd, ma_dv, so_luong, don_gia, thang, nam,
           CONVERT(varchar, ngay_tt, 23), trang_thai, nguoi_thuc_hien, ghi_chu,
           thanh_tien
    FROM thanhtoan
    """
    try:
        raw_data = fetch_all(query)
        master_data_list = [
            tuple(str(v) if v is not None else "" for v in row)
            for row in raw_data
        ]
        refresh_tree()
    except Exception as e:
        messagebox.showerror("Lỗi DB", f"Không tải dữ liệu:\n{e}")

# IN & LƯU TXT
def print_payment():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn thanh toán để in.")
        return
    index = tree.index(selected[0])
    data = master_data_list[index]
    info = f"""
🧾 Mã TT: {data[0]}
💳 Mã Hóa Đơn: {data[1]}
🏢 Mã Dịch vụ: {data[2]}
📦 Số lượng: {data[3]}
💰 Đơn giá: {data[4]}
💸 Thành tiền: {data[11]}
🗓️ Tháng/Năm: {data[5]}/{data[6]}
📅 Ngày TT: {data[7]}
📌 Trạng thái: {data[8]}
👤 Người thực hiện: {data[9]}
📝 Ghi chú: {data[10]}
"""
    messagebox.showinfo("🖨️ Thông tin Thanh Toán", info)

def save_payments_to_txt():
    if not master_data_list:
        messagebox.showwarning("Chưa có dữ liệu", "Không có thanh toán nào để lưu.")
        return
    filename = "thanhtoan.txt"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for data in master_data_list:
                line = " | ".join(str(x) for x in data)
                f.write(line + "\n")
        messagebox.showinfo("Thành công", f"Đã lưu {len(master_data_list)} thanh toán vào file {os.path.abspath(filename)}")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không lưu được file: {e}")


def go_back_to_home(root):
    from app.ui.homepage import show_home_page
    show_home_page(root)  
