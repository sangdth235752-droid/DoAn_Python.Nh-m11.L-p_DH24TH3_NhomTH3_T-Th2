import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# ===================== MÀU SẮC ======================
BG_COLOR = "#eef6ff"
HEADER_BG = "#005f99"
HEADER_FG = "white"
FRAME_BG = "#ffffff"
BTN_COLOR = "#28a745"
ACCENT_COLOR = "#dc3545"
FONT_FAMILY = "Segoe UI"

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

# ===================== SHOW FORM =========================
def show(parent):
    win = tk.Toplevel(parent)
    win.title("Quản lý HÓA ĐƠN")
    win.configure(bg=BG_COLOR)
    center_window(win)

    # ===== TIÊU ĐỀ =====
    tk.Label(win, text="QUẢN LÝ HÓA ĐƠN", font=(FONT_FAMILY, 18, "bold"),
             bg=HEADER_BG, fg=HEADER_FG, height=2).pack(fill="x", pady=(0, 10))

    # ===== FRAME CHÍNH =====
    main_frame = tk.Frame(win, bg=BG_COLOR)
    main_frame.pack(fill="both", expand=True, padx=15, pady=10)

    # ======================= FORM NHẬP ==========================
    form_frame = tk.LabelFrame(main_frame, text="Thông tin Hóa đơn",
                               font=(FONT_FAMILY, 12, "bold"),
                               bg=FRAME_BG, fg=HEADER_BG, padx=20, pady=15)
    form_frame.pack(fill="x", pady=10)

    labels = [
        "Mã HĐ", "Ngày lập (YYYY-MM-DD)",
        "Mã KH", "Mã SP (Mã Xe)",
        "Số lượng", "Đơn giá",
        "Ghi chú"
    ]

    entries = {}
    row = 0

    for label in labels:
        tk.Label(form_frame, text=label, font=(FONT_FAMILY, 10, "bold"),
                 bg=FRAME_BG).grid(row=row, column=0, sticky="e", pady=8, padx=10)

        if label in ["Mã SP (Mã Xe)", "Mã KH"]:
            cbo = ttk.Combobox(form_frame, font=(FONT_FAMILY, 10), width=27, state="readonly")
            cbo.grid(row=row, column=1, pady=8, sticky="w")
            entries[label] = cbo
        else:
            e = tk.Entry(form_frame, font=(FONT_FAMILY, 10), width=30)
            e.grid(row=row, column=1, pady=8, sticky="w")
            entries[label] = e

        row += 1

    # ================== LOAD MÃ SP ==================
    def load_masp():
        conn = connect_db()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("SELECT MaSP FROM XE ORDER BY MaSP")
            masp_list = [row[0] for row in cur.fetchall()]
            entries["Mã SP (Mã Xe)"]["values"] = masp_list
        finally:
            conn.close()

    # ================== LOAD MÃ KH ==================
    def load_makh():
        conn = connect_db()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("SELECT MaKhach FROM khachhang ORDER BY MaKhach")
            makh_list = [row[0] for row in cur.fetchall()]
            entries["Mã KH"]["values"] = makh_list
        finally:
            conn.close()

    load_masp()
    load_makh()

    # ================== TỰ ĐIỀN ĐƠN GIÁ KHI CHỌN MÃ XE ==================
    def auto_fill_dongia(event):
        masp = entries["Mã SP (Mã Xe)"].get()
        if masp == "":
            entries["Đơn giá"].delete(0, tk.END)
            return

        conn = connect_db()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("SELECT DonGia FROM XE WHERE MaSP=%s", (masp,))
            dg = cur.fetchone()
            if dg:
                entries["Đơn giá"].delete(0, tk.END)
                entries["Đơn giá"].insert(0, str(dg[0]))
        finally:
            conn.close()

    entries["Mã SP (Mã Xe)"].bind("<<ComboboxSelected>>", auto_fill_dongia)

    # ==================== FRAME NÚT ======================
    btn_frame = tk.Frame(main_frame, bg=BG_COLOR)
    btn_frame.pack(fill="x", pady=10)

    btn_style = {
        "width": 15,
        "font": (FONT_FAMILY, 11, "bold"),
        "bd": 0,
        "height": 1,
        "cursor": "hand2"
    }

    btn_add = tk.Button(btn_frame, text="➕ Thêm", bg=BTN_COLOR, fg="white", **btn_style)
    btn_edit = tk.Button(btn_frame, text="✏️ Sửa", bg="#ffc107", fg="black", **btn_style)
    btn_delete = tk.Button(btn_frame, text="🗑 Xóa", bg=ACCENT_COLOR, fg="white", **btn_style)
    btn_reload = tk.Button(btn_frame, text="🔄 Tải lại / Hủy", bg="#6c757d", fg="white", **btn_style)
    btn_exit = tk.Button(btn_frame, text="🚪 Thoát", bg="#343a40", fg="white", **btn_style)

    btn_add.pack(side="left", padx=10)
    btn_edit.pack(side="left", padx=10)
    btn_delete.pack(side="left", padx=10)
    btn_reload.pack(side="left", padx=10)
    btn_exit.pack(side="right", padx=10)

    # ======================= TREEVIEW ======================
    tk.Label(main_frame, text="Danh sách hóa đơn", font=(FONT_FAMILY, 12, "bold"),
             bg=BG_COLOR).pack(anchor="w")

    tree_frame = tk.Frame(main_frame, bg=BG_COLOR)
    tree_frame.pack(fill="both", expand=True)

    columns = ("MaHD", "NgayLap", "MaKH", "MaSP", "SL", "DonGia", "ThanhTien", "GhiChu")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)

    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=110)

    # ==================== LOAD DATA ======================
    def load_data():
        tree.delete(*tree.get_children())
        conn = connect_db()
        if not conn:
            return
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM HD")
            for row in cur.fetchall():
                tree.insert("", "end", values=(
                    row["MaHD"], row["NgayLap"], row["MaKH"],
                    row["MaSP"], row["SL"], row["DonGia"],
                    row["ThanhTien"], row["GhiChu"]
                ))
        finally:
            conn.close()

    load_data()

    # ==================== ĐỔ FORM KHI CHỌN TREEVIEW ====================
    def fill_to_form(event):
        selected = tree.focus()
        if not selected:
            return
        values = tree.item(selected, "values")
        if not values:
            return

        entries["Mã HĐ"].delete(0, tk.END)
        entries["Mã HĐ"].insert(0, values[0])

        entries["Ngày lập (YYYY-MM-DD)"].delete(0, tk.END)
        entries["Ngày lập (YYYY-MM-DD)"].insert(0, values[1])

        entries["Mã KH"].set(values[2])
        entries["Mã SP (Mã Xe)"].set(values[3])

        entries["Số lượng"].delete(0, tk.END)
        entries["Số lượng"].insert(0, values[4])

        entries["Đơn giá"].delete(0, tk.END)
        entries["Đơn giá"].insert(0, values[5])

        entries["Ghi chú"].delete(0, tk.END)
        entries["Ghi chú"].insert(0, values[7])

    tree.bind("<<TreeviewSelect>>", fill_to_form)

    # ==================== HÀM CRUD ======================
    def clear_form():
        for e in entries.values():
            if isinstance(e, ttk.Combobox):
                e.set("")
            else:
                e.delete(0, tk.END)
        load_data()
#them
    def add_data():
        MaHD = entries["Mã HĐ"].get().strip()
        NgayLap = entries["Ngày lập (YYYY-MM-DD)"].get().strip()
        MaKH = entries["Mã KH"].get().strip()
        MaSP = entries["Mã SP (Mã Xe)"].get().strip()
        SL = entries["Số lượng"].get().strip()
        DonGia = entries["Đơn giá"].get().strip()
        GhiChu = entries["Ghi chú"].get().strip()

        if "" in [MaHD, NgayLap, MaKH, MaSP, SL, DonGia]:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin!")
            return

        try:
            SL_int = int(SL)
            DonGia_int = int(DonGia)
        except ValueError:
            messagebox.showwarning("Lỗi định dạng", "Số lượng và Đơn giá phải là số nguyên!")
            return

        ThanhTien = SL_int * DonGia_int

        conn = connect_db()
        if not conn:
            return

        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO HD (MaHD, NgayLap, MaKH, MaSP, SL, DonGia, ThanhTien, GhiChu)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """, (MaHD, NgayLap, MaKH, MaSP, SL_int, DonGia_int, ThanhTien, GhiChu))
            conn.commit()
            clear_form()  # Bỏ messagebox
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi cơ sở dữ liệu: {e}")
        finally:
            conn.close()

    def edit_data():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Chọn dòng", "Hãy chọn hóa đơn cần sửa!")
            return

        MaHD = entries["Mã HĐ"].get().strip()
        NgayLap = entries["Ngày lập (YYYY-MM-DD)"].get().strip()
        MaKH = entries["Mã KH"].get().strip()
        MaSP = entries["Mã SP (Mã Xe)"].get().strip()
        SL = entries["Số lượng"].get().strip()
        DonGia = entries["Đơn giá"].get().strip()
        GhiChu = entries["Ghi chú"].get().strip()

        try:
            SL_int = int(SL)
            DonGia_int = int(DonGia)
        except ValueError:
            messagebox.showwarning("Lỗi định dạng", "Số lượng và Đơn giá phải là số nguyên!")
            return

        ThanhTien = SL_int * DonGia_int

        conn = connect_db()
        if not conn:
            return

        try:
            cur = conn.cursor()
            cur.execute("""
                UPDATE HD SET NgayLap=%s, MaKH=%s, MaSP=%s,
                SL=%s, DonGia=%s, ThanhTien=%s, GhiChu=%s
                WHERE MaHD=%s
            """, (NgayLap, MaKH, MaSP, SL_int, DonGia_int, ThanhTien, GhiChu, MaHD))
            conn.commit()
            clear_form()
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi cơ sở dữ liệu: {e}")
        finally:
            conn.close()

    def delete_data():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Chọn dòng", "Hãy chọn hóa đơn cần xóa!")
            return

        MaHD = tree.item(selected, "values")[0]

        if not messagebox.askyesno("Xác nhận", f"Xóa hóa đơn {MaHD}?"):
            return

        conn = connect_db()
        if not conn:
            return

        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM HD WHERE MaHD=%s", (MaHD,))
            conn.commit()
            clear_form()
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi cơ sở dữ liệu: {e}")
        finally:
            conn.close()

    # GÁN NÚT
    #Button
    btn_add.config(command=add_data)
    btn_edit.config(command=edit_data)
    btn_delete.config(command=delete_data)
    btn_reload.config(command=clear_form)
    btn_exit.config(command=win.destroy)

    win.mainloop()


# Nếu chạy trực tiếp
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Main window")
    root.geometry("300x100")
    btn = tk.Button(root, text="Quản lý Hóa Đơn", command=lambda: show(root))
    btn.pack(pady=20)
    root.mainloop()
