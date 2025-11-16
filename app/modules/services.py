import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date
from app.db import fetch_all, fetch_one, execute_non_query  

#   BIẾN TOÀN CỤC
entries = {}
tree = None
add_btn, update_btn, delete_btn = None, None, None
search_entry = None
master_data_list = []

FIELD_GROUPS = {
    "tab1": {
        "labels": ["Mã Dịch vụ:", "Tên Dịch vụ:", "Loại dịch vụ:"],
        "keys": ["ma_dv", "ten_dv", "loai_dv"]
    },
    "tab2": {
        "labels": ["Đơn vị:", "Đơn giá:", "Ngày áp dụng:"],
        "keys": ["don_vi", "don_gia", "ngay_ap_dung"]
    },
    "tab3": {
        "labels": ["Trạng thái:", "Mô tả:"],
        "keys": ["trang_thai", "mo_ta"]
    }
}

ALL_FIELD_KEYS = FIELD_GROUPS["tab1"]["keys"] + FIELD_GROUPS["tab2"]["keys"] + FIELD_GROUPS["tab3"]["keys"]
  
#   HIỂN THỊ MODULE QUẢN LÝ DỊCH VỤ  
def show_service_management(root):
    global entries, tree, add_btn, update_btn, delete_btn, search_entry, master_data_list
    entries = {}
    master_data_list = []

    for widget in root.winfo_children():
        widget.destroy()

    root.title("🏢 Quản lý Dịch vụ - Ký túc xá")
    root.geometry("1300x700")
    root.configure(bg="#e0f2fe")

    #  STYLE 
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#e0f2fe")
    style.configure("White.TFrame", background="white")
    style.configure("TLabel", background="white", font=("Segoe UI", 11))
    style.configure("Title.TLabel", background="white", font=("Segoe UI", 14, "bold"), foreground="#1e3a8a")
    style.configure("TEntry", padding=5, font=("Segoe UI", 11))
    style.configure("TCombobox", padding=5, font=("Segoe UI", 11))
    style.map("TCombobox", selectbackground=[("readonly", "#dbeafe")], selectforeground=[("readonly", "black")])
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
    header = tk.Frame(root, bg="#1e40af", height=70)
    header.pack(fill="x", side="top")
    header.pack_propagate(False)
    tk.Label(header, text="🏢 QUẢN LÝ DỊCH VỤ", bg="#1e40af", fg="white",
             font=("Segoe UI", 20, "bold")).pack(side="left", padx=30)
    ttk.Button(header, text="⬅ Quay lại Trang chủ", command=lambda: go_back_to_home(root),
               style="Back.TButton").pack(side="right", padx=20, pady=10)

    #  MAIN LAYOUT 
    main_frame = tk.Frame(root, bg="#e0f2fe")
    main_frame.pack(fill="both", expand=True, padx=20, pady=15)

    #  LEFT PANEL 
    left_frame = tk.Frame(main_frame, bg="white", bd=2, relief="groove")
    left_frame.pack(side="left", fill="y", padx=(0, 15), pady=5)
    left_frame.pack_propagate(False)
    left_frame.configure(width=450)

    tk.Label(left_frame, text="📋 Thông tin Dịch vụ", font=("Segoe UI", 14, "bold"), bg="white", fg="#1e3a8a").pack(pady=10)

    notebook = ttk.Notebook(left_frame)
    notebook.pack(fill="both", expand=True, padx=10, pady=5)

    tab1 = ttk.Frame(notebook, style="White.TFrame")
    tab2 = ttk.Frame(notebook, style="White.TFrame")
    tab3 = ttk.Frame(notebook, style="White.TFrame")
    notebook.add(tab1, text=" 📝 Cơ bản ")
    notebook.add(tab2, text=" 💰 Giá & Ngày ")
    notebook.add(tab3, text=" ⚙️ Trạng thái ")

    create_form_fields(tab1, FIELD_GROUPS["tab1"]["labels"], FIELD_GROUPS["tab1"]["keys"])
    create_form_fields(tab2, FIELD_GROUPS["tab2"]["labels"], FIELD_GROUPS["tab2"]["keys"])
    create_form_fields(tab3, FIELD_GROUPS["tab3"]["labels"], FIELD_GROUPS["tab3"]["keys"])

    #  Button Frame 
    btn_frame = tk.Frame(left_frame, bg="white")
    btn_frame.pack(side="bottom", pady=10, padx=15, fill="x")
    btn_frame.grid_columnconfigure((0, 1), weight=1)

    global add_btn, update_btn, delete_btn
    add_btn = ttk.Button(btn_frame, text="➕ Thêm", style="Primary.TButton", command=add_service)
    add_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    update_btn = ttk.Button(btn_frame, text="✎ Cập nhật", style="Primary.TButton", command=update_service,
                            state="disabled")
    update_btn.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    delete_btn = ttk.Button(btn_frame, text="🗑️ Xóa", style="Danger.TButton", command=delete_service,
                            state="disabled")
    delete_btn.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
    ttk.Button(btn_frame, text="↻ Làm mới", style="Secondary.TButton", command=clear_form).grid(row=1, column=1,
                                                                                                 padx=5, pady=5,
                                                                                                 sticky="ew")

    #  RIGHT PANEL (TREE) 
    right_frame = tk.Frame(main_frame, bg="white", bd=2, relief="groove")
    right_frame.pack(side="right", fill="both", expand=True, pady=5)

    tk.Label(right_frame, text="📑 Danh sách Dịch vụ", bg="white", font=("Segoe UI", 14, "bold"),
             fg="#1e3a8a").pack(anchor="w", padx=15, pady=(10, 5))

    search_frame = tk.Frame(right_frame, bg="white")
    search_frame.pack(fill="x", padx=15, pady=5)
    global search_entry
    search_entry = ttk.Entry(search_frame, width=35)
    search_entry.pack(side="left", padx=5)
    ttk.Button(search_frame, text="🔍 Tìm kiếm", style="Primary.TButton", command=search_service).pack(side="left", padx=5)
    search_entry.bind("<Return>", lambda e: search_service())

    tree_container = tk.Frame(right_frame, bg="white")
    tree_container.pack(fill="both", expand=True, padx=10, pady=10)
    tree_scroll_y = ttk.Scrollbar(tree_container, orient="vertical")
    tree_scroll_y.pack(side="right", fill="y")
    tree_scroll_x = ttk.Scrollbar(tree_container, orient="horizontal")
    tree_scroll_x.pack(side="bottom", fill="x")

    global tree
    tree = ttk.Treeview(tree_container, columns=ALL_FIELD_KEYS, show="headings",
                        yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set, height=20)
    for key in ALL_FIELD_KEYS:
        tree.heading(key, text=key.replace("_", " ").title())
        tree.column(key, width=120, anchor="center")
    tree.pack(fill="both", expand=True)
    tree_scroll_y.config(command=tree.yview)
    tree_scroll_x.config(command=tree.xview)
    tree.bind("<<TreeviewSelect>>", on_tree_select)


    #   LOAD DATA TỪ DB
    try:
        populate_data_from_db()
    except Exception as e:
        messagebox.showerror("Lỗi DB", f"Không thể tải dữ liệu dịch vụ.\n{e}")

#   TẠO FORM FIELD CHO TABS
def create_form_fields(frame, labels, keys):
    global entries
    for i, (label, key) in enumerate(zip(labels, keys)):
        tk.Label(frame, text=label, bg="white", anchor="w").grid(row=i, column=0, sticky="w", padx=5, pady=5)
        if key == "loai_dv":
            entry = ttk.Combobox(frame, values=["Điện", "Nước", "Internet", "Giặt là", "Dọn vệ sinh"], state="readonly")
        elif key == "trang_thai":
            entry = ttk.Combobox(frame, values=["Hoạt động", "Ngưng"], state="readonly")
        elif key == "ngay_ap_dung":
            entry = DateEntry(frame, width=18, background='darkblue', foreground='white', borderwidth=2,
                              year=date.today().year)
        elif key == "mo_ta":
            entry = tk.Text(frame, height=4, width=28)
        else:
            entry = ttk.Entry(frame)
        entry.grid(row=i, column=1, sticky="w", padx=5, pady=5)
        entries[key] = entry

#  CÁC HÀM CRUD
def get_form_data():
    result = []
    for k in ALL_FIELD_KEYS:
        if k == "mo_ta":
            result.append(entries[k].get("1.0", "end").strip())
        elif k == "ngay_ap_dung":
            result.append(entries[k].get_date().strftime("%Y-%m-%d"))
        elif k == "don_gia":
            val = entries[k].get().strip()
            try:
                result.append(int(val) if val else 0)  # DECIMAL(12,0) trong DB
            except ValueError:
                result.append(0)
        else:
            result.append(entries[k].get().strip())
    return tuple(result)



def clear_form():
    for k in ALL_FIELD_KEYS:
        if k in entries:
            if k == "mo_ta":
                entries[k].delete("1.0", "end")
            elif k == "ngay_ap_dung":
                entries[k].set_date(date.today())
            elif k in ["loai_dv", "trang_thai"]:
                entries[k].set("")
            else:
                entries[k].delete(0, "end")
    if add_btn: add_btn.config(state="normal")
    if update_btn: update_btn.config(state="disabled")
    if delete_btn: delete_btn.config(state="disabled")
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

    for i, k in enumerate(ALL_FIELD_KEYS):
        val = values[i] if values[i] is not None else ""
        widget = entries[k]

        if isinstance(widget, ttk.Combobox):
            # Nếu giá trị DB chưa có trong list, thêm vào
            if val not in widget["values"]:
                widget["values"] = list(widget["values"]) + [val]
            widget.set(val)

        elif isinstance(widget, DateEntry):
            try:
                y, m, d = map(int, val.split('-'))
                widget.set_date(date(y, m, d))
            except:
                widget.set_date(date.today())

        elif isinstance(widget, tk.Text):
            widget.delete("1.0", "end")
            widget.insert("1.0", val)

        else:  # Entry
            widget.delete(0, "end")
            widget.insert(0, val)

    update_btn.config(state="normal")
    delete_btn.config(state="normal")

def add_service():
    data = get_form_data()
    if not data[0] or not data[1]:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập Mã và Tên dịch vụ")
        return
    query = """
    INSERT INTO dichvu (ma_dv, ten_dv, loai_dv, don_vi, don_gia, ngay_ap_dung, trang_thai, mo_ta)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    try:
        execute_non_query(query, data)
        messagebox.showinfo("Thành công", f"Đã thêm dịch vụ {data[1]}")
        populate_data_from_db()
        clear_form()
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def update_service():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn dịch vụ để cập nhật.")
        return

    data = get_form_data()  
    query = """
    UPDATE dichvu 
    SET ten_dv=?, loai_dv=?, don_vi=?, don_gia=?, ngay_ap_dung=?, trang_thai=?, mo_ta=? 
    WHERE ma_dv=?
    """
    try:
        execute_non_query(query, data[1:] + (data[0],))
        messagebox.showinfo("Thành công", f"Đã cập nhật dịch vụ {data[1]}")
        populate_data_from_db()
        clear_form()
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))



def delete_service():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn dịch vụ để xóa.")
        return

    confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa dịch vụ này không?")
    if not confirm:
        return

    try:
        index = tree.index(selected[0])
        ma_dv = master_data_list[index][0]
        query = "DELETE FROM dichvu WHERE ma_dv=?"
        execute_non_query(query, (ma_dv,))
        master_data_list.pop(index)
        tree.delete(selected[0])
        messagebox.showinfo("Thành công", f"Đã xóa dịch vụ {ma_dv}")
        clear_form()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Xóa không thành công:\n{e}")




def search_service():
    term = search_entry.get().lower()
    tree.delete(*tree.get_children())
    for row in master_data_list:
        if term in str(row).lower():
            tree.insert("", "end", values=row)

def populate_data_from_db():
    global master_data_list
    query = """
    SELECT ma_dv, ten_dv, loai_dv, don_vi, don_gia, CONVERT(varchar, ngay_ap_dung, 23), trang_thai, mo_ta
    FROM dichvu
    """
    try:
        raw_data = fetch_all(query)
        master_data_list = [
            tuple(str(v) if v is not None else "" for v in row)
            for row in raw_data
        ]
        refresh_tree()
    except Exception as e:
        messagebox.showerror("Lỗi DB", str(e))



def go_back_to_home(root):
    from app.ui.homepage import show_home_page
    show_home_page(root)
