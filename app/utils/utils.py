def clear_window(root):
    """Xóa toàn bộ giao diện hiện tại"""
    for widget in root.winfo_children():
        widget.destroy()
