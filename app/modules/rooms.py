import tkinter as tk
from tkinter import ttk, messagebox
from app.db import fetch_all, execute_non_query

entries = {}
tree = None
add_btn = update_btn = delete_btn = None
search_entry = None
master_data_list = []
#  FIELD KEYS 
FIELD_KEYS = ["ma_phong", "toa_nha", "loai_phong", "so_nguoi_toi_da",
              "so_nguoi_hien_tai", "gia_phong", "trang_thai", "ghi_chu"]

#  SHOW MODULE 
def show_room_management(root):
    global entries, tree, add_btn, update_btn, delete_btn, search_entry, master_data_list
    entries = {}
    master_data_list = []

    for w in root.winfo_children():
        w.destroy()

    root.title("🏢 Quản lý Phòng - KTX")
    root.geometry("1400x750")
    root.configure(bg="#f0f4f8")

    #  HEADER 
    header = tk.Frame(root, bg="#1e3a8a", height=80)
    header.pack(fill="x", side="top")
    header.pack_propagate(False)
    tk.Label(header, text="🏢 QUẢN LÝ PHÒNG KÝ TÚC XÁ", bg="#1e3a8a", fg="white",
             font=("Segoe UI", 24, "bold")).pack(side="left", padx=30)
    ttk.Button(header, text="⬅ Quay lại Trang chủ", command=lambda: go_back_to_home(root),
               style="Back.TButton").pack(side="right", padx=20, pady=15)

    #  STYLE 
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#f0f4f8")
    style.configure("White.TFrame", background="white")
    style.configure("TLabel", background="white", font=("Segoe UI", 12))
    style.configure("Title.TLabel", background="white", font=("Segoe UI", 16, "bold"), foreground="#1e3a8a")
    style.configure("TEntry", padding=5, font=("Segoe UI", 12))
    style.configure("TCombobox", padding=5, font=("Segoe UI", 12))
    style.map("TCombobox", selectbackground=[("readonly", "#dbeafe")], selectforeground=[("readonly", "black")])
    btn_padding = (12, 8)
    style.configure("Primary.TButton", font=("Segoe UI", 12, "bold"), padding=btn_padding,
                    background="#0ea5e9", foreground="white")
    style.map("Primary.TButton", background=[("active", "#0284c7"), ("disabled", "#9ca3af")])
    style.configure("Danger.TButton", font=("Segoe UI", 12, "bold"), padding=btn_padding,
                    background="#e11d48", foreground="white")
    style.map("Danger.TButton", background=[("active", "#be123c"), ("disabled", "#9ca3af")])
    style.configure("Secondary.TButton", font=("Segoe UI", 12, "bold"), padding=btn_padding,
                    background="#6b7280", foreground="white")
    style.map("Secondary.TButton", background=[("active", "#4b5563")])
    style.configure("Back.TButton", font=("Segoe UI", 12, "bold"), padding=(12, 8),
                    background="#1e3a8a", foreground="white")
    style.map("Back.TButton", background=[("active", "#2563eb")])

    #  MAIN LAYOUT 
    main_frame = tk.Frame(root, bg="#f0f4f8")
    main_frame.pack(fill="both", expand=True, padx=20, pady=15)

    #  LEFT FORM PANEL 
    left_frame = tk.Frame(main_frame, bg="white", bd=2, relief="groove")
    left_frame.pack(side="left", fill="y", padx=(0,15))
    left_frame.pack_propagate(False)
    left_frame.configure(width=500)

    tk.Label(left_frame, text="📋 Thông tin Phòng", font=("Segoe UI", 16, "bold"), bg="white", fg="#1e3a8a").pack(pady=15)

    form_frame = tk.Frame(left_frame, bg="white")
    form_frame.pack(padx=15, pady=10)
    for i, key in enumerate(FIELD_KEYS):
        tk.Label(form_frame, text=key.replace("_"," ").title()+":", bg="white", anchor="w", font=("Segoe UI", 12)).grid(row=i, column=0, sticky="w", padx=5, pady=6)
        if key == "trang_thai":
            entry = ttk.Combobox(form_frame, values=["Còn trống","Đầy","Đang sử dụng"], state="readonly")
        elif key == "ghi_chu":
            entry = tk.Text(form_frame, width=25, height=4, font=("Segoe UI",12))
        else:
            entry = ttk.Entry(form_frame, font=("Segoe UI",12))
        entry.grid(row=i, column=1, sticky="w", padx=5, pady=6)
        entries[key] = entry

    # BUTTONS   
    btn_frame = tk.Frame(left_frame, bg="white")
    btn_frame.pack(side="bottom", pady=15, padx=15, fill="x")
    add_btn = ttk.Button(btn_frame, text="➕ Thêm", style="Primary.TButton", command=lambda: add_room())
    add_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    update_btn = ttk.Button(btn_frame, text="✎ Cập nhật", style="Primary.TButton", command=lambda: update_room(), state="disabled")
    update_btn.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    delete_btn = ttk.Button(btn_frame, text="🗑️ Xóa", style="Danger.TButton", command=lambda: delete_room(), state="disabled")
    delete_btn.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
    ttk.Button(btn_frame, text="↻ Làm mới", style="Secondary.TButton", command=lambda: clear_form()).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    #  RIGHT TREE PANEL 
    right_frame = tk.Frame(main_frame, bg="white", bd=2, relief="groove")
    right_frame.pack(side="right", fill="both", expand=True)

    tk.Label(right_frame, text="📑 Danh sách Phòng", bg="white", font=("Segoe UI",16,"bold"), fg="#1e3a8a").pack(anchor="w", padx=15, pady=(10,5))

    # SEARCH
    search_frame = tk.Frame(right_frame, bg="white")
    search_frame.pack(fill="x", padx=15, pady=5)
    search_entry = ttk.Entry(search_frame, width=35, font=("Segoe UI",12))
    search_entry.pack(side="left", padx=5)
    ttk.Button(search_frame, text="🔍 Tìm kiếm", style="Primary.TButton", command=lambda: search_room()).pack(side="left", padx=5)
    search_entry.bind("<Return>", lambda e: search_room())

    # TREEVIEW
    tree_container = tk.Frame(right_frame, bg="white")
    tree_container.pack(fill="both", expand=True, padx=10, pady=10)
    tree_scroll_y = ttk.Scrollbar(tree_container, orient="vertical")
    tree_scroll_y.pack(side="right", fill="y")
    tree_scroll_x = ttk.Scrollbar(tree_container, orient="horizontal")
    tree_scroll_x.pack(side="bottom", fill="x")

    global tree
    tree = ttk.Treeview(tree_container, columns=FIELD_KEYS, show="headings",
                        yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set, height=25)
    for key in FIELD_KEYS:
        tree.heading(key, text=key.replace("_"," ").title())
        tree.column(key, width=140, anchor="center")
    tree.pack(fill="both", expand=True)
    tree_scroll_y.config(command=tree.yview)
    tree_scroll_x.config(command=tree.xview)
    tree.bind("<<TreeviewSelect>>", lambda e: on_tree_select())

    populate_data_from_db()


#  FORM & CRUD 
def get_form_data():
    result = []
    for k in FIELD_KEYS:
        if k=="ghi_chu":
            val = entries[k].get("1.0","end").strip()
        else:
            val = entries[k].get().strip()
        if k in ["so_nguoi_toi_da","so_nguoi_hien_tai"]:
            val = int(val) if val else 0
        elif k=="gia_phong":
            val = float(val) if val else 0
        result.append(val)
    return tuple(result)

def clear_form():
    for k in FIELD_KEYS:
        if k=="ghi_chu":
            entries[k].delete("1.0","end")
        else:
            entries[k].delete(0,"end")
    add_btn.config(state="normal")
    update_btn.config(state="disabled")
    delete_btn.config(state="disabled")
    if tree.selection(): tree.selection_remove(tree.selection()[0])

def refresh_tree():
    tree.delete(*tree.get_children())
    for row in master_data_list:
        tree.insert("", "end", values=[str(v) for v in row])

def on_tree_select():
    sel = tree.selection()
    if not sel: 
        return
    values = tree.item(sel[0],"values")
    for i, k in enumerate(FIELD_KEYS):
        if k=="ghi_chu":
            entries[k].delete("1.0","end")
            entries[k].insert("1.0", values[i])
        elif k=="trang_thai":   # combobox
            entries[k].set(values[i])
        else:
            entries[k].delete(0,"end")
            entries[k].insert(0, values[i])
    add_btn.config(state="disabled")
    update_btn.config(state="normal")
    delete_btn.config(state="normal")


def populate_data_from_db():
    global master_data_list
    query = "SELECT ma_phong, toa_nha, loai_phong, so_nguoi_toi_da, so_nguoi_hien_tai, gia_phong, trang_thai, ghi_chu FROM phong"
    master_data_list = fetch_all(query)
    refresh_tree()

def add_room():
    data = get_form_data()
    if not data[0]:
        messagebox.showwarning("Thiếu thông tin","Vui lòng nhập Mã phòng")
        return
    try:
        execute_non_query("INSERT INTO phong (ma_phong, toa_nha, loai_phong, so_nguoi_toi_da, so_nguoi_hien_tai, gia_phong, trang_thai, ghi_chu) VALUES (?,?,?,?,?,?,?,?)", data)
        messagebox.showinfo("Thành công",f"Đã thêm phòng {data[0]}")
        populate_data_from_db()
        clear_form()
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def update_room():
    sel = tree.selection()
    if not sel: return
    data = get_form_data()
    try:
        execute_non_query("UPDATE phong SET toa_nha=?, loai_phong=?, so_nguoi_toi_da=?, so_nguoi_hien_tai=?, gia_phong=?, trang_thai=?, ghi_chu=? WHERE ma_phong=?", data[1:]+(data[0],))
        messagebox.showinfo("Thành công",f"Đã cập nhật phòng {data[0]}")
        populate_data_from_db()
        clear_form()
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def delete_room():
    sel = tree.selection()
    if not sel: return
    ma_phong = tree.item(sel[0],"values")[0]
    if not messagebox.askyesno("Xác nhận",f"Xóa phòng {ma_phong}?"): return
    try:
        execute_non_query("DELETE FROM phong WHERE ma_phong=?", (ma_phong,))
        messagebox.showinfo("Thành công", f"Đã xóa phòng {ma_phong}")
        populate_data_from_db()
        clear_form()
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def search_room():
    term = search_entry.get().lower()
    tree.delete(*tree.get_children())
    for row in master_data_list:
        if term in str(row).lower():
            tree.insert("", "end", values=[str(v) for v in row])

def go_back_to_home(root):
    from app.ui.homepage import show_home_page
    show_home_page(root)
