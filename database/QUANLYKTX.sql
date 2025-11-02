CREATE DATABASE QUANLYKTX 
GO
USE QUANLYKTX;
GO

-- ============================================
-- 1️⃣ BẢNG TÀI KHOẢN
-- ============================================
CREATE TABLE taikhoan (
    ten_dang_nhap NVARCHAR(50) PRIMARY KEY,
    mat_khau NVARCHAR(100) NOT NULL,
    vai_tro NVARCHAR(20) DEFAULT 'admin'
);

-- ============================================
-- 2️⃣ BẢNG SINH VIÊN
-- ============================================
CREATE TABLE sinhvien (
    ma_sv NVARCHAR(10) PRIMARY KEY,
    ho_ten NVARCHAR(100),
    ngay_sinh DATE,
    gioi_tinh NVARCHAR(10),
    cmnd_cccd NVARCHAR(20),
    sdt NVARCHAR(15),
    email NVARCHAR(100),
    que_quan NVARCHAR(100),
    khoa NVARCHAR(100),
    lop NVARCHAR(50),
    phong NVARCHAR(10),
    ngay_vao DATE,
    trang_thai NVARCHAR(50),
    ghi_chu NVARCHAR(255)
);

-- ============================================
-- 3️⃣ BẢNG NHÂN VIÊN
-- ============================================
CREATE TABLE nhanvien (
    ma_nv NVARCHAR(10) PRIMARY KEY,
    ho_ten NVARCHAR(100),
    ngay_sinh DATE,
    gioi_tinh NVARCHAR(10),
    cmnd_cccd NVARCHAR(20),
    sdt NVARCHAR(15),
    email NVARCHAR(100),
    que_quan NVARCHAR(100),
    dia_chi NVARCHAR(200),
    chuc_vu NVARCHAR(50),
    ngay_vao_lam DATE,
    ca_truc NVARCHAR(50),
    luong_cb DECIMAL(12,0),
    trang_thai_lv NVARCHAR(50),
    ghi_chu NVARCHAR(255)
);

-- ============================================
-- 4️⃣ BẢNG PHÒNG
-- ============================================
CREATE TABLE phong (
    ma_phong NVARCHAR(10) PRIMARY KEY,
    toa_nha NVARCHAR(10),
    loai_phong NVARCHAR(50),
    so_nguoi_toi_da INT,
    so_nguoi_hien_tai INT DEFAULT 0,
    gia_phong DECIMAL(10,0),
    trang_thai NVARCHAR(50),
    ghi_chu NVARCHAR(255)
);

-- ============================================
-- 5️⃣ BẢNG DỊCH VỤ
-- ============================================
CREATE TABLE dichvu (
    ma_dv NVARCHAR(10) PRIMARY KEY,
    ten_dv NVARCHAR(100),
    don_gia DECIMAL(10,0),
    don_vi NVARCHAR(50)
);

-- ============================================
-- 6️⃣ BẢNG HÓA ĐƠN
-- ============================================
CREATE TABLE hoadon (
    ma_hd NVARCHAR(10) PRIMARY KEY,
    ma_sv NVARCHAR(10),
    ngay_lap DATE,
    tong_tien DECIMAL(12,0),
    nguoi_lap NVARCHAR(100),
    FOREIGN KEY (ma_sv) REFERENCES sinhvien(ma_sv)
);

-- ============================================
-- 7️⃣ BẢNG THANH TOÁN
-- ============================================
CREATE TABLE thanhtoan (
    ma_tt NVARCHAR(10) PRIMARY KEY,
    ma_hd NVARCHAR(10),
    ma_dv NVARCHAR(10),
    so_luong DECIMAL(10,2),
    thanh_tien DECIMAL(12,0),
    FOREIGN KEY (ma_hd) REFERENCES hoadon(ma_hd),
    FOREIGN KEY (ma_dv) REFERENCES dichvu(ma_dv)
);

---------------------------------------------------------
-- ============================================
-- 🔹 BẢNG TÀI KHOẢN
-- ============================================
DELETE FROM taikhoan WHERE ten_dang_nhap = N'admin';
INSERT INTO taikhoan (ten_dang_nhap, mat_khau, vai_tro)
VALUES (N'admin', N'123456', N'admin');


-- ============================================
-- 🔹 BẢNG SINH VIÊN
-- ============================================
INSERT INTO SINHVIEN (ma_sv, ho_ten, ngay_sinh, gioi_tinh, cmnd_cccd, sdt, email, que_quan, khoa, lop, phong, ngay_vao, trang_thai, ghi_chu)
VALUES
('SV001', N'Nguyễn Văn An', '2003-05-12', N'Nam', N'079123456', N'0905111222', N'an.nguyen@agu.edu.vn', N'An Giang', N'Công nghệ thông tin', N'DH22TH1', N'P101', '2022-09-01', N'Đang ở', N''),
('SV002', N'Lê Thị Bình', '2004-08-10', N'Nữ', N'089654321', N'0912111333', N'binh.le@agu.edu.vn', N'Đồng Tháp', N'Kinh tế', N'DH22KT1', N'P102', '2023-01-10', N'Đang ở', N''),
('SV003', N'Phạm Văn Cường', '2002-11-23', N'Nam', N'077234567', N'0988776655', N'cuong.pham@agu.edu.vn', N'Cần Thơ', N'Công nghệ thông tin', N'DH22TH2', N'P201', '2022-09-01', N'Đang ở', N''),
('SV004', N'Trần Thị Dung', '2004-03-30', N'Nữ', N'066543210', N'0977888999', N'dung.tran@agu.edu.vn', N'Kiên Giang', N'Sư phạm Toán', N'DH22SP1', N'P202', '2023-02-15', N'Đang ở', N''),
('SV005', N'Võ Minh Đức', '2003-12-05', N'Nam', N'099111222', N'0933444555', N'duc.vo@agu.edu.vn', N'Hậu Giang', N'Kỹ thuật phần mềm', N'DH21CT3', N'P203', '2022-09-01', N'Đang ở', N''),
('SV006', N'Nguyễn Thị Hoa', '2002-07-14', N'Nữ', N'055444333', N'0944555666', N'hoa.nguyen@agu.edu.vn', N'An Giang', N'Công nghệ thực phẩm', N'DH20TP1', N'P301', '2022-09-01', N'Đang ở', N''),
('SV007', N'Lý Văn Hưng', '2001-06-22', N'Nam', N'033222111', N'0911222333', N'hung.ly@agu.edu.vn', N'Đồng Tháp', N'Nông Nghiệp', N'DH21NN1', N'P302', '2021-09-01', N'Đang ở', N''),
('SV008', N'Trần Ngọc Lan', '2003-09-18', N'Nữ', N'044777888', N'0922111000', N'lan.tran@agu.edu.vn', N'Cần Thơ', N'Ngôn ngữ Anh', N'DH21NA1', N'P303', '2022-09-01', N'Đang ở', N''),
('SV009', N'Phạm Quang Minh', '2004-01-25', N'Nam', N'099888777', N'0977445566', N'minh.pham@agu.edu.vn', N'Kiên Giang', N'Kế toán', N'DH22KT2', N'P304', '2023-02-01', N'Đang ở', N''),
('SV010', N'Đỗ Thị Như', '2003-04-09', N'Nữ', N'088111222', N'0955666777', N'nhu.do@agu.edu.vn', N'An Giang', N'Quản trị du lịch và lữ hành', N'DH21DL1', N'P305', '2022-09-01', N'Đang ở', N'');



-- ============================================
-- 🔹 BẢNG NHÂN VIÊN
-- ============================================
INSERT INTO NHANVIEN (ma_nv, ho_ten, ngay_sinh, gioi_tinh, cmnd_cccd, sdt, email, que_quan, dia_chi, chuc_vu, ngay_vao_lam, ca_truc, luong_cb, trang_thai_lv, ghi_chu)
VALUES
('NV001', N'Trần Văn Hùng', '1985-05-15', N'Nam', N'079123456', N'0905111222', N'tvhung@gmail.com', N'An Giang', N'123 Trần Hưng Đạo, P. Mỹ Bình', N'Quản lý', '2020-01-10', N'Hành chính', N'10000000', N'Đang làm việc', N''),
('NV002', N'Lê Thị Lan', '1990-08-20', N'Nữ', N'088765432', N'0912333444', N'ltlan@gmail.com', N'Đồng Tháp', N'456 Lý Thường Kiệt, P. Mỹ Xuyên', N'Vệ sinh', '2021-03-05', N'Sáng (6-14h)', N'5500000', N'Đang làm việc', N''),
('NV003', N'Phạm Văn Nam', '1995-11-10', N'Nam', N'066543210', N'0987555666', N'pvnam@gmail.com', N'Cần Thơ', N'789 Nguyễn Trãi, P. Mỹ Long', N'Bảo vệ', '2022-07-20', N'Đêm (22-6h)', N'7000000', N'Đang làm việc', N''),
('NV004', N'Nguyễn Thị Hoa', '1988-03-02', N'Nữ', N'099888777', N'0333444555', N'nthoa@gmail.com', N'Kiên Giang', N'101 Tôn Đức Thắng, P. Bình Khánh', N'Vệ sinh', '2021-12-01', N'Chiều (14-22h)', N'5500000', N'Tạm nghỉ', N'Nghỉ thai sản'),
('NV005', N'Lý Văn Toàn', '1992-06-30', N'Nam', N'055444333', N'0777888999', N'lvtoan@gmail.com', N'An Giang', N'222 Hà Hoàng Hổ, P. Mỹ Xuyên', N'Kỹ thuật', '2021-02-15', N'Hành chính', N'8000000', N'Đang làm việc', N'Bảo trì điện nước'),
('NV006', N'Đặng Thị Hằng', '1994-09-12', N'Nữ', N'044555666', N'0911666777', N'hdang@gmail.com', N'Hậu Giang', N'23 Nguyễn Du, P. Mỹ Bình', N'Lễ tân', '2021-08-01', N'Sáng (6-14h)', N'6000000', N'Đang làm việc', N''),
('NV007', N'Trương Minh Phúc', '1987-01-18', N'Nam', N'033666777', N'0933666777', N'mphuc@gmail.com', N'Cần Thơ', N'89 Trần Quang Diệu, P. Mỹ Long', N'Bảo vệ', '2020-05-10', N'Đêm (22-6h)', N'7200000', N'Đang làm việc', N''),
('NV008', N'Võ Ngọc Yến', '1996-11-21', N'Nữ', N'088777999', N'0944888999', N'vyen@gmail.com', N'Đồng Tháp', N'66 Lê Lợi, P. Mỹ Phước', N'Kế toán', '2022-03-15', N'Hành chính', N'9000000', N'Đang làm việc', N''),
('NV009', N'Phan Thanh Sơn', '1989-02-26', N'Nam', N'077333222', N'0922444555', N'tson@gmail.com', N'An Giang', N'120 Nguyễn Văn Cừ, P. Mỹ Bình', N'Bảo trì', '2021-05-01', N'Hành chính', N'8500000', N'Đang làm việc', N''),
('NV010', N'Nguyễn Thị Kim', '1993-10-04', N'Nữ', N'099222333', N'0955777888', N'ntkim@gmail.com', N'Cần Thơ', N'34 Phan Bội Châu, P. Bình Đức', N'Vệ sinh', '2022-01-10', N'Chiều (14-22h)', N'5400000', N'Đang làm việc', N'');

-- ============================================
-- 🔹 BẢNG PHÒNG
-- ============================================
INSERT INTO phong VALUES
(N'P101', N'A', N'Thường', 4, 2, 500000, N'Đang sử dụng', N''),
(N'P102', N'A', N'Máy lạnh', 4, 3, 700000, N'Đang sử dụng', N'Có điều hòa'),
(N'P103', N'B', N'VIP', 2, 1, 1000000, N'Còn trống', N'Phòng rộng rãi');

-- ============================================
-- 🔹 BẢNG DỊCH VỤ
-- ============================================
INSERT INTO dichvu VALUES
(N'DV001', N'Điện', 3500, N'kWh'),
(N'DV002', N'Nước', 15000, N'm3'),
(N'DV003', N'Internet', 100000, N'tháng'),
(N'DV004', N'Gửi xe', 50000, N'tháng');

-- ============================================
-- 🔹 BẢNG HÓA ĐƠN
-- ============================================
INSERT INTO hoadon VALUES
(N'HD001', N'SV001', '2024-09-30', 850000, N'Admin'),
(N'HD002', N'SV002', '2024-09-30', 900000, N'Admin');

-- ============================================
-- 🔹 BẢNG THANH TOÁN
-- ============================================
INSERT INTO thanhtoan VALUES
(N'TT001', N'HD001', N'DV001', 50, 175000),
(N'TT002', N'HD001', N'DV002', 3, 45000),
(N'TT003', N'HD001', N'DV003', 1, 100000),
(N'TT004', N'HD002', N'DV001', 60, 210000),
(N'TT005', N'HD002', N'DV004', 1, 50000);



select *from sinhvien;