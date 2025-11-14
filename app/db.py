import pyodbc
import datetime

# ============================================================
# 🔧 CẤU HÌNH KẾT NỐI SQL SERVER
# ============================================================
DRIVER = "{ODBC Driver 17 for SQL Server}"  # hoặc "{SQL Server}"
SERVER = r"LAPTOP-EU99C1O4\SQLEXPRESS"      # ⚠️ Thay bằng tên server thật của bạn
DATABASE = "QUANLYKTX"                     # Tên database
Trusted = True                             # True = Windows Authentication, False = SQL Authentication

USER = "sa"                                # Chỉ dùng nếu Trusted = False
PASSWORD = "123"                 # Chỉ dùng nếu Trusted = False


# ============================================================
# 🧩 HÀM TẠO KẾT NỐI
# ============================================================
def get_connection():
    """Tạo và trả về kết nối tới SQL Server"""
    try:
        if Trusted:
            conn_str = f"DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;"
        else:
            conn_str = f"DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};UID={USER};PWD={PASSWORD};"
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ❌ Lỗi kết nối SQL Server:", e)
        return None


# ============================================================
# 📘 HÀM SELECT NHIỀU DÒNG
# ============================================================
def fetch_all(query, params=()):
    """
    Dùng cho SELECT nhiều dòng.
    Trả về list các tuple hoặc [] nếu lỗi.
    """
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ❌ Lỗi fetch_all:", e)
        return []


# ============================================================
# 📗 HÀM SELECT 1 DÒNG DUY NHẤT
# ============================================================
def fetch_one(query, params=()):
    """
    Dùng cho SELECT 1 dòng (ví dụ kiểm tra, đăng nhập, lấy chi tiết 1 bản ghi)
    Trả về tuple hoặc None nếu không có dữ liệu.
    """
    conn = get_connection()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        row = cur.fetchone()
        conn.close()
        return row
    except Exception as e:
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ❌ Lỗi fetch_one:", e)
        return None


# ============================================================
# 🧾 HÀM INSERT / UPDATE / DELETE
# ============================================================
def execute_non_query(query, params=()):
    """
    Dùng cho INSERT / UPDATE / DELETE.
    Trả về True nếu thành công, False nếu lỗi.
    """
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ❌ Lỗi execute_non_query:", e)
        try:
            conn.rollback()
        except:
            pass
        return False


# ============================================================
# 🔹 HÀM KIỂM TRA KẾT NỐI SQL SERVER
# ============================================================
def check_connection():
    """Kiểm tra kết nối SQL Server, in log ra console"""
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 🔄 Đang kiểm tra kết nối SQL Server...")
    conn = get_connection()
    if conn:
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ✅ Kết nối thành công tới database '{DATABASE}'")
        conn.close()
        return True
    else:
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ❌ Không thể kết nối tới SQL Server")
        return False


# ============================================================
# 🧪 TỰ ĐỘNG KIỂM TRA KẾT NỐI KHI IMPORT
# ============================================================
if __name__ != "__main__":
    check_connection()
else:
    # Nếu chạy trực tiếp file db.py để test
    check_connection()
    print("\n📋 Danh sách 5 sinh viên đầu tiên:")
    rows = fetch_all("SELECT TOP 5 * FROM sinhvien")
    for r in rows:
        print(r)
