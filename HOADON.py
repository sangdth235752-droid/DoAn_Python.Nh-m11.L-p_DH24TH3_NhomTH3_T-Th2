import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

# ===================== MÀU SẮC ĐỒNG BỘ ======================
BG_COLOR = "#f0f8ff"       # Nền tổng thể (Alice Blue)
HEADER_BG = "#4682b4"       # Tiêu đề (Steel Blue)
HEADER_FG = "white"         # Chữ tiêu đề
FRAME_BG = "#e9f5ff"        # Nền LabelFrame
BTN_COLOR = "#5cb85c"       # Nút chính (Thêm)
BTN_FG = "white"             # Chữ nút
ACCENT_COLOR = "#dc3545"    # Nút Xóa
FONT_FAMILY = "Segoe UI"     # Font chung

# ===================== KẾT NỐI DATABASE ======================
def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="qli_chxm"
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi DB", f"Không thể kết nối CSDL: {err}")
        return None

# ===================== CĂN GIỮA CỬA SỔ ======================
def center_window(win, w=1000, h=700):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f"{w}x{h}+{x}+{y}")

# ===================== SHOW HÓA ĐƠN =========================
def show(parent):
    win = tk.Toplevel(parent)
    win.title("Quản lý HÓA ĐƠN")
    win.configure(bg=BG_COLOR)
    center_window(win, 1000, 700)
    win.transient(parent)

    # ===== TIÊU ĐỀ =====
    tk.Label(win, text="QUẢN LÝ HÓA ĐƠN", font=(FONT_FAMILY, 16, "bold"),
             bg=HEADER_BG, fg=HEADER_FG, height=2).pack(fill="x", pady=(0,10))

    # ===== FRAME CHỨA FORM + NÚT =====
    top_frame = tk.Frame(win, bg=BG_COLOR)
    top_frame.pack(fill="x", padx=10, pady=10)

    # ===== FRAME THÔNG TIN HÓA ĐƠN (LEFT) =====
    frame_info = tk.LabelFrame(top_frame, text="Thông tin Hóa đơn",
                               font=(FONT_FAMILY, 12, "bold"),
                               padx=15, pady=10, bg=FRAME_BG, fg=HEADER_BG,
                               labelanchor="n")
    frame_info.pack(side="left", fill="x", expand=True, padx=(0,20))

    labels = ["Mã HĐ", "Ngày lập (YYYY-MM-DD)", "Mã KH", "Mã SP (Mã Xe)",
              "Số lượng", "Đơn giá", "Ghi chú"]
    entries = {}
    label_font = (FONT_FAMILY, 10)
    entry_font = (FONT_FAMILY, 10)

    for i, text in enumerate(labels):
        tk.Label(frame_info, text=text, font=label_font, bg=FRAME_BG).grid(
            row=i//2, column=(i%2)*2, sticky="e", pady=5, padx=5)
        entry = tk.Entry(frame_info, width=25, font=entry_font)
        entry.grid(row=i//2, column=(i%2)*2+1, padx=10, pady=5, sticky="w")
        entries[text] = entry

    # Căn chỉnh Ghi chú
    entries["Ghi chú"].grid(row=3, column=1, columnspan=3, padx=10, pady=5, sticky="ew")
    frame_info.grid_columnconfigure(3, weight=1)

    # ===== FRAME NÚT CHỨC NĂNG (RIGHT) =====
    frame_btn = tk.Frame(top_frame, bg=BG_COLOR)
    frame_btn.pack(side="right", padx=10, pady=10)
    btn_font = (FONT_FAMILY, 10, "bold")

    # ================= TREEVIEW STYLE =================
    style = ttk.Style(win)
    style.theme_use("clam")
    style.configure("Treeview.Heading", font=(FONT_FAMILY, 10, 'bold'),
                    background=HEADER_BG, foreground=HEADER_FG)
    style.configure("Treeview", font=(FONT_FAMILY, 10), rowheight=25)

    # ================= TREEVIEW =================
    columns = ("MaHD", "NgayLap", "MaKH", "MaSP", "SL", "DonGia", "ThanhTien", "GhiChu")
    lbl_ds = tk.Label(win, text="Danh sách Hóa đơn", font=(FONT_FAMILY, 12, "bold"),
                      bg=BG_COLOR)
    lbl_ds.pack(pady=5, anchor="w", padx=10)

    tree_frame = tk.Frame(win)
    tree_frame.pack(padx=10, pady=5, fill="both", expand=True)
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.pack(side='right', fill='y')
    tree.pack(side='left', fill="both", expand=True)

    for col in columns:
        tree.heading(col, text=col)
    tree.column("MaHD", width=80, anchor="center")
    tree.column("NgayLap", width=110, anchor="center")
    tree.column("MaKH", width=80, anchor="center")
    tree.column("MaSP", width=80, anchor="center")
    tree.column("SL", width=60, anchor="center")
    tree.column("DonGia", width=120, anchor="e")
    tree.column("ThanhTien", width=150, anchor="e")
    tree.column("GhiChu", width=200, anchor="w")

    # ================= HÀM XỬ LÝ DỮ LIỆU =================
    def clear_input():
        for e in entries.values(): e.delete(0, tk.END)
        tree.selection_remove(tree.selection())

    def load_data():
        tree.delete(*tree.get_children())
        conn = connect_db()
        if not conn: return
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM HD")
            for row in cur.fetchall():
                ngay_str = row['NgayLap'].strftime("%Y-%m-%d") if isinstance(row['NgayLap'], datetime) else str(row['NgayLap'])
                tree.insert("", "end", values=(
                    row['MaHD'], ngay_str, row['MaKH'], row['MaSP'], row['SL'],
                    "{:,.0f}".format(row['DonGia']),
                    "{:,.0f}".format(row['ThanhTien']),
                    row['GhiChu']
                ))
        except Exception as e:
            messagebox.showerror("Lỗi tải dữ liệu", str(e))
        finally:
            if conn and conn.is_connected(): conn.close()

    def validate_and_get_data(is_update=False):
        data = {}
        try:
            data['mahd'] = entries["Mã HĐ"].get().strip()
            data['ngaylap'] = entries["Ngày lập (YYYY-MM-DD)"].get().strip()
            data['makh'] = entries["Mã KH"].get().strip()
            data['masp'] = entries["Mã SP (Mã Xe)"].get().strip()
            sl_str = entries["Số lượng"].get().strip()
            dongia_str = entries["Đơn giá"].get().strip().replace('.', '').replace(',', '')
            data['ghichu'] = entries["Ghi chú"].get().strip()

            if not all([data['mahd'], data['ngaylap'], data['makh'], data['masp'], sl_str, dongia_str]):
                messagebox.showwarning("Thiếu thông tin", "Nhập đầy đủ Mã HĐ, Ngày lập, Mã KH, Mã SP, Số lượng, Đơn giá.")
                return None

            datetime.strptime(data['ngaylap'], "%Y-%m-%d")
            data['sl'] = int(sl_str)
            data['dongia'] = float(dongia_str)
            if data['sl'] <=0 or data['dongia'] <=0:
                messagebox.showerror("Lỗi nhập liệu", "Số lượng và Đơn giá phải >0.")
                return None
            data['thanhtien'] = data['sl'] * data['dongia']
            return data
        except ValueError:
            messagebox.showerror("Lỗi nhập liệu", "Số lượng/Đơn giá phải số. Ngày lập YYYY-MM-DD.")
            return None
        except Exception as e:
            messagebox.showerror("Lỗi nhập liệu", str(e))
            return None

    def them_hd():
        data = validate_and_get_data()
        if not data: return
        conn = connect_db()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO HD (MaHD, NgayLap, MaKH, MaSP, SL, DonGia, ThanhTien, GhiChu) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                        (data['mahd'], data['ngaylap'], data['makh'], data['masp'], data['sl'], data['dongia'], data['thanhtien'], data['ghichu']))
            conn.commit()
            load_data(); clear_input()
            messagebox.showinfo("Thành công", f"Đã thêm hóa đơn {data['mahd']}")
        except mysql.connector.errors.IntegrityError as e:
            if "Duplicate entry" in str(e):
                messagebox.showerror("Lỗi", f"Mã HĐ {data['mahd']} đã tồn tại hoặc Mã KH/SP không hợp lệ.")
            else:
                messagebox.showerror("Lỗi", str(e))
        finally:
            if conn and conn.is_connected(): conn.close()

    def sua_hd():
        sel = tree.selection()
        if not sel: messagebox.showwarning("Chọn dòng", "Chọn hóa đơn để sửa"); return
        original_mahd = tree.item(sel[0])['values'][0]
        data = validate_and_get_data(is_update=True)
        if not data: return
        conn = connect_db();  
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("UPDATE HD SET MaHD=%s, NgayLap=%s, MaKH=%s, MaSP=%s, SL=%s, DonGia=%s, ThanhTien=%s, GhiChu=%s WHERE MaHD=%s",
                        (data['mahd'], data['ngaylap'], data['makh'], data['masp'], data['sl'], data['dongia'], data['thanhtien'], data['ghichu'], original_mahd))
            conn.commit(); load_data(); clear_input()
            messagebox.showinfo("Thành công", f"Đã cập nhật hóa đơn {original_mahd}")
        except mysql.connector.errors.IntegrityError as e:
            messagebox.showerror("Lỗi cập nhật", str(e))
        finally:
            if conn and conn.is_connected(): conn.close()

    def xoa_hd():
        sel = tree.selection()
        if not sel: messagebox.showwarning("Chọn dòng", "Chọn hóa đơn để xóa"); return
        mahd = tree.item(sel[0])['values'][0]
        if messagebox.askyesno("Xác nhận", f"Xóa hóa đơn {mahd}?"):
            conn = connect_db();  
            if not conn: return
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM HD WHERE MaHD=%s", (mahd,))
                conn.commit(); load_data(); clear_input()
                messagebox.showinfo("Thành công", f"Đã xóa hóa đơn {mahd}")
            finally:
                if conn and conn.is_connected(): conn.close()

    def on_tree_select(event):
        sel = tree.selection();  
        if not sel: return
        item = tree.item(sel[0]); values = item['values']; clear_input()
        keys = ["Mã HĐ","Ngày lập (YYYY-MM-DD)","Mã KH","Mã SP (Mã Xe)","Số lượng","Đơn giá","Ghi chú"]
        tree_indices = [0,1,2,3,4,5,7]
        for key,index in zip(keys,tree_indices):
            entry = entries.get(key)
            if entry:
                val = str(values[index]).replace(',','').replace('.','') if index==5 else values[index]
                entry.insert(0,val)

    tree.bind("<<TreeviewSelect>>", on_tree_select)

    # ===== NÚT =====
    btn_style = {'width':15, 'font':btn_font, 'activebackground':'#00695c', 'activeforeground':'white'}
    tk.Button(frame_btn, text="➕ Thêm", command=them_hd, bg=BTN_COLOR, fg=BTN_FG, **btn_style).pack(pady=5)
    tk.Button(frame_btn, text="✏️ Sửa", command=sua_hd, bg="#ffc107", fg="black", **btn_style).pack(pady=5)
    tk.Button(frame_btn, text="🗑️ Xóa", command=xoa_hd, bg=ACCENT_COLOR, fg=BTN_FG, **btn_style).pack(pady=5)
    tk.Button(frame_btn, text="🔄 Tải lại/Hủy", command=lambda:[clear_input(), load_data()], bg="#6c757d", fg=BTN_FG, **btn_style).pack(pady=5)
    tk.Button(frame_btn, text="🚪 Thoát", command=win.destroy, bg="#343a40", fg=BTN_FG, **btn_style).pack(pady=5)

    load_data()
    win.protocol("WM_DELETE_WINDOW", win.destroy)
    win.grab_set()
    win.wait_window()
