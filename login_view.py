import tkinter as tk
from tkinter import messagebox
from database import dang_nhap  # hàm đăng nhập

# Hàm căn giữa cửa sổ cục bộ
def center_window(win, w=700, h=500):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')

def login():
    root = tk.Tk()
    root.title("Đăng nhập")
    center_window(root, 400, 250)
    root.configure(bg="#a8c6ff")

    tk.Label(root, text="ĐĂNG NHẬP HỆ THỐNG",
             font=("Times New Roman", 16, "bold"),
             bg="#457bff", fg="white", pady=10).pack(fill=tk.X)

    frame = tk.Frame(root, bg="#8fb1ff", padx=20, pady=20)
    frame.pack(pady=15)

    tk.Label(frame, text="Tên đăng nhập:", font=("Times New Roman", 12),
             bg="#8fb1ff").grid(row=0, column=0, sticky=tk.E, pady=5)
    username_entry = tk.Entry(frame, font=("Times New Roman", 12))
    username_entry.grid(row=0, column=1, pady=5)

    tk.Label(frame, text="Mật khẩu:", font=("Times New Roman", 12),
             bg="#8fb1ff").grid(row=1, column=0, sticky=tk.E, pady=5)
    password_entry = tk.Entry(frame, font=("Times New Roman", 12), show="*")
    password_entry.grid(row=1, column=1, pady=5)

    def xu_ly_dang_nhap():
        ten = username_entry.get().strip()
        mk = password_entry.get().strip()

        if not ten or not mk:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu!")
            return

        user = dang_nhap(ten, mk)
        if user:
            messagebox.showinfo("Thành công", f"Xin chào {user['TenNV']}!")
            root.destroy()
            # Import cục bộ để tránh vòng import
            from main import main_view
            main_view(user)
        else:
            messagebox.showerror("Lỗi đăng nhập", "Sai tên đăng nhập hoặc mật khẩu!")

    tk.Button(root, text="Đăng nhập", font=("Times New Roman", 12, "bold"),
              bg="#1a4ed1", fg="white", width=15, command=xu_ly_dang_nhap).pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    login()
