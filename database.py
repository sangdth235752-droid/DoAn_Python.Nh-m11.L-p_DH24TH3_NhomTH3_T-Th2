# database.py
import mysql.connector
from mysql.connector import Error

# ==============================================
#  HÀM KẾT NỐI CƠ SỞ DỮ LIỆU
def get_connection():
    try:
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456", 
        database="qli_chxm"
        )
        return conn
    except Error as e:
        print("❌ Lỗi kết nối MySQL:", e)
        return None


# ==============================================
#  HÀM ĐĂNG NHẬP - PHÂN QUYỀN NHÂN VIÊN
def dang_nhap(ten_dang_nhap, mat_khau):
    conn = get_connection()
    if conn is None:
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM nhanvien WHERE TenDangNhap = %s AND MatKhau = %s"
        cursor.execute(query, (ten_dang_nhap, mat_khau))
        user = cursor.fetchone()
        return user  # trả về thông tin nhân viên (nếu có)
    except Error as e:
        print("❌ Lỗi khi đăng nhập:", e)
        return None
    finally:
        cursor.close()
        conn.close()


# ==============================================
#  HÀM LẤY DỮ LIỆU CHUNG (dành cho CRUD)
def fetch_all(query, params=None):
    conn = get_connection()
    if conn is None:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print("❌ Lỗi truy vấn:", e)
        return []
    finally:
        cursor.close()
        conn.close()


# ==============================================
#  HÀM THỰC HIỆN THÊM/SỬA/XÓA
def execute_query(query, params=None):
    conn = get_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        return True
    except Error as e:
        print("❌ Lỗi khi thực hiện truy vấn:", e)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()
