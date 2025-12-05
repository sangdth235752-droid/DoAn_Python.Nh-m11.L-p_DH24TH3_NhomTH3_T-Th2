CREATE DATABASE IF NOT EXISTS qli_chxm CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE qli_chxm;
CREATE TABLE XE (
    MaSP VARCHAR(50) NOT NULL PRIMARY KEY,
    TenSP VARCHAR(200) NOT NULL,
    LoaiXe VARCHAR(50),      -- Thêm LoaiXe vào đây
    Hangsx VARCHAR(200),     -- Thêm Hangsx vào đây
    Gia DECIMAL(18,2) NOT NULL,
    SoLuong INT NOT NULL     -- Số lượng tồn kho
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

---

-- Bảng KHACHHANG
CREATE TABLE KHACHHANG (
    MaKhach VARCHAR(50) NOT NULL PRIMARY KEY,
    TenKhach VARCHAR(200) NOT NULL,
    DiaChi VARCHAR(200),
    DienThoai VARCHAR(50)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

---

-- Bảng NHANVIEN
CREATE TABLE NHANVIEN (
    MaNV VARCHAR(50) NOT NULL PRIMARY KEY,
    TenNV VARCHAR(200) NOT NULL,
    GioiTinh VARCHAR(50),
    DiaChi VARCHAR(200),
    DienThoai VARCHAR(50),
    NgaySinh DATETIME,
    TenDangNhap VARCHAR(50) UNIQUE NOT NULL,
    MatKhau VARCHAR(200) NOT NULL,
    VaiTro ENUM('Quan Ly', 'Nhân viên') NOT NULL DEFAULT 'Nhân viên'
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

---

-- Bảng HOADON: Không thay đổi
CREATE TABLE HD (
    MaHD VARCHAR(50) NOT NULL PRIMARY KEY,
    NgayLap DATE NOT NULL,
    MaKH VARCHAR(50) NOT NULL,
	MaSP VARCHAR(50) NOT NULL, -- Mã Xe
    SL INT NOT NULL,
    DonGia DECIMAL(18,2) NOT NULL,
    ThanhTien DECIMAL(18,2) NOT NULL,
    GhiChu TEXT,
    FOREIGN KEY (MaKH) REFERENCES KHACHHANG(MaKhach),
	FOREIGN KEY (MaSP) REFERENCES XE(MaSP)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

#Chen thong tin mau
INSERT INTO XE VALUES
('XE01','Honda Air Blade 160','Xe Tay Ga','Honda',56000000,15),
('XE02','Honda Vision','Xe Tay Ga','Honda',32000000,20),
('XE03','Yamaha Exciter 155','Xe Côn Tay','Yamaha',50000000,10),
('XE04','Yamaha Grande','Xe Tay Ga','Yamaha',45000000,12),
('XE05','Honda Wave Alpha','Xe Số','Honda',18500000,25);

INSERT INTO KHACHHANG VALUES
('KH001', 'Lê Văn Chính', '30 Phan Chu Trinh, HCM', '0903112233'),
('KH002', 'Nguyễn Thị Hiền', '10 Trần Hưng Đạo, Hà Nội', '0904456789'),
('KH003', 'Trần Minh Khôi', '55 Nguyễn Huệ, Đà Nẵng', '0905567890');

INSERT INTO NHANVIEN VALUES
('NV01', 'Trần An', 'Nam', '45 Hoàng Diệu, Đà Nẵng', '0905345678', '1995-03-15','nv01_xe','123456','Nhân viên'),
('NV02', 'Lê Bích Thảo', 'Nữ', '78 Trưng Nữ Vương, Huế', '0906789123', '1990-07-20','admin_xe','1234567','Quan Ly');

INSERT INTO HD (MaHD, NgayLap, MaKH, MaSP, SL, DonGia, ThanhTien, GhiChu)
VALUES 
('HD01', '2025-11-30', 'KH002', 'XE01', 2, 15000000, 30000000, 'Thanh toán tiền mặt'),
('HD02', '2025-12-30', 'KH004', 'XE02', 1, 22000000, 22000000, 'Chuyển khoản'),
('HD03', '2025-11-30', 'KH003', 'XE03', 3, 12000000, 36000000, 'Chuyển khoản');
