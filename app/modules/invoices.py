# app/ui/invoice_ui.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date
from app.db import fetch_all, execute_non_query
import os

# BIẾN TOÀN CỤC
entries = {}
tree = None
add_btn = update_btn = delete_btn = print_btn = None
search_entry = None
master_data_list = []

FIELD_KEYS = [
    "ma_hd", "ma_sv", "ma_phong", "ngay_lap", "thang", "nam", "tong_tien",
    "trang_thai", "phuong_thuc_tt", "ngay_thanh_toan", "ghi_chu"
]

FIELD_LABELS = [
    "Mã HD:", "Mã SV:", "Mã Phòng:", "Ngày lập:", "Tháng:", "Năm:", "Tổng tiền:",
    "Trạng thái:", "Phương thức TT:", "Ngày thanh toán:", "Ghi chú:"
]
# ===============================
def show_invoice_management(root):
    global entries, tree, add_btn, update_btn, delete_btn, print_btn, search_entry, master_data_list
    entries = {}
    master_data_list = []

    # Xóa nội dung root cũ
    for widget in root.winfo_children():
        widget.destroy()

    root.title("🧾 Quản lý Hóa Đơn - Ký túc xá")
    root.geometry("1350x700")
    root.configure(bg="#f0f4ff")

    #  STYLE 
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#f0f4ff")
    style.configure("TLabel", background="white", font=("Segoe UI", 11))
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
    tk.Label(header, text="🧾 QUẢN LÝ HÓA ĐƠN", bg="#1e3a8a", fg="white",
             font=("Segoe UI", 20, "bold")).pack(side="left", padx=30)
    ttk.Button(header, text="⬅ Quay lại Trang chủ", command=lambda: go_back_to_home(root),
               style="Back.TButton").pack(side="right", padx=20, pady=10)

    # ===== MAIN LAYOUT =====
    main_frame = tk.Frame(root, bg="#f0f4ff")
    main_frame.pack(fill="both", expand=True, padx=20, pady=15)

    #  LEFT PANEL (FORM) 
    left_frame = tk.Frame(main_frame, bg="white", bd=2, relief="groove")
    left_frame.pack(side="left", fill="y", padx=(0, 15), pady=5)
    left_frame.pack_propagate(False)
    left_frame.configure(width=450)

    tk.Label(left_frame, text="📋 Thông tin Hóa Đơn", font=("Segoe UI", 14, "bold"),
             bg="white", fg="#1e3a8a").pack(pady=10)

    form_frame = tk.Frame(left_frame, bg="white")
    form_frame.pack(fill="both", expand=True, padx=10, pady=5)
    create_invoice_form(form_frame)

    #  BUTTON FRAME 
    btn_frame = tk.Frame(left_frame, bg="white")
    btn_frame.pack(side="bottom", pady=10, padx=15, fill="x")
    btn_frame.grid_columnconfigure((0, 1), weight=1)

    global add_btn, update_btn, delete_btn, print_btn
    add_btn = ttk.Button(btn_frame, text="➕ Thêm", style="Primary.TButton", command=add_invoice)
    add_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    update_btn = ttk.Button(btn_frame, text="✎ Cập nhật", style="Primary.TButton", command=update_invoice,
                            state="disabled")
    update_btn.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    delete_btn = ttk.Button(btn_frame, text="🗑️ Xóa", style="Danger.TButton", command=delete_invoice,
                            state="disabled")
    delete_btn.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
    print_btn = ttk.Button(btn_frame, text="🖨️ In Hóa Đơn", style="Secondary.TButton", command=print_invoice,
                           state="disabled")
    print_btn.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    ttk.Button(btn_frame, text="↻ Làm mới", style="Secondary.TButton", command=clear_form).grid(row=2, column=0,
                                                                                               columnspan=2,
                                                                                               padx=5, pady=5,
                                                                                               sticky="ew")
    save_btn = ttk.Button(btn_frame, text="💾 Lưu TXT", style="Secondary.TButton", command=save_invoices_to_txt)
    save_btn.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    #  RIGHT PANEL (TREE) 
    right_frame = tk.Frame(main_frame, bg="white", bd=2, relief="groove")
    right_frame.pack(side="right", fill="both", expand=True, pady=5)

    tk.Label(right_frame, text="📑 Danh sách Hóa Đơn", bg="white", font=("Segoe UI", 14, "bold"),
             fg="#1e3a8a").pack(anchor="w", padx=15, pady=(10, 5))

    search_frame = tk.Frame(right_frame, bg="white")
    search_frame.pack(fill="x", padx=15, pady=5)
    global search_entry
    search_entry = ttk.Entry(search_frame, width=35)
    search_entry.pack(side="left", padx=5)
    ttk.Button(search_frame, text="🔍 Tìm kiếm", style="Primary.TButton", command=search_invoice).pack(side="left",
                                                                                                      padx=5)
    search_entry.bind("<Return>", lambda e: search_invoice())

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

    populate_data_from_db()


#  FORM 
def create_invoice_form(frame):
    global entries
    for i, (label, key) in enumerate(zip(FIELD_LABELS, FIELD_KEYS)):
        tk.Label(frame, text=label, bg="white", anchor="w").grid(row=i, column=0, sticky="w", padx=5, pady=3)
        if key == "trang_thai":
            entry = ttk.Combobox(frame, values=["Chưa thanh toán", "Đang xử lý", "Đã thanh toán"], state="readonly")
        elif key == "phuong_thuc_tt":
            entry = ttk.Combobox(frame, values=["Tiền mặt", "Chuyển khoản"], state="readonly")
        elif key in ["ngay_lap", "ngay_thanh_toan"]:
            entry = DateEntry(frame, width=18, background='darkblue', foreground='white', borderwidth=2,
                              year=date.today().year)
        else:
            entry = ttk.Entry(frame)
        entry.grid(row=i, column=1, sticky="w", padx=5, pady=3)
        entries[key] = entry

#  CÁC HÀM CRUD 
def get_form_data():
    result = []
    for k in FIELD_KEYS:
        if k in ["ngay_lap", "ngay_thanh_toan"]:
            val = entries[k].get()
            if val == "":
                result.append(None)
            else:
                result.append(entries[k].get_date().strftime("%Y-%m-%d"))
        else:
            result.append(entries[k].get().strip())
    return tuple(result)


def clear_form():
    for k in FIELD_KEYS:
        if k in entries:
            if k in ["trang_thai", "phuong_thuc_tt"]:
                entries[k].set("")
            elif k in ["ngay_lap", "ngay_thanh_toan"]:
                entries[k].set_date(date.today())
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
        if k in ["trang_thai", "phuong_thuc_tt"]:
            entries[k].set(values[i])
        elif k in ["ngay_lap", "ngay_thanh_toan"]:
            if values[i]:
                y, m, d = map(int, values[i].split('-'))
                entries[k].set_date(date(y, m, d))
        else:
            entries[k].delete(0, "end")
            entries[k].insert(0, values[i])
    add_btn.config(state="disabled")
    update_btn.config(state="normal")
    delete_btn.config(state="normal")
    print_btn.config(state="normal")


def add_invoice():
    data = get_form_data()
    if not data[0] or not data[1]:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập Mã HD và Mã SV")
        return
    query = """
    INSERT INTO hoadon (ma_hd, ma_sv, ma_phong, ngay_lap, thang, nam, tong_tien, trang_thai, phuong_thuc_tt, ngay_thanh_toan, ghi_chu)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    try:
        execute_non_query(query, data)
        messagebox.showinfo("Thành công", f"Đã thêm Hóa Đơn {data[0]}")
        populate_data_from_db()
        clear_form()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi thêm: {e}")


def update_invoice():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn hóa đơn để cập nhật.")
        return
    data = get_form_data()
    query = """
    UPDATE hoadon
    SET ma_sv=?, ma_phong=?, ngay_lap=?, thang=?, nam=?, tong_tien=?, trang_thai=?, phuong_thuc_tt=?, ngay_thanh_toan=?, ghi_chu=?
    WHERE ma_hd=?
    """
    try:
        execute_non_query(query, data[1:] + (data[0],))
        messagebox.showinfo("Thành công", f"Đã cập nhật Hóa Đơn {data[0]}")
        populate_data_from_db()
        clear_form()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi cập nhật: {e}")


def delete_invoice():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn hóa đơn để xóa.")
        return
    confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa hóa đơn này không?")
    if not confirm:
        return
    index = tree.index(selected[0])
    ma_hd = master_data_list[index][0]
    query = "DELETE FROM hoadon WHERE ma_hd=?"
    try:
        execute_non_query(query, (ma_hd,))
        messagebox.showinfo("Thành công", f"Đã xóa Hóa Đơn {ma_hd}")
        populate_data_from_db()
        clear_form()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi xóa: {e}")


def search_invoice():
    term = search_entry.get().lower()
    tree.delete(*tree.get_children())
    for row in master_data_list:
        if term in str(row).lower():
            tree.insert("", "end", values=row)


def populate_data_from_db():
    global master_data_list
    query = """
    SELECT ma_hd, ma_sv, ma_phong, CONVERT(varchar, ngay_lap, 23), thang, nam, tong_tien,
           trang_thai, phuong_thuc_tt, CONVERT(varchar, ngay_thanh_toan, 23), ghi_chu
    FROM hoadon
    """
    try:
        raw_data = fetch_all(query)
        master_data_list = [tuple(str(v) if v is not None else "" for v in row) for row in raw_data]
        refresh_tree()
    except Exception as e:
        messagebox.showerror("Lỗi DB", f"Không tải dữ liệu:\n{e}")


# IN & LƯU TXT
def print_invoice():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn hóa đơn để in.")
        return
    index = tree.index(selected[0])
    data = master_data_list[index]
    info = f"""
🧾 Mã HD: {data[0]}
👤 Mã SV: {data[1]}
🏢 Mã Phòng: {data[2]}
📅 Ngày lập: {data[3]}
💸 Tổng tiền: {data[6]}
📌 Trạng thái: {data[7]}
💳 Phương thức TT: {data[8]}
📅 Ngày thanh toán: {data[9]}
📝 Ghi chú: {data[10]}
"""
    messagebox.showinfo("🖨️ Thông tin Hóa Đơn", info)


def save_invoices_to_txt():
    if not master_data_list:
        messagebox.showwarning("Chưa có dữ liệu", "Không có hóa đơn nào để lưu.")
        return
    filename = "hoadon.txt"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for data in master_data_list:
                f.write(" | ".join(str(x) for x in data) + "\n")
        messagebox.showinfo("Thành công", f"Đã lưu {len(master_data_list)} hóa đơn vào file {os.path.abspath(filename)}")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không lưu được file: {e}")


def go_back_to_home(root):
    from app.ui.homepage import show_home_page
    show_home_page(root)
