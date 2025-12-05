# XE.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
import mysql.connector
import openpyxl
from openpyxl.styles import Font, Alignment
# ===================== THIẾT LẬP MÀU SẮC ======================
BG_COLOR = "#f0f8ff"      # Màu nền tổng thể (Alice Blue)
HEADER_COLOR = "#4682b4"  # Màu tiêu đề (Steel Blue)
LABEL_COLOR = "#333333"   # Màu chữ Label
BUTTON_BG = "#5cb85c"     # Màu nền nút (Green - Success)
BUTTON_FG = "white"       # Màu chữ nút
FRAME_BG = "#e9f5ff"      # Màu nền Frame thông tin
ACCENT_COLOR = "#dc3545"  # Màu nhấn (Error/Delete)

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
        messagebox.showerror("Lỗi DB", f"Không thể kết nối CSDL: {err}")
        return None

# ===================== HÀM CĂN GIỮA ==========================
def center_window(win, w=950, h=650):
    """Đặt cửa sổ vào giữa màn hình."""
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f"{w}x{h}+{x}+{y}")

# ===================== HÀM HIỂN THỊ FORM XE ===================
def show(root):
    win = tk.Toplevel(root)
    win.title("Quản lý XE")
    center_window(win, w=950, h=650)
    win.configure(bg=BG_COLOR)
    win.transient(root) # Đặt form con luôn nằm trên form cha

    # ===== TIÊU ĐỀ =====
    tk.Label(win, text="QUẢN LÝ THÔNG TIN XE", 
             font=("Arial", 18, "bold"), 
             bg=HEADER_COLOR, fg="white", 
             pady=10).pack(fill=tk.X)

    # ===== FRAME THÔNG TIN XE (2 cột nhập liệu) =====
    frame_info = tk.LabelFrame(win, text="📝 Chi tiết sản phẩm", 
                               font=("Times New Roman", 13, "bold"), 
                               padx=20, pady=15, bg=FRAME_BG, fg=HEADER_COLOR)
    frame_info.pack(side="bottom",padx=20, pady=15, fill="x")

    # Đặt trọng số cho cột để Entry mở rộng đẹp hơn
    frame_info.grid_columnconfigure(1, weight=1)
    frame_info.grid_columnconfigure(3, weight=1)

    label_font = ("Times New Roman", 12)
    entry_font = ("Times New Roman", 12)
    
    # Dictionary lưu Entry
    entries = {}
    
    # Danh sách các trường cần nhập liệu
    fields = [
        ("Mã SP", 0, 0), ("Tên SP", 1, 0), 
        ("Loại xe", 2, 0), ("Hãng SX", 0, 2), 
        ("Giá (VND)", 1, 2), ("Số lượng (Kho)", 2, 2)
    ]
    
    for text, row, col in fields:
        tk.Label(frame_info, text=text, font=label_font, bg=FRAME_BG, fg=LABEL_COLOR).grid(
            row=row, column=col, sticky="w", pady=5, padx=(0, 10)) # sticky="w" căn trái Label

        entry = tk.Entry(frame_info, font=entry_font, borderwidth=1, relief="solid")
        # Đặt Entry vào cột tiếp theo và mở rộng theo chiều ngang (sticky="ew")
        entry.grid(row=row, column=col+1, padx=(0, 20), pady=5, sticky="ew")
        entries[text] = entry
        
    # Gán biến Entry cho dễ sử dụng
    entry_masp = entries["Mã SP"]
    entry_tensp = entries["Tên SP"]
    entry_loaixe = entries["Loại xe"]
    entry_hangsx = entries["Hãng SX"]
    entry_gia = entries["Giá (VND)"]
    entry_soluong = entries["Số lượng (Kho)"]

    # ===== FRAME NÚT CHỨC NĂNG =====
     # ===== FRAME NÚT CHỨC NĂNG =====


    btn_font = ("Times New Roman", 13, "bold")
    

    def xuat_excel():
        if not tree.get_children():
            messagebox.showwarning("Không có dữ liệu", "Không có dữ liệu để xuất!")
            return
    
        try:
        # Tạo workbook mới
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Danh sách Xe"

        # Ghi tiêu đề cột
            headers = ["Mã SP", "Tên SP", "Loại Xe", "Hãng SX", "Giá (VND)", "Số lượng (Kho)"]
            for col_num, header in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col_num, value=header)
                cell.font = Font(bold=True)
                cell.alignment = Alignment(horizontal='center')

        # Ghi dữ liệu từ Treeview
            for row_num, item in enumerate(tree.get_children(), 2):
                values = tree.item(item)["values"]
                for col_num, value in enumerate(values, 1):
                    ws.cell(row=row_num, column=col_num, value=value)

        # Tự động căn chỉnh độ rộng cột
            for column_cells in ws.columns:
                length = max(len(str(cell.value)) for cell in column_cells)
                ws.column_dimensions[column_cells[0].column_letter].width = length + 2

        # Lưu file
            file_path = "Danh_sach_xe.xlsx"
            wb.save(file_path)
            messagebox.showinfo("Xuất Excel thành công", f"Đã xuất dữ liệu ra file {file_path}")
    
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất Excel: {e}")

    # ======================= HÀM XỬ LÝ =========================
    
    def load_data():
        tree.delete(*tree.get_children())
        conn = connect_db()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("SELECT MaSP, TenSP, LoaiXe, Hangsx, Gia, SoLuong FROM XE")
            for row in cur.fetchall():
                # Định dạng giá tiền (Ví dụ: 1000000 -> 1,000,000)
                formatted_gia = f"{row[4]:,.0f}" if row[4] is not None else "N/A"
                # Tạo hàng mới với giá đã định dạng
                tree.insert("", "end", values=(row[0], row[1], row[2], row[3], formatted_gia, row[5]))
        except Exception as e:
            messagebox.showerror("Lỗi DB", str(e))
        finally:
            if conn and conn.is_connected():
                conn.close()

    def clear_input():
        for e in entries.values():
            e.delete(0, tk.END)

    def validate_input(is_update=False):
        """Hàm kiểm tra dữ liệu đầu vào."""
        data = {
            'masp': entry_masp.get().strip(),
            'tensp': entry_tensp.get().strip(),
            'loaixe': entry_loaixe.get().strip(),
            'hangsx': entry_hangsx.get().strip(),
        }
        
        if not data['masp'] or not data['tensp']:
            messagebox.showwarning("Thiếu dữ liệu", "Mã SP và Tên SP bắt buộc!")
            return None

        try:
            data['gia'] = float(entry_gia.get().strip().replace(',', ''))
            data['sl'] = int(entry_soluong.get().strip())
        except ValueError:
            messagebox.showwarning("Lỗi dữ liệu", "Giá phải là số, Số lượng phải là số nguyên")
            return None
            
        if data['gia'] < 0 or data['sl'] < 0:
            messagebox.showwarning("Lỗi dữ liệu", "Giá và Số lượng phải lớn hơn hoặc bằng 0.")
            return None

        return data
#thenh xoa sua
    def them():
        data = validate_input()
        if not data: return

        conn = connect_db()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO XE (MaSP, TenSP, LoaiXe, Hangsx, Gia, SoLuong) VALUES (%s,%s,%s,%s,%s,%s)",
                        (data['masp'], data['tensp'], data['loaixe'], data['hangsx'], data['gia'], data['sl']))
            conn.commit()
            messagebox.showinfo("Thành công", f"Đã thêm xe {data['tensp']} ({data['masp']})")
            load_data()
            clear_input()
        except mysql.connector.errors.IntegrityError:
            messagebox.showerror("Lỗi", "Mã SP đã tồn tại!")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            if conn and conn.is_connected(): conn.close()

    def sua():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Chọn dữ liệu", "Hãy chọn xe để sửa")
            return

        item_id = sel[0]
        ma_cu = tree.item(item_id)['values'][0] 
        data = validate_input(is_update=True)
        if not data: return

        if data['masp'] != ma_cu:
            messagebox.showwarning("Cảnh báo", "Không được thay đổi Mã SP khi Sửa. Hãy nhấn Hủy và chọn lại.")
            return

        conn = connect_db()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("UPDATE XE SET TenSP=%s, LoaiXe=%s, Hangsx=%s, Gia=%s, SoLuong=%s WHERE MaSP=%s",
                        (data['tensp'], data['loaixe'], data['hangsx'], data['gia'], data['sl'], ma_cu))
            conn.commit()
            
            # Cập nhật trực tiếp trên Treeview với giá đã định dạng
            formatted_gia = f"{data['gia']:,.0f}"
            tree.item(item_id, values=(ma_cu, data['tensp'], data['loaixe'], data['hangsx'], formatted_gia, data['sl']))
            
            messagebox.showinfo("Thành công", f"Đã cập nhật thông tin xe {ma_cu}")
            clear_input()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            if conn and conn.is_connected(): conn.close()

    def xoa():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Chọn dữ liệu", "Hãy chọn xe để xóa")
            return

        ma = tree.item(sel[0])['values'][0]
        if messagebox.askyesno("Xác nhận", f"Bạn chắc chắn muốn xóa xe {ma}?"):
            conn = connect_db()
            if not conn: return
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM XE WHERE MaSP=%s", (ma,))
                conn.commit()
                load_data()
                clear_input()
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
            finally:
                if conn and conn.is_connected(): conn.close()

    # ===== CHỌN DÒNG TREEVIEW =====
    def on_tree_select(event):
        sel = tree.selection()
        if not sel: return
        
        values = tree.item(sel[0])["values"]
        clear_input() 
        
        # Chuyển đổi giá từ chuỗi định dạng (có dấu phẩy) về dạng số (không dấu phẩy) trước khi hiển thị
        gia_str = str(values[4]).replace(',', '') 
        
        entry_masp.insert(0, values[0])
        entry_tensp.insert(0, values[1])
        entry_loaixe.insert(0, values[2])
        entry_hangsx.insert(0, values[3])
        entry_gia.insert(0, gia_str)
        entry_soluong.insert(0, values[5])


    # ===== TREEVIEW HIỂN THỊ DỮ LIỆU =====
    cols = ("MaSP", "TenSP", "LoaiXe", "Hangsx", "Gia", "SoLuong")
    
    # Tạo Scrollbar dọc
    vsb = ttk.Scrollbar(win, orient="vertical")
    
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Treeview.Heading", font=('Times New Roman', 12, 'bold'), background=HEADER_COLOR, foreground="white")
    style.configure("Treeview", font=('Times New Roman', 11), rowheight=25)
    
    tree = ttk.Treeview(win, columns=cols, show="headings", yscrollcommand=vsb.set)
    vsb.config(command=tree.yview)

    # Đóng gói scrollbar và treeview (sử dụng expand=True để nó chiếm khoảng trống lớn nhất)
    vsb.pack(side='right', fill='y', padx=(0, 20))
    tree.pack(fill="both", expand=True, padx=(20, 0), pady=(10, 5)) # Giảm pady dưới

    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, anchor="center", width=120)
    
    tree.column("Gia", anchor="e", width=150)
    tree.column("TenSP", anchor="w", width=180)

    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, anchor="center", width=120)
    
    # Căn chỉnh cột Giá và Tên SP rộng hơn
    tree.column("Gia", anchor="e", width=150)
    tree.column("TenSP", anchor="w", width=180)
    
    tree.bind("<<TreeviewSelect>>", on_tree_select)
    load_data()
    
    # ===== FRAME NÚT CHỨC NĂNG (Đưa xuống dưới TreeView) =====
    frame_btn = tk.Frame(win, bg=BG_COLOR)
    frame_btn.pack(pady=(10, 15))

    btn_font = ("Times New Roman", 13, "bold")

    tk.Button(frame_btn, text="➕ Thêm", width=12, font=btn_font, command=them, bg=BUTTON_BG, fg=BUTTON_FG).pack(side="left", padx=7)
    tk.Button(frame_btn, text="✏️ Sửa", width=12, font=btn_font, command=sua, bg="#ffc107", fg=LABEL_COLOR).pack(side="left", padx=7)
    tk.Button(frame_btn, text="🗑️ Xóa", width=12, font=btn_font, command=xoa, bg=ACCENT_COLOR, fg=BUTTON_FG).pack(side="left", padx=7)
    tk.Button(frame_btn, text="🔄 Hủy", width=12, font=btn_font, command=clear_input, bg="#6c757d", fg=BUTTON_FG).pack(side="left", padx=7)
    tk.Button(frame_btn, text="🚪 Thoát", width=12, font=btn_font, command=win.destroy, bg="#343a40", fg=BUTTON_FG).pack(side="left", padx=7)
    tk.Button(frame_btn, text="📄 Xuất Excel", width=12, font=btn_font, command=xuat_excel, bg="#17a2b8", fg=BUTTON_FG).pack(side="left", padx=7)

    # Không nên gọi win.mainloop() ở đây, để root.mainloop() trong main.py quản lý
    # win.mainloop() 
    return win