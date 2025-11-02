import tkinter as tk
from tkinter import ttk, messagebox

# ==================================
# KHAI BÁO BIẾN TOÀN CỤC
# ==================================
entries = {}
tree = None
add_btn, update_btn, delete_btn = None, None, None
search_entry = None
master_data_list = []

FIELD_GROUPS = {
    "tab1": {
        "labels": ["Mã SV:", "Họ và tên:", "Ngày sinh (dd/mm/yy):", "Giới tính:", "CMND/CCCD:"],
        "keys": ["ma_sv", "ho_ten", "ngay_sinh", "gioi_tinh", "cmnd_cccd"]
    },
    "tab2": {
        "labels": ["Số điện thoại:", "Email:", "Quê quán:", "Khoa:", "Lớp:"],
        "keys": ["sdt", "email", "que_quan", "khoa", "lop"]
    },
    "tab3": {
        "labels": ["Phòng:", "Ngày vào KTX:", "Trạng thái:", "Ghi chú:"],
        "keys": ["phong", "ngay_vao", "trang_thai", "ghi_chu"]
    }
}
ALL_FIELD_KEYS = FIELD_GROUPS["tab1"]["keys"] + FIELD_GROUPS["tab2"]["keys"] + FIELD_GROUPS["tab3"]["keys"]

def show_student_management(root):
    """Giao diện Quản lý Sinh viên - Cột cố định, Nút nổi bật"""
    global entries, tree, add_btn, update_btn, delete_btn, search_entry, master_data_list
    
    master_data_list = []
    entries = {}

    for widget in root.winfo_children():
        widget.destroy()

    # ====== CẤU HÌNH CỬA SỔ (Tối ưu cho 1366x768) ======
    root.title("👨‍🎓 Quản lý Sinh viên - Hệ thống Quản lý Ký túc xá")
    root.geometry("1280x670") 
    root.configure(bg="#f0f4ff")

    # ============================
    # ====== STYLE NÂNG CAO ======
    # ============================
    style = ttk.Style()
    style.theme_use("clam")

    # --- Nền và Khung ---
    style.configure("TFrame", background="#f0f4ff") # Nền xanh nhạt
    style.configure("White.TFrame", background="white") # Nền trắng
    
    # --- Tiêu đề ---
    style.configure("Title.TLabel", background="white", foreground="#1e3a8a", font=("Segoe UI", 16, "bold"))
    style.configure("Header.TLabel", background="white", foreground="#1e3a8a", font=("Segoe UI", 13, "bold"))
    style.configure("TLabel", background="white", foreground="#0f172a", font=("Segoe UI", 11))
                    
    # --- Widget nhập liệu ---
    style.configure("TEntry", fieldbackground="white", font=("Segoe UI", 11), padding=4)
    style.configure("TCombobox", fieldbackground="white", font=("Segoe UI", 11), padding=4)
    style.map("TCombobox",
        arrowcolor=[('!readonly', 'white')],
        fieldbackground=[('readonly', 'white')],
        selectbackground=[('readonly', '#dbeafe')],
        selectforeground=[('readonly', 'black')]
    )

    # --- CÁC NÚT BẤM (MÀU NỔI BẬT HƠN) ---
    btn_padding = (10, 7)
    
    # Nút Primary (Xanh da trời sáng)
    style.configure("Primary.TButton", font=("Segoe UI", 11, "bold"), padding=btn_padding,
                    background="#0ea5e9", foreground="white", borderwidth=0)
    style.map("Primary.TButton", 
              background=[("active", "#0284c7"), ("disabled", "#9ca3af")]) # active: xanh đậm hơn

    # Nút Danger (Đỏ hồng)
    style.configure("Danger.TButton", font=("Segoe UI", 11, "bold"), padding=btn_padding,
                    background="#e11d48", foreground="white", borderwidth=0)
    style.map("Danger.TButton", 
              background=[("active", "#be123c"), ("disabled", "#9ca3af")]) # active: đỏ đậm hơn

    # Nút Secondary (Xám kim loại)
    style.configure("Secondary.TButton", font=("Segoe UI", 11, "bold"), padding=btn_padding,
                    background="#a1a1aa", foreground="white", borderwidth=0)
    style.map("Secondary.TButton", 
              background=[("active", "#71717a")]) # active: xám đậm hơn

    # Nút Back (Giữ nguyên)
    style.configure("Back.TButton", font=("Segoe UI", 11, "bold"), padding=(10, 8),
                    background="#1e3a8a", foreground="white", borderwidth=0)
    style.map("Back.TButton", background=[("active", "#2563eb")])
              
    # --- Treeview ---
    style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), 
                    background="#e0e7ff", foreground="#1e3a8a", padding=10)
    style.configure("Treeview", font=("Segoe UI", 10), rowheight=27,
                    background="white", fieldbackground="white")
    style.map("Treeview",
              background=[("selected", "#dbeafe")], 
              foreground=[("selected", "black")])

    # --- Style cho Notebook (Tabs) ---
    style.configure("TNotebook", background="white", borderwidth=0)
    style.configure("TNotebook.Tab", 
                    font=("Segoe UI", 10, "bold"), 
                    padding=(12, 7), 
                    background="#f1f5f9", foreground="#64748b", borderwidth=0)
    style.map("TNotebook.Tab",
              background=[("selected", "#e0e7ff")],
              foreground=[("selected", "#1e3a8a")])
    style.configure("TNotebook.Pane", background="white", borderwidth=1, 
                    relief="solid", bordercolor="#cbd5e1")

    # ==========================
    # ====== HEADER CHÍNH ======
    # ==========================
    header = tk.Frame(root, bg="#1e3a8a", height=70)
    header.pack(fill="x", side="top") # Pack lên trên cùng
    header.pack_propagate(False)

    tk.Label(header, text="👨‍🎓 Quản lý Sinh viên", bg="#1e3a8a", fg="white",
             font=("Segoe UI", 18, "bold")).pack(side="left", padx=20, pady=12)
    ttk.Button(header, text="⬅ Quay lại Trang chủ", style="Back.TButton",
               command=lambda: go_back_to_home(root)).pack(side="right", padx=20, pady=10)

    # ========================================
    # ====== BỐ CỤC CHÍNH (Layout Ổn định) ======
    # ========================================
    
    # Khung container chính
    main_container = ttk.Frame(root, style="TFrame", padding=(20, 15, 20, 20))
    main_container.pack(fill="both", expand=True, side="bottom")
    
    # --- KHUNG ĐIỀU KHIỂN (BÊN TRÁI) ---
    left_wrapper = ttk.Frame(main_container, style="White.TFrame", 
                             borderwidth=1, relief="solid")
    left_wrapper.pack(side="left", fill="y", padx=(0, 15))
    
    # Dùng width=460 để đảm bảo không bị che
    left_pane = ttk.Frame(left_wrapper, style="White.TFrame", width=460)
    left_pane.pack(fill="y", expand=True)
    # **QUAN TRỌNG: Chống co khung**
    left_pane.pack_propagate(False) 

    ttk.Label(left_pane, text="THÔNG TIN CHI TIẾT", style="Title.TLabel") \
       .pack(pady=(15, 10), padx=25, anchor="w")

    # --- Tạo Notebook (Tabs) ---
    notebook = ttk.Notebook(left_pane, style="TNotebook")
    notebook.pack(fill="both", expand=True, padx=20, pady=0)

    tab_padding = (15, 10)
    tab1 = ttk.Frame(notebook, style="White.TFrame", padding=tab_padding)
    tab2 = ttk.Frame(notebook, style="White.TFrame", padding=tab_padding)
    tab3 = ttk.Frame(notebook, style="White.TFrame", padding=tab_padding)
    
    notebook.add(tab1, text=" 👤  Cá nhân ")
    notebook.add(tab2, text=" 📞  Liên hệ & Học vấn ")
    notebook.add(tab3, text=" 🏨  Nội trú ")

    create_form_fields(tab1, FIELD_GROUPS["tab1"]["labels"], FIELD_GROUPS["tab1"]["keys"])
    create_form_fields(tab2, FIELD_GROUPS["tab2"]["labels"], FIELD_GROUPS["tab2"]["keys"])
    create_form_fields(tab3, FIELD_GROUPS["tab3"]["labels"], FIELD_GROUPS["tab3"]["keys"])

    # --- Khung Nút Chức năng ---
    button_frame = ttk.Frame(left_pane, style="White.TFrame", padding=(20, 10))
    button_frame.pack(fill="x", side="bottom")

    button_frame.grid_columnconfigure((0, 1), weight=1)
    
    add_btn = ttk.Button(button_frame, text="➕ Thêm mới", style="Primary.TButton", command=add_student)
    add_btn.grid(row=0, column=0, padx=5, pady=4, sticky="ew")
    update_btn = ttk.Button(button_frame, text="✎ Cập nhật", style="Primary.TButton", command=update_student, state="disabled")
    update_btn.grid(row=0, column=1, padx=5, pady=4, sticky="ew")
    delete_btn = ttk.Button(button_frame, text="🗑️ Xóa", style="Danger.TButton", command=delete_student, state="disabled")
    delete_btn.grid(row=1, column=0, padx=5, pady=4, sticky="ew")
    clear_btn = ttk.Button(button_frame, text="↻ Làm mới", style="Secondary.TButton", command=refresh_all_data)
    clear_btn.grid(row=1, column=1, padx=5, pady=4, sticky="ew")


    # --- KHUNG DỮ LIỆU (BÊN PHẢI) ---
    right_pane = ttk.Frame(main_container, style="White.TFrame",
                           borderwidth=1, relief="solid")
    right_pane.pack(side="right", fill="both", expand=True, padx=(0, 0))

    # --- Header của Khung Dữ liệu ---
    data_header = ttk.Frame(right_pane, style="White.TFrame")
    data_header.pack(fill="x", padx=15, pady=8)
    
    ttk.Label(data_header, text="DANH SÁCH SINH VIÊN", style="Header.TLabel") \
       .pack(side="left", padx=(5, 0), pady=8)

    search_btn = ttk.Button(data_header, text="Tìm", style="Primary.TButton", command=search_students)
    search_btn.pack(side="right", padx=(8, 5), pady=8)
    search_entry = ttk.Entry(data_header, width=40, style="TEntry", font=("Segoe UI", 11))
    search_entry.pack(side="right", fill="x", pady=8)
    ttk.Label(data_header, text="🔍", style="TLabel", font=("Segoe UI", 14)) \
       .pack(side="right", padx=(0, 10), pady=8)
    search_entry.bind("<Return>", lambda event: search_students())
    
    # --- Khung Treeview ---
    tree_container = ttk.Frame(right_pane, style="White.TFrame")
    tree_container.pack(fill="both", expand=True, padx=15, pady=(0, 10))

    tree_scroll_y = ttk.Scrollbar(tree_container, orient="vertical")
    tree_scroll_y.pack(side="right", fill="y")
    tree_scroll_x = ttk.Scrollbar(tree_container, orient="horizontal")
    tree_scroll_x.pack(side="bottom", fill="x")
    
    tree = ttk.Treeview(tree_container, columns=ALL_FIELD_KEYS, show="headings", 
                        yscrollcommand=tree_scroll_y.set, 
                        xscrollcommand=tree_scroll_x.set,
                        style="Treeview")
    
    # --- ĐỊNH NGHĨA CỘT (ĐÃ THÊM stretch=tk.NO) ---
    tree.heading("ma_sv", text="Mã SV")
    tree.column("ma_sv", width=80, anchor="center", stretch=tk.NO)
    
    tree.heading("ho_ten", text="Họ tên")
    tree.column("ho_ten", width=180, stretch=tk.NO)
    
    tree.heading("ngay_sinh", text="Ngày sinh")
    tree.column("ngay_sinh", width=100, anchor="center", stretch=tk.NO)
    
    tree.heading("gioi_tinh", text="Giới tính")
    tree.column("gioi_tinh", width=90, anchor="center", stretch=tk.NO)
    
    tree.heading("cmnd_cccd", text="CMND/CCCD")
    tree.column("cmnd_cccd", width=120, stretch=tk.NO)
    
    tree.heading("sdt", text="SĐT")
    tree.column("sdt", width=100, stretch=tk.NO)
    
    tree.heading("que_quan", text="Quê quán")
    tree.column("que_quan", width=150, stretch=tk.NO)

    tree.heading("khoa", text="Khoa")
    tree.column("khoa", width=150, stretch=tk.NO)
    
    tree.heading("lop", text="Lớp")
    tree.column("lop", width=100, stretch=tk.NO)
    
    tree.heading("email", text="Email")
    tree.column("email", width=180, stretch=tk.NO)
    
    tree.heading("phong", text="Phòng")
    tree.column("phong", width=70, anchor="center", stretch=tk.NO)
    
    tree.heading("ngay_vao", text="Ngày vào")
    tree.column("ngay_vao", width=100, anchor="center", stretch=tk.NO)
    
    tree.heading("trang_thai", text="Trạng thái")
    tree.column("trang_thai", width=100, anchor="center", stretch=tk.NO)
    
    tree.heading("ghi_chu", text="Ghi chú")
    tree.column("ghi_chu", width=200, stretch=tk.NO)

    tree.pack(fill="both", expand=True)
    tree_scroll_y.config(command=tree.yview)
    tree_scroll_x.config(command=tree.xview)

    tree.bind("<<TreeviewSelect>>", on_student_select)
    
    populate_sample_data()
    search_entry.focus()


# ==================================
# HÀM TẠO FORM PHỤ TRỢ
# ==================================
def create_form_fields(frame, labels, keys):
    global entries
    for i, (label_text, key) in enumerate(zip(labels, keys)):
        ttk.Label(frame, text=label_text, style="TLabel") \
           .grid(row=i, column=0, sticky="e", pady=6, padx=5)
        
        if key == "gioi_tinh":
            widget = ttk.Combobox(frame, values=["Nam", "Nữ", "Khác"], width=28, state="readonly", style="TCombobox")
        elif key == "phong":
            widget = ttk.Combobox(frame, values=["A101", "A102", "B201", "B202", "C301", "C302"], width=28, style="TCombobox")
        elif key == "khoa":
             widget = ttk.Combobox(frame, values=["Công nghệ thông tin", "Kinh tế", "Nông nghiệp", "Sư phạm", "Kỹ thuật"], width=28, style="TCombobox")
        elif key == "trang_thai":
             widget = ttk.Combobox(frame, values=["Đang ở", "Đã tốt nghiệp", "Đã rời KTX", "Bị kỷ luật"], width=28, state="readonly", style="TCombobox")
        else:
            widget = ttk.Entry(frame, width=30, style="TEntry")
            
        widget.grid(row=i, column=1, pady=6, padx=5, sticky="w")
        entries[key] = widget

# ==================================
# CÁC HÀM XỬ LÝ LOGIC (Không đổi)
# ==================================

def go_back_to_home(root):
    from app.ui.homepage import show_home_page
    show_home_page(root)

def clear_form(set_focus=False):
    global add_btn, update_btn, delete_btn, entries
    
    for key, entry in entries.items():
        if isinstance(entry, ttk.Combobox):
            entry.set("")
        else:
            entry.config(state="normal")
            entry.delete(0, "end")
            
    if add_btn: add_btn.config(state="normal")
    if update_btn: update_btn.config(state="disabled")
    if delete_btn: delete_btn.config(state="disabled")

    if tree and tree.selection():
        tree.selection_remove(tree.selection()[0])
        
    if set_focus and "ma_sv" in entries:
        entries["ma_sv"].focus()

def refresh_all_data():
    global search_entry, master_data_list, tree
    clear_form()
    if search_entry:
        search_entry.delete(0, "end")
    if tree:
        tree.delete(*tree.get_children())
        for student in master_data_list:
            tree.insert("", "end", values=student)

def get_form_data():
    data = []
    for key in ALL_FIELD_KEYS:
        if key in entries:
            data.append(entries[key].get())
        else:
            data.append("")
    return tuple(data)

def on_student_select(event):
    global add_btn, update_btn, delete_btn, entries, tree
    selected_item = tree.selection()
    if not selected_item: return
    
    selected_item = selected_item[0]
    values = tree.item(selected_item, "values")
    
    # **ĐÂY LÀ THAY ĐỔI QUAN TRỌNG:**
    # Gọi clear_form nhưng KHÔNG xóa lựa chọn trên Treeview
    clear_form(set_focus=False, clear_tree_selection=False) 
    
    for key, value in zip(ALL_FIELD_KEYS, values):
        if key in entries:
            entry = entries[key]
            if isinstance(entry, ttk.Combobox):
                entry.set(value)
            else:
                entry.insert(0, value)
            
    entries["ma_sv"].config(state="readonly") 
    
    add_btn.config(state="disabled")
    update_btn.config(state="normal")
    delete_btn.config(state="normal")

def clear_form(set_focus=False, clear_tree_selection=True):
    global add_btn, update_btn, delete_btn, entries
    
    for key, entry in entries.items():
        if isinstance(entry, ttk.Combobox):
            entry.set("")
        else:
            entry.config(state="normal")
            entry.delete(0, "end")
            
    if add_btn: add_btn.config(state="normal")
    if update_btn: update_btn.config(state="disabled")
    if delete_btn: delete_btn.config(state="disabled")

    # Chỉ xóa lựa chọn treeview nếu được yêu cầu
    if clear_tree_selection:
        if tree and tree.selection():
            tree.selection_remove(tree.selection()[0])
        
    if set_focus and "ma_sv" in entries:
        entries["ma_sv"].focus()

def populate_sample_data():
    global master_data_list, tree
    
    # DANH SÁCH DỮ LIỆU ĐÃ ĐƯỢC SẮP XẾP LẠI CHO ĐÚNG THỨ TỰ
    master_data_list = [
        # (ma_sv, ho_ten, ngay_sinh, gioi_tinh, cmnd_cccd, sdt, email, que_quan, khoa, lop, phong, ngay_vao, trang_thai, ghi_chu)
        ("SV001", "Nguyễn Văn An", "10/10/2003", "Nam", "089123456", "0912345678", "nva@gmail.com", "An Giang", "Công nghệ thông tin", "DH22TH", "A101", "05/09/2022", "Đang ở", ""),
        ("SV002", "Trần Thị Bình", "05/12/2003", "Nữ", "089654321", "0987654321", "ttb@gmail.com", "Kiên Giang", "Kinh tế", "DH22KT", "A102", "05/09/2022", "Đang ở", "Ưu tiên"),
        ("SV003", "Lê Văn Cường", "20/03/2003", "Nam", "077123123", "0905123123", "lvc@gmail.com", "Đồng Tháp", "Nông nghiệp", "DH22NN", "B201", "10/09/2022", "Đang ở", ""),
        ("SV004", "Phạm Thị Dung", "15/07/2003", "Nữ", "065321321", "0345678901", "ptd@gmail.com", "Cần Thơ", "Sư phạm", "DH22SP", "B202", "10/09/2022", "Đã rời KTX", "Chuyển ra ngoài"),
        ("SV005", "Võ Minh Hải", "30/01/2003", "Nam", "090555666", "0777888999", "vmh@gmail.com", "An Giang", "Công nghệ thông tin", "DH22TH", "A101", "15/09/2022", "Đang ở", "")
    ]
    
    refresh_all_data()

# --- CÁC HÀM CRUD (SỬA LỖI PARENT) ---

def get_root_window():
    if add_btn:
        return add_btn.winfo_toplevel()
    elif tree:
        return tree.winfo_toplevel()
    else:
        return tk._default_root 
        
def add_student():
    global master_data_list, tree, entries
    data = get_form_data()
    ma_sv, ho_ten = data[0], data[1]
    root_window = get_root_window()
    
    if not ma_sv or not ho_ten:
        messagebox.showwarning("Thiếu thông tin", "Mã SV và Họ tên là bắt buộc.", parent=root_window)
        return

    for student in master_data_list:
        if student[0] == ma_sv:
            messagebox.showerror("Lỗi", f"Mã SV [ {ma_sv} ] đã tồn tại!", parent=root_window)
            return
            
    master_data_list.append(data)
    tree.insert("", "end", values=data)
    
    last_item = tree.get_children()[-1]
    tree.selection_set(last_item)
    tree.focus(last_item)
    tree.see(last_item)
    
    messagebox.showinfo("Thành công", f"Đã thêm sinh viên [ {ho_ten} ].", parent=root_window)
    clear_form(set_focus=True)

def update_student():
    global master_data_list, tree
    root_window = get_root_window()
    
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn một sinh viên để sửa.", parent=root_window)
        return
    selected_item = selected_item[0]
    
    new_data = get_form_data()
    ma_sv = new_data[0]
    
    tree.item(selected_item, values=new_data)
    
    for i, student in enumerate(master_data_list):
        if student[0] == ma_sv:
            master_data_list[i] = new_data
            break
            
    messagebox.showinfo("Thành công", f"Đã cập nhật sinh viên [ {ma_sv} ].", parent=root_window)
    clear_form()
    
def delete_student():
    global master_data_list, tree
    root_window = get_root_window()

    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn một sinh viên để xóa.", parent=root_window)
        return
    selected_item = selected_item[0]
    
    values = tree.item(selected_item, "values")
    ma_sv, ho_ten = values[0], values[1]
    
    if messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa sinh viên:\n\n{ma_sv} - {ho_ten}?", parent=root_window):
        tree.delete(selected_item)
        for student in master_data_list:
            if student[0] == ma_sv:
                master_data_list.remove(student)
                break
        messagebox.showinfo("Thành công", f"Đã xóa sinh viên [ {ma_sv} ].", parent=root_window)
        clear_form()

def search_students():
    global search_entry, master_data_list, tree
    search_term = search_entry.get().lower().strip()
    
    tree.delete(*tree.get_children())
    
    if not search_term:
        for student in master_data_list:
            tree.insert("", "end", values=student)
        return
        
    for student in master_data_list:
        if search_term in str(student).lower():
            tree.insert("", "end", values=student)