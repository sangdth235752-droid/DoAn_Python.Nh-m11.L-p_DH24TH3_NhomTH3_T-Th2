# KHACHHANG.py
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# ===================== THIẾT LẬP MÀU SẮC & FONT ======================
BG_COLOR = "#e8f9fd"        # Màu nền tổng thể (Light Cyan)
HEADER_COLOR = "#00bcd4"    # Màu tiêu đề (Cyan - Clean Look)
LABEL_COLOR = "#2c3e50"     # Màu chữ Label (Dark Blue)
BUTTON_BG_ADD = "#4caf50"   # Màu nền nút Thêm (Green)
BUTTON_BG_EDIT = "#ffc107"  # Màu nền nút Sửa (Amber)
BUTTON_BG_DELETE = "#f44336" # Màu nền nút Xóa (Red)
BUTTON_FG = "white"
FRAME_BG = "#ffffff"        # Màu nền Frame thông tin (White)
FONT_STYLE = "Times New Roman"

# ===================== KẾT NỐI DATABASE ======================
def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="qli_chxm",
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi Kết nối DB", f"Không thể kết nối CSDL: {err}")
        return None

# ===================== HÀM CĂN GIỮA ==========================
def center_window(win, w=850, h=600):
    """Đặt cửa sổ vào giữa màn hình."""
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f"{w}x{h}+{x}+{y}")

# ===================== HÀM SHOW KHÁCH HÀNG ===================
def show(parent):
    """Hiển thị cửa sổ quản lý khách hàng"""
    win = tk.Toplevel(parent)
    win.title("Quản lý KHÁCH HÀNG")
    center_window(win, 850, 600)
    win.configure(bg=BG_COLOR)
    win.transient(parent)

    # ===== TIÊU ĐỀ =====
    tk.Label(win, text="QUẢN LÝ THÔNG TIN KHÁCH HÀNG", 
             font=(FONT_STYLE, 18, "bold"), 
             bg=HEADER_COLOR, fg="white", 
             pady=10).pack(fill=tk.X)

    # ===== KHUNG CHỨA FORM + NÚT (Sử dụng Grid trong Frame này) =====
    top_container = tk.Frame(win, bg=BG_COLOR)
    top_container.pack(fill="x", padx=20, pady=15)
    
    # Cấu hình container: cột 0 chứa form, cột 1 chứa nút.
    top_container.grid_columnconfigure(0, weight=1)
    
    # ===== FRAME THÔNG TIN KHÁCH HÀNG (LEFT) =====
    frame_info = tk.LabelFrame(top_container, text="👤 Chi tiết khách hàng",
                               font=(FONT_STYLE, 13, "bold"), 
                               padx=20, pady=15, bg=FRAME_BG, fg=HEADER_COLOR)
    frame_info.grid(row=0, column=0, sticky="ew") # sticky="ew" để mở rộng theo chiều ngang
    
    # Cấu hình Entry mở rộng trong frame_info
    frame_info.grid_columnconfigure(1, weight=1)

    label_font = (FONT_STYLE, 12)
    entry_font = (FONT_STYLE, 12)

    # Dictionary lưu Entry
    entries = {}
    
    fields = [
        ("Mã KH", 0), ("Tên KH", 1), 
        ("Địa chỉ", 2), ("Điện thoại", 3)
    ]
    
    for row_num, (text, row_pos) in enumerate(fields):
        tk.Label(frame_info, text=text, font=label_font, bg=FRAME_BG, fg=LABEL_COLOR).grid(
            row=row_pos, column=0, sticky="e", pady=7, padx=10)
        
        entry = tk.Entry(frame_info, font=entry_font, borderwidth=1, relief="solid")
        entry.grid(row=row_pos, column=1, padx=(0, 20), pady=7, sticky="ew")
        entries[text] = entry
        
    # Gán biến dễ dùng
    entry_makhach = entries["Mã KH"]
    entry_tenkhach = entries["Tên KH"]
    entry_diachi = entries["Địa chỉ"]
    entry_dienthoai = entries["Điện thoại"]


    # ===== NÚT CHỨC NĂNG (RIGHT) =====
    frame_btn = tk.Frame(top_container, bg=BG_COLOR)
    frame_btn.grid(row=0, column=1, padx=(20, 0), sticky="n")
    btn_font = (FONT_STYLE, 12, "bold")

    # ================= HÀM XỬ LÝ CHỨC NĂNG =================
    
    def clear_input():
        for e in entries.values():
            e.delete(0, tk.END)
      

    def load_data():
        for i in tree.get_children():
            tree.delete(i)
        conn = connect_db()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("SELECT MaKhach, TenKhach, DiaChi, DienThoai FROM KHACHHANG")
            for row in cur.fetchall():
                tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Lỗi DB", str(e))
        finally:
            if conn and conn.is_connected():
                conn.close()

    def them_kh():
        makh = entry_makhach.get().strip()
        tenkh = entry_tenkhach.get().strip()
        dc = entry_diachi.get().strip()
        dt = entry_dienthoai.get().strip()
        
        if not makh or not tenkh:
            messagebox.showwarning("Thiếu thông tin", "Mã KH và Tên KH bắt buộc!")
            return
            
        conn = connect_db()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO KHACHHANG (MaKhach, TenKhach, DiaChi, DienThoai) VALUES (%s,%s,%s,%s)",
                        (makh, tenkh, dc, dt))
            conn.commit()
            messagebox.showinfo("Thành công", f"Đã thêm khách hàng {tenkh} ({makh}).")
            load_data()
            clear_input()
        except mysql.connector.errors.IntegrityError:
            messagebox.showerror("Lỗi", "Mã khách hàng đã tồn tại!")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            if conn and conn.is_connected():
                conn.close()

    def xoa_kh():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Chọn dòng", "Hãy chọn khách hàng để xóa")
            return
            
        makh = tree.item(sel[0])["values"][0]
        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa khách hàng **{makh}**?"):
            return
            
        conn = connect_db()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM KHACHHANG WHERE MaKhach=%s", (makh,))
            conn.commit()
            messagebox.showinfo("Thành công", f"Đã xóa khách hàng **{makh}**.")
            load_data()
            clear_input()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            if conn and conn.is_connected():
                conn.close()

    def sua_kh():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Chọn dòng", "Hãy chọn khách hàng để sửa")
            return

        item_id = sel[0] 
        makh_cu = tree.item(item_id)['values'][0] # Lấy mã KH cũ
        makh_moi = entry_makhach.get().strip() 
        tenkh = entry_tenkhach.get().strip()
        diachi = entry_diachi.get().strip()
        dienthoai = entry_dienthoai.get().strip()

        if not tenkh:
            messagebox.showwarning("Thiếu thông tin", "Tên khách hàng không được để trống")
            return
        
        if makh_moi != makh_cu:
            messagebox.showwarning("Cảnh báo", "Không được thay đổi Mã KH khi Sửa.")
            return

        conn = connect_db()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("""
                UPDATE KHACHHANG
                SET TenKhach=%s, DiaChi=%s, DienThoai=%s
                WHERE MaKhach=%s
            """, (tenkh, diachi, dienthoai, makh_cu))
            conn.commit()
            messagebox.showinfo("Thành công", f"Đã cập nhật thông tin KH **{makh_cu}**.")
            
            # Cập nhật trực tiếp dòng đang chọn trong Treeview
            tree.item(item_id, values=(makh_cu, tenkh, diachi, dienthoai))

            # Giữ dòng vừa sửa được chọn
            tree.selection_set(item_id)
            tree.focus(item_id)

        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            if conn and conn.is_connected():
                conn.close()
                
        # Xóa form
        clear_input()

    def thoat():
        win.destroy()

    # ================= NÚT =================
    tk.Button(frame_btn, text="➕ Thêm", width=14, font=btn_font, command=them_kh, 
              bg=BUTTON_BG_ADD, fg=BUTTON_FG).pack(pady=7)
    tk.Button(frame_btn, text="✏️ Sửa", width=14, font=btn_font, command=sua_kh, 
              bg=BUTTON_BG_EDIT, fg=LABEL_COLOR).pack(pady=7)
    tk.Button(frame_btn, text="🗑️ Xóa", width=14, font=btn_font, command=xoa_kh, 
              bg=BUTTON_BG_DELETE, fg=BUTTON_FG).pack(pady=7)
    tk.Button(frame_btn, text="🔄 Hủy/Tải lại", width=14, font=btn_font, command=lambda: [clear_input(), load_data()], 
              bg="#6c757d", fg=BUTTON_FG).pack(pady=7)
    tk.Button(frame_btn, text="🚪 Thoát", width=14, font=btn_font, command=thoat, 
              bg="#343a40", fg=BUTTON_FG).pack(pady=7)

    # ===== TREEVIEW HIỂN THỊ DỮ LIỆU =====
    columns = ("MaKhach", "TenKhach", "DiaChi", "DienThoai")
    
    # Cấu hình Style cho Treeview
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Treeview.Heading", font=(FONT_STYLE, 12, 'bold'), background=HEADER_COLOR, foreground="white")
    style.configure("Treeview", font=(FONT_STYLE, 11), rowheight=25)

    tree = ttk.Treeview(win, columns=columns, show="headings", height=12)
    tree.pack(padx=20, pady=10, fill="both", expand=True)

    for col in columns:
        tree.heading(col, text=col)
    tree.column("MaKhach", width=80, anchor="center")
    tree.column("TenKhach", width=180, anchor="w")
    tree.column("DiaChi", width=250, anchor="w")
    tree.column("DienThoai", width=120, anchor="center")

    # ================= CHỌN DÒNG TREE =================
    # Đoạn code trong file KHACHHANG.py sau khi sửa
# ================= CHỌN DÒNG TREE =================
    def on_tree_select(event):
        sel = tree.selection()
        if not sel:
            return
        values = tree.item(sel[0])["values"]
    
    # Gọi hàm clear_input() để xóa tất cả các trường nhập liệu
        clear_input() 
    
    # Sau đó, chèn dữ liệu của dòng vừa chọn vào các Entry
        entry_makhach.insert(0, values[0])
        entry_tenkhach.insert(0, values[1])
        entry_diachi.insert(0, values[2])
        entry_dienthoai.insert(0, values[3])

    tree.bind("<<TreeviewSelect>>", on_tree_select)
    # Load dữ liệu ban đầu
    load_data()

    return win