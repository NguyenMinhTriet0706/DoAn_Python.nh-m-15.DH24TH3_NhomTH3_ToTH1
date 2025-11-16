CREATE DATABASE QUANLYKTX;
GO
USE QUANLYKTX;
GO

-- ===========================================
-- 1️ BẢNG TÀI KHOẢN
-- ===========================================
CREATE TABLE taikhoan (
    ten_dang_nhap NVARCHAR(50) PRIMARY KEY,
    mat_khau NVARCHAR(100) NOT NULL,
    vai_tro NVARCHAR(20) DEFAULT 'admin'
);
GO

-- DỮ LIỆU MẪU TÀI KHOẢN
INSERT INTO taikhoan VALUES
('admin', N'123', N'admin')

GO

-- ===========================================
-- 2️ BẢNG SINH VIÊN
-- ===========================================
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
GO

-- DỮ LIỆU MẪU SINH VIÊN
INSERT INTO sinhvien VALUES
('SV01', N'Nguyễn Văn An', '2003-05-12', N'Nam', '079123456', '0905111222', 'an.nguyen@agu.edu.vn', N'An Giang', N'Công nghệ thông tin', N'DH22TH1', 'P101', '2022-09-01', N'Đang ở', N''),
('SV02', N'Lê Thị Bình', '2004-08-10', N'Nữ', '089654321', '0912111333', 'binh.le@agu.edu.vn', N'Đồng Tháp', N'Kinh tế', N'DH22KT1', 'P102', '2023-01-10', N'Đang ở', N''),
('SV03', N'Phạm Văn Cường', '2002-11-23', N'Nam', '077234567', '0988776655', 'cuong.pham@agu.edu.vn', N'Cần Thơ', N'Công nghệ thông tin', N'DH22TH2', 'P103', '2022-09-01', N'Đang ở', N''),
('SV04', N'Trần Thị Dung', '2004-03-30', N'Nữ', '066543210', '0977888999', 'dung.tran@agu.edu.vn', N'Kiên Giang', N'Sư phạm Toán', N'DH22SP1', 'P104', '2023-02-15', N'Đang ở', N''),
('SV05', N'Võ Minh Đức', '2003-12-05', N'Nam', '099111222', '0933444555', 'duc.vo@agu.edu.vn', N'Hậu Giang', N'Kỹ thuật phần mềm', N'DH21CT3', 'P105', '2022-09-01', N'Đang ở', N''),
('SV06', N'Nguyễn Thị Hoa', '2002-07-14', N'Nữ', '055444333', '0944555666', 'hoa.nguyen@agu.edu.vn', N'An Giang', N'Công nghệ thực phẩm', N'DH20TP1', 'P201', '2022-09-01', N'Đang ở', N''),
('SV07', N'Lý Văn Hưng', '2001-06-22', N'Nam', '033222111', '0911222333', 'hung.ly@agu.edu.vn', N'Đồng Tháp', N'Nông Nghiệp', N'DH21NN1', 'P202', '2021-09-01', N'Đang ở', N''),
('SV08', N'Trần Ngọc Lan', '2003-09-18', N'Nữ', '044777888', '0922111000', 'lan.tran@agu.edu.vn', N'Cần Thơ', N'Ngôn ngữ Anh', N'DH21NA1', 'P203', '2022-09-01', N'Đang ở', N'');
GO

-- ===========================================
-- 3️ BẢNG NHÂN VIÊN
-- ===========================================
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
GO

-- DỮ LIỆU MẪU NHÂN VIÊN
INSERT INTO nhanvien VALUES
('NV01', N'Trần Văn Hùng', '1985-05-15', N'Nam', '079123456', '0905111222', 'tvhung@gmail.com', N'An Giang', N'123 Trần Hưng Đạo, P. Mỹ Bình', N'Quản lý', '2020-01-10', N'Hành chính', 10000000, N'Đang làm việc', N''),
('NV02', N'Lê Thị Lan', '1990-08-20', N'Nữ', '088765432', '0912333444', 'ltlan@gmail.com', N'Đồng Tháp', N'456 Lý Thường Kiệt, P. Mỹ Xuyên', N'Vệ sinh', '2021-03-05', N'Sáng (6-14h)', 5500000, N'Đang làm việc', N''),
('NV03', N'Phạm Văn Nam', '1995-11-10', N'Nam', '066543210', '0987555666', 'pvnam@gmail.com', N'Cần Thơ', N'789 Nguyễn Trãi, P. Mỹ Long', N'Bảo vệ', '2022-07-20', N'Đêm (22-6h)', 7000000, N'Đang làm việc', N''),
('NV04', N'Nguyễn Thị Hoa', '1988-03-02', N'Nữ', '099888777', '0333444555', 'nthoa@gmail.com', N'Kiên Giang', N'101 Tôn Đức Thắng, P. Bình Khánh', N'Vệ sinh', '2021-12-01', N'Chiều (14-22h)', 5500000, N'Tạm nghỉ', N'Nghỉ thai sản'),
('NV05', N'Lý Văn Toàn', '1992-06-30', N'Nam', '055444333', '0777888999', 'lvtoan@gmail.com', N'An Giang', N'222 Hà Hoàng Hổ, P. Mỹ Xuyên', N'Kỹ thuật', '2021-02-15', N'Hành chính', 8000000, N'Đang làm việc', N'Bảo trì điện nước'),
('NV06', N'Đặng Thị Hằng', '1994-09-12', N'Nữ', '044555666', '0911666777', 'hdang@gmail.com', N'Hậu Giang', N'23 Nguyễn Du, P. Mỹ Bình', N'Lễ tân', '2021-08-01', N'Sáng (6-14h)', 6000000, N'Đang làm việc', N''),
('NV07', N'Trương Minh Phúc', '1987-01-18', N'Nam', '033666777', '0933666777', 'mphuc@gmail.com', N'Cần Thơ', N'89 Trần Quang Diệu, P. Mỹ Long', N'Bảo vệ', '2020-05-10', N'Đêm (22-6h)', 7200000, N'Đang làm việc', N''),
('NV08', N'Võ Ngọc Yến', '1996-11-21', N'Nữ', '088777999', '0944888999', 'vyen@gmail.com', N'Đồng Tháp', N'66 Lê Lợi, P. Mỹ Phước', N'Kế toán', '2022-03-15', N'Hành chính', 9000000, N'Đang làm việc', N'');
GO

-- ===========================================
-- 4️ BẢNG PHÒNG 
-- ===========================================
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
GO

INSERT INTO phong VALUES
('P101', 'A', N'Thường', 4, 2, 1200000, N'Còn trống', N'Phòng thoáng mát'),
('P102', 'A', N'Máy lạnh', 4, 4, 1500000, N'Đầy', N'Phòng có máy lạnh'),
('P103', 'A', N'Thường', 4, 3, 1200000, N'Đang sử dụng', N'Phòng có ban công'),
('P104', 'B', N'Máy lạnh', 4, 4, 1600000, N'Đầy', N'Phòng có tủ lạnh'),
('P105', 'B', N'Thường', 4, 1, 1100000, N'Còn trống', N'Gần khu vệ sinh'),
('P201', 'C', N'Thường', 6, 6, 1000000, N'Đầy', N'Phòng lớn'),
('P202', 'C', N'Máy lạnh', 6, 5, 1700000, N'Đang sử dụng', N'Phòng rộng rãi'),
('P203', 'C', N'Thường', 4, 2, 1150000, N'Còn trống', N'Phòng sạch đẹp');
GO

-- ===========================================
-- 5️ BẢNG DỊCH VỤ 
-- ===========================================
CREATE TABLE dichvu (
    ma_dv NVARCHAR(10) PRIMARY KEY,
    ten_dv NVARCHAR(100),
    loai_dv NVARCHAR(50),
    don_vi NVARCHAR(20),
    don_gia DECIMAL(10,0),
    ngay_ap_dung DATE DEFAULT GETDATE(),
    trang_thai NVARCHAR(50) DEFAULT N'Hoạt động',
    mo_ta NVARCHAR(255)
);
GO

INSERT INTO dichvu VALUES
('DV01', N'Tiền điện', N'Điện', N'kWh', 3500, GETDATE(), N'Hoạt động', N'Tính theo công tơ'),
('DV02', N'Tiền nước', N'Nước', N'm³', 15000, GETDATE(), N'Hoạt động', N'Tính theo đồng hồ nước'),
('DV03', N'Internet', N'Mạng', N'Tháng', 100000, GETDATE(), N'Hoạt động', N'Cáp quang tốc độ cao'),
('DV04', N'Rác thải', N'Phí môi trường', N'Tháng', 20000, GETDATE(), N'Hoạt động', N'Thu gom rác hàng ngày'),
('DV05', N'Gửi xe', N'Phí dịch vụ', N'Tháng', 50000, GETDATE(), N'Hoạt động', N'Xe máy'),
('DV06', N'Máy giặt', N'Dịch vụ thêm', N'Lần', 10000, GETDATE(), N'Hoạt động', N'Tự phục vụ'),
('DV07', N'Vệ sinh phòng', N'Dịch vụ thêm', N'Lần', 20000, GETDATE(), N'Hoạt động', N'Dọn dẹp theo yêu cầu'),
('DV08', N'Dịch vụ thêm khác', N'Dịch vụ thêm', N'Lần', 15000, GETDATE(), N'Hoạt động', N'Thuê thêm thiết bị');
GO

-- ===========================================
-- 6️ BẢNG HÓA ĐƠN 
-- ===========================================
CREATE TABLE hoadon (
    ma_hd NVARCHAR(10) PRIMARY KEY,
    ma_sv NVARCHAR(10),
    ma_phong NVARCHAR(10),
    ngay_lap DATE DEFAULT GETDATE(),
    thang INT,
    nam INT,
    tong_tien DECIMAL(12,0),
    trang_thai NVARCHAR(50) DEFAULT N'Chưa thanh toán',
    phuong_thuc_tt NVARCHAR(50) DEFAULT N'Tiền mặt',
    ngay_thanh_toan DATE NULL,
    ghi_chu NVARCHAR(255),
    FOREIGN KEY (ma_phong) REFERENCES phong(ma_phong)
);
GO

INSERT INTO hoadon VALUES
('HD01', 'SV01', 'P101', GETDATE(), 10, 2025, 2000000, N'Chưa thanh toán', N'Tiền mặt', NULL, N''),
('HD02', 'SV02', 'P102', GETDATE(), 10, 2025, 2300000, N'Đã thanh toán', N'Chuyển khoản', GETDATE(), N'Đã thu đủ'),
('HD03', 'SV03', 'P103', GETDATE(), 9, 2025, 1800000, N'Chưa thanh toán', N'Tiền mặt', NULL, N''),
('HD04', 'SV04', 'P104', GETDATE(), 10, 2025, 2500000, N'Đã thanh toán', N'Tiền mặt', GETDATE(), N'Đã nộp'),
('HD05', 'SV05', 'P105', GETDATE(), 8, 2025, 1600000, N'Chưa thanh toán', N'Tiền mặt', NULL, N'Nợ 1 tháng'),
('HD06', 'SV06', 'P201', GETDATE(), 10, 2025, 3000000, N'Đã thanh toán', N'Chuyển khoản', GETDATE(), N'Đủ tiền'),
('HD07', 'SV07', 'P202', GETDATE(), 10, 2025, 2100000, N'Đang xử lý', N'Chuyển khoản', NULL, N'Đang xác minh'),
('HD08', 'SV08', 'P203', GETDATE(), 10, 2025, 1950000, N'Chưa thanh toán', N'Tiền mặt', NULL, N'');

GO

-- ===========================================
-- 7️ BẢNG THANH TOÁN 
-- ===========================================
CREATE TABLE thanhtoan (
    ma_tt NVARCHAR(10) PRIMARY KEY,
    ma_hd NVARCHAR(10),
    ma_dv NVARCHAR(10),
    so_luong DECIMAL(10,2),
    don_gia DECIMAL(10,0),
    thanh_tien AS (so_luong * don_gia) PERSISTED,
    thang INT,
    nam INT,
    ngay_tt DATE DEFAULT GETDATE(),
    trang_thai NVARCHAR(50) DEFAULT N'Chưa xác nhận',
    nguoi_thuc_hien NVARCHAR(100),
    ghi_chu NVARCHAR(255),

    FOREIGN KEY (ma_hd) REFERENCES hoadon(ma_hd),
    FOREIGN KEY (ma_dv) REFERENCES dichvu(ma_dv)
);
GO

INSERT INTO thanhtoan (
    ma_tt, ma_hd, ma_dv, so_luong, don_gia, thang, nam, ngay_tt, trang_thai, nguoi_thuc_hien, ghi_chu
) VALUES
('TT01', 'HD01', 'DV01', 120, 3500, 10, 2025, GETDATE(), N'Đã xác nhận', N'Nguyễn Văn A', N'Tiền điện tháng 10'),
('TT02', 'HD01', 'DV02', 10, 15000, 10, 2025, GETDATE(), N'Đã xác nhận', N'Nguyễn Văn A', N'Tiền nước tháng 10'),
('TT03', 'HD02', 'DV03', 1, 100000, 10, 2025, GETDATE(), N'Đã xác nhận', N'Lê Thị B', N'Internet tháng 10'),
('TT04', 'HD03', 'DV05', 1, 50000, 9, 2025, GETDATE(), N'Đã xác nhận', N'Phạm Minh C', N'Phí gửi xe tháng 9'),
('TT05', 'HD04', 'DV04', 1, 20000, 10, 2025, GETDATE(), N'Đang xử lý', N'Trần Thị D', N'Rác thải tháng 10'),
('TT06', 'HD05', 'DV01', 100, 3500, 8, 2025, GETDATE(), N'Chưa xác nhận', N'Võ Minh Đ', N'Tiền điện tháng 8'),
('TT07', 'HD06', 'DV03', 1, 100000, 10, 2025, GETDATE(), N'Đã xác nhận', N'Nguyễn Thị H', N'Internet tháng 10'),
('TT08', 'HD07', 'DV02', 15, 15000, 10, 2025, GETDATE(), N'Đang xử lý', N'Lý Văn H', N'Tiền nước tháng 10');


select *from sinhvien


UPDATE taikhoan
SET mat_khau = N'123456'
WHERE ten_dang_nhap = 'admin';

DELETE FROM hoadon
WHERE ma_hd = 'HD09';