# main.py
import tkinter as tk
from tkinter import messagebox
from XE import show as xe_show
# Chú ý: Đảm bảo các file sau tồn tại và có hàm show(parent)
from NHANVIEN import show as nv_show
from KHACHHANG import show as kh_show
from HOADON import show as hd_show 

# ===================== HÀM CĂN GIỮA =====================
def center_window(win, w=900, h=600):
    """Căn giữa cửa sổ trên màn hình."""
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')

# ===================== HÀM MỞ FORM CHUẨN =====================
def open_form(form_func, root):
    """Mở form Toplevel ở chế độ Modal."""
    try:
        top = form_func(root)
        top.grab_set()         # Ngăn tương tác với cửa sổ cha
        top.focus_set()        # Tập trung vào cửa sổ con
        root.wait_window(top)  # Đợi cửa sổ con đóng
    except Exception as e:
        messagebox.showerror("Lỗi mở form", f"Không thể mở form. Vui lòng kiểm tra file module. Chi tiết: {e}")

# ===================== HÀM XỬ LÝ CHỨC NĂNG =====================

def main_view(user=None):
    """
    Hiển thị giao diện Trang Chủ.
    Nhận thông tin user sau khi đăng nhập thành công.
    """
    # Dữ liệu giả định nếu chạy trực tiếp (Testing)
    if user is None:
        user = {"TenNV": "Admin Test", "TenDangNhap": "admin", "VaiTro": "Quan Ly"} 
        # Hoặc thử user thường: user = {"TenNV": "Nhân viên A", "TenDangNhap": "nv001", "VaiTro": "Nhan Vien"}

    root = tk.Tk()
    root.title("QUẢN LÝ CỬA HÀNG XE MÁY")
    center_window(root, 900, 600)
    root.configure(bg="#e8f0fe") # Nền sáng hơn
    
    # Quyền của người dùng
    user_role = user['VaiTro']

    # --- HÀM XỬ LÝ CHUYÊN BIỆT ---
    def quan_ly_nhan_vien():
        if user_role != 'Quan Ly':
            messagebox.showwarning("Cảnh báo", "Chỉ Quản lý mới được quản lý nhân viên!")
            return
        open_form(nv_show, root)

    def quan_ly_xe():
        open_form(xe_show, root)

    def quan_ly_khach_hang():
        open_form(kh_show, root)

    def quan_ly_hoa_don():
        open_form(hd_show, root)

    def thoat():
        if messagebox.askyesno("Thoát", "Bạn có chắc chắn muốn thoát không?"):
            root.destroy()

    # ================== HEADER/FOOTER ==================
    
    # --- THANH TIÊU ĐỀ THÔNG TIN USER ---
    tk.Label(root, text=f"Xin chào, {user['TenNV']} ({user['TenDangNhap']}) - VAI TRÒ: {user_role}",
             font=("Times New Roman", 14, "bold"), bg="#4287f5", fg="white", anchor="w", padx=10).pack(fill=tk.X, pady=(0, 20))

    # ================== MENU BAR ==================
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    
    # --- Menu Quản Lý ---
    menu_ql = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Chức năng quản lý", menu=menu_ql)
    
    menu_ql.add_command(label="🛵 Quản lý XE", command=quan_ly_xe)
    menu_ql.add_command(label="👥 Quản lý KHÁCH HÀNG", command=quan_ly_khach_hang)
    menu_ql.add_command(label="🧾 Quản lý HÓA ĐƠN", command=quan_ly_hoa_don)
    menu_ql.add_separator()
    
    # Chỉ thêm chức năng Quản lý Nhân viên nếu user là Quản lý
    if user_role == 'Quan Ly':
        menu_ql.add_command(label="🧑‍💼 Quản lý NHÂN VIÊN", command=quan_ly_nhan_vien)
        
    # --- Menu Hệ Thống ---
    menu_hethong = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Hệ thống", menu=menu_hethong)
    menu_hethong.add_command(label="Đăng xuất", command=lambda: [root.destroy(), print("Chuyển đến màn hình Đăng nhập")])
    menu_hethong.add_command(label="🚪 Thoát", command=thoat)


    # ================== KHUNG TRUNG TÂM (BUTTONS) ==================
    
    tk.Label(root, text="CHỌN CHỨC NĂNG", font=("Arial", 18, "bold"), fg="#0a2a66", bg="#e8f0fe").pack(pady=20)
    
    frame_buttons = tk.Frame(root, bg="#e8f0fe")
    frame_buttons.pack(pady=10)

    # Danh sách nút được hiển thị ở trung tâm
    buttons_info = [
        ("🛵 Quản lý XE", quan_ly_xe, "#007bff"),
        ("👥 Quản lý KHÁCH HÀNG", quan_ly_khach_hang, "#28a745"),
        ("🧾 Quản lý HÓA ĐƠN", quan_ly_hoa_don, "#ffc107"),
    ]
    
    if user_role == 'Quan Ly':
        buttons_info.append(("🧑‍💼 Quản lý NHÂN VIÊN", quan_ly_nhan_vien, "#dc3545"))
    
    # Tạo các nút
    for text, cmd, color in buttons_info:
        tk.Button(frame_buttons, text=text, font=("Times New Roman", 14, "bold"),
                  bg=color, fg="white", activebackground="#0056b3", 
                  width=25, height=2, command=cmd).pack(pady=10)

    # Nút Thoát cuối cùng
    tk.Button(root, text="🚪 Thoát chương trình", font=("Times New Roman", 12),
              bg="#6c757d", fg="white", width=20, command=thoat).pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    # Đây là điểm bắt đầu khi chạy main.py
    # Bạn có thể gọi main_view() với thông tin user thật sau khi tích hợp màn hình đăng nhập
    
    # Chạy thử với vai trò Quản lý
    # main_view({"TenNV": "Admin Test", "TenDangNhap": "admin", "VaiTro": "Quan Ly"})
    
    # Chạy thử với vai trò Nhân viên
    main_view({"TenNV": "Nhân viên B", "TenDangNhap": "nv002", "VaiTro": "Nhan Vien"})