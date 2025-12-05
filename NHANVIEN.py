# NHANVIEN.py
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

# ===================== THIẾT LẬP MÀU SẮC ======================
BG_COLOR = "#f4f7f6"        # Màu nền tổng thể (Off White/Light Gray)
HEADER_COLOR = "#007bff"    # Màu tiêu đề (Primary Blue)
LABEL_COLOR = "#343a40"     # Màu chữ Label (Dark Gray)
BUTTON_BG = "#28a745"       # Màu nền nút Thêm (Success Green)
BUTTON_FG = "white"
FRAME_BG = "#ffffff"        # Màu nền Frame thông tin (White)
ACCENT_COLOR = "#dc3545"    # Màu nhấn (Error/Delete)
FONT_STYLE = "Times New Roman"


def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="qli_chxm"
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi Kết nối DB", f"Không thể kết nối CSDL: {err}")
        return None


def center_window(win, w=1000, h=650):
    """Đặt cửa sổ vào giữa màn hình."""
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f"{w}x{h}+{x}+{y}")


def show(parent):
    win = tk.Toplevel(parent)
    win.title("Quản lý NHÂN VIÊN")
    center_window(win, 1000, 650)
    win.configure(bg=BG_COLOR)
    win.transient(parent) # Đặt form con luôn nằm trên form cha
    

    tk.Label(win, text="QUẢN LÝ THÔNG TIN NHÂN VIÊN", 
             font=(FONT_STYLE, 18, "bold"), 
             bg=HEADER_COLOR, fg="white", 
             pady=10).pack(fill=tk.X)


    top_frame = tk.Frame(win, bg=BG_COLOR)
    top_frame.pack(fill="x", padx=20, pady=15)


    frame_info = tk.LabelFrame(top_frame, text="📝 Chi tiết Nhân viên", 
                               font=(FONT_STYLE, 13, "bold"), 
                               padx=25, pady=15, bg=FRAME_BG, fg=HEADER_COLOR)
    frame_info.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
    # Cấu hình để Entry mở rộng
    frame_info.grid_columnconfigure(1, weight=1) 
    
    label_font = (FONT_STYLE, 12)
    entry_font = (FONT_STYLE, 12)

    fields = [
        ("Mã NV", 0, 0, 'Entry'), 
        ("Tên NV", 1, 0, 'Entry'), 
        ("Giới tính", 2, 0, 'Combo'), 
        ("Ngày sinh (YYYY-MM-DD)", 3, 0, 'Entry'),
        ("Địa chỉ", 4, 0, 'Entry'),
        ("Điện thoại", 5, 0, 'Entry'),
        ("Tên đăng nhập", 6, 0, 'Entry'), 
        ("Mật khẩu", 7, 0, 'Entry'), 
        ("Vai trò", 8, 0, 'Combo')
    ]
    
    entries_dict = {}
    
    for row, (text, row_num, col_num, input_type) in enumerate(fields):
        tk.Label(frame_info, text=text, font=label_font, bg=FRAME_BG, fg=LABEL_COLOR).grid(
            row=row_num, column=col_num * 2, sticky="e", pady=5, padx=5)
        
        if input_type == 'Entry':
            if text == 'Mật khẩu':
                entry = tk.Entry(frame_info, font=entry_font, show="*")
            else:
                entry = tk.Entry(frame_info, font=entry_font)
            entries_dict[text] = entry
            
        elif input_type == 'Combo':
            values = []
            if text == 'Giới tính':
                values = ["Nam", "Nữ", "Khác"]
            elif text == 'Vai trò':
                values = ["Quan Ly", "Nhân viên"]
            entry = ttk.Combobox(frame_info, values=values, font=entry_font, state="readonly", width=20)
            entries_dict[text] = entry

        entry.grid(row=row_num, column=col_num * 2 + 1, padx=(10, 20), pady=5, sticky="ew")

    # Gán biến dễ dùng
    entry_manv = entries_dict["Mã NV"]
    entry_tennv = entries_dict["Tên NV"]
    cbb_gioitinh = entries_dict["Giới tính"]
    entry_diachi = entries_dict["Địa chỉ"]
    entry_dienthoai = entries_dict["Điện thoại"]
    entry_ngaysinh = entries_dict["Ngày sinh (YYYY-MM-DD)"]
    entry_tendangnhap = entries_dict["Tên đăng nhập"]
    entry_matkhau = entries_dict["Mật khẩu"]
    cbb_vaitro = entries_dict["Vai trò"]



    frame_btn = tk.Frame(top_frame, bg=BG_COLOR)
    frame_btn.grid(row=0, column=1, sticky="n") 
    btn_font = (FONT_STYLE, 12, "bold")

    
    def clear_input():
        for e in [entry_manv, entry_tennv, entry_diachi, entry_dienthoai, entry_ngaysinh, entry_tendangnhap, entry_matkhau]:
            e.delete(0, tk.END)
        cbb_gioitinh.set('')
        cbb_vaitro.set('')


    def load_data():
        for i in tree.get_children():
            tree.delete(i)
        conn = connect_db()
        if not conn: return
        try:
            cur = conn.cursor()

            cur.execute("SELECT MaNV, TenNV, GioiTinh, DiaChi, DienThoai, DATE_FORMAT(NgaySinh, '%Y-%m-%d'), TenDangNhap, VaiTro FROM NHANVIEN")
            for row in cur.fetchall():
                tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Lỗi tải dữ liệu", str(e))
        finally:
            if conn and conn.is_connected():
                conn.close()

    def validate_and_get_data(is_update=False):

        data = {
            'MaNV': entry_manv.get().strip(),
            'TenNV': entry_tennv.get().strip(),
            'GioiTinh': cbb_gioitinh.get().strip(),
            'DiaChi': entry_diachi.get().strip(),
            'DienThoai': entry_dienthoai.get().strip(),
            'NgaySinh': entry_ngaysinh.get().strip(),
            'TenDangNhap': entry_tendangnhap.get().strip(),
            'MatKhau': entry_matkhau.get().strip(),
            'VaiTro': cbb_vaitro.get().strip()
        }
        
        if not all([data['MaNV'], data['TenNV'], data['GioiTinh'], data['DienThoai'], data['TenDangNhap'], data['VaiTro']]):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ các trường bắt buộc.")
            return None
        
        if not is_update and not data['MatKhau']:
            messagebox.showwarning("Thiếu thông tin", "Mật khẩu không được để trống khi Thêm mới.")
            return None
        
        try:
            # Kiểm tra định dạng ngày sinh
            datetime.strptime(data['NgaySinh'], "%Y-%m-%d") 
        except ValueError:
            messagebox.showwarning("Lỗi dữ liệu", "Ngày sinh không hợp lệ hoặc sai định dạng (YYYY-MM-DD).")
            return None
            
        return data

    def them_nv():
        data = validate_and_get_data(is_update=False)
        if not data: return
        
        conn = connect_db()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO NHANVIEN (MaNV, TenNV, GioiTinh, DiaChi, DienThoai, NgaySinh, TenDangNhap, MatKhau, VaiTro)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, tuple(data.values()))
            
            conn.commit()
            messagebox.showinfo("Thành công", f"Đã thêm nhân viên **{data['MaNV']}**.")
            load_data()
            clear_input()
        except mysql.connector.errors.IntegrityError:
            messagebox.showerror("Lỗi", "Mã NV hoặc Tên đăng nhập đã tồn tại!")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            if conn and conn.is_connected(): conn.close()

    def sua_nv():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Chọn dòng", "Hãy chọn nhân viên để sửa")
            return

        item_id = sel[0]
        ma_nv_cu = tree.item(item_id)['values'][0] 

        data = validate_and_get_data(is_update=True)
        if not data: return
        
        # Nếu MaNV bị thay đổi, ta cần đảm bảo tính duy nhất
        if data['MaNV'] != ma_nv_cu:
            messagebox.showwarning("Cảnh báo", "Bạn không được thay đổi Mã NV. Hãy hủy và chọn lại.")
            return

        conn = connect_db()
        if not conn: return
        try:
            cur = conn.cursor()
            
            if data['MatKhau']:
               
                sql = """UPDATE NHANVIEN
                         SET MaNV=%s, TenNV=%s, GioiTinh=%s, DiaChi=%s, DienThoai=%s, NgaySinh=%s, TenDangNhap=%s, MatKhau=%s, VaiTro=%s
                         WHERE MaNV=%s"""
                params = (data['MaNV'], data['TenNV'], data['GioiTinh'], data['DiaChi'], data['DienThoai'], data['NgaySinh'], data['TenDangNhap'], data['MatKhau'], data['VaiTro'], ma_nv_cu)
            else:
                
                sql = """UPDATE NHANVIEN
                         SET MaNV=%s, TenNV=%s, GioiTinh=%s, DiaChi=%s, DienThoai=%s, NgaySinh=%s, TenDangNhap=%s, VaiTro=%s
                         WHERE MaNV=%s"""
                params = (data['MaNV'], data['TenNV'], data['GioiTinh'], data['DiaChi'], data['DienThoai'], data['NgaySinh'], data['TenDangNhap'], data['VaiTro'], ma_nv_cu)

            cur.execute(sql, params)
            conn.commit()
            
            messagebox.showinfo("Thành công", f"Đã cập nhật thông tin NV **{ma_nv_cu}**.")
            load_data() 
            clear_input()

        except mysql.connector.errors.IntegrityError:
            messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại!")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            if conn and conn.is_connected(): conn.close()
    
    def xoa_nv():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Chọn dòng", "Hãy chọn nhân viên để xóa")
            return
            
        manv = tree.item(sel[0])["values"][0]
        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa nhân viên **{manv}**?"):
            return
            
        conn = connect_db()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM NHANVIEN WHERE MaNV=%s", (manv,))
            conn.commit()
            messagebox.showinfo("Thành công", f"Đã xóa nhân viên **{manv}**.")
            load_data()
            clear_input()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            if conn and conn.is_connected(): conn.close()

    def thoat():
        win.destroy()
    
    # Buttons
    #Them xoa sua huy
    tk.Button(frame_btn, text="➕ Thêm", width=14, font=btn_font, command=them_nv, bg=BUTTON_BG, fg=BUTTON_FG).pack(pady=7)
    tk.Button(frame_btn, text="✏️ Sửa", width=14, font=btn_font, command=sua_nv, bg="#ffc107", fg=LABEL_COLOR).pack(pady=7)
    tk.Button(frame_btn, text="🗑️ Xóa", width=14, font=btn_font, command=xoa_nv, bg=ACCENT_COLOR, fg=BUTTON_FG).pack(pady=7)
    tk.Button(frame_btn, text="🔄 Hủy/Tải lại", width=14, font=btn_font, command=lambda: [clear_input(), load_data()], bg="#6c757d", fg=BUTTON_FG).pack(pady=7)
    tk.Button(frame_btn, text="🚪 Thoát", width=14, font=btn_font, command=thoat, bg="#343a40", fg=BUTTON_FG).pack(pady=7)
    

    columns = ("MaNV", "TenNV", "GioiTinh", "DiaChi", "DienThoai", "NgaySinh", "TenDangNhap", "VaiTro")
    
    # Tạo Scrollbar
    vsb = ttk.Scrollbar(win, orient="vertical")
    
    # Cấu hình Style cho Treeview đẹp hơn
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Treeview.Heading", font=(FONT_STYLE, 12, 'bold'), background=HEADER_COLOR, foreground="white")
    style.configure("Treeview", font=(FONT_STYLE, 11), rowheight=25)
    
    tree = ttk.Treeview(win, columns=columns, show="headings", height=12, yscrollcommand=vsb.set)
    vsb.config(command=tree.yview)

    vsb.pack(side='right', fill='y', padx=(0, 20))
    tree.pack(padx=(20, 0), pady=10, fill="both", expand=True)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    # Điều chỉnh độ rộng một số cột quan trọng
    tree.column("DiaChi", width=150, anchor="w")
    tree.column("TenNV", width=150, anchor="w")
    
    # Tree select
    def on_tree_select(event):
        sel = tree.selection()
        if not sel: return
        
        values = tree.item(sel[0])["values"]
        clear_input() 

        entry_manv.insert(0, values[0])
        entry_tennv.insert(0, values[1])
        cbb_gioitinh.set(values[2])
        entry_diachi.insert(0, values[3])
        entry_dienthoai.insert(0, values[4])
        entry_ngaysinh.insert(0, values[5])
        entry_tendangnhap.insert(0, values[6])
        cbb_vaitro.set(values[7])
        
        # Mật khẩu không được load vào form vì lý do bảo mật.
        # Khi sửa, người dùng phải nhập lại nếu muốn thay đổi.

    tree.bind("<<TreeviewSelect>>", on_tree_select)

    load_data()
    return win