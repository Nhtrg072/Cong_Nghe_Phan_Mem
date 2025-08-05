import tkinter as tk
from tkinter import messagebox, ttk

# Class quản lý giao diện người dùng
class QuanLyGiaoDien:
    def __init__(self, root, quan_ly_cai_dat):
        self.root = root
        self.quan_ly_cai_dat = quan_ly_cai_dat
        self.man_hinh_hien_tai = None
        self.board_buttons = []
        self.current_player_label = None
        self.score_x_label = None
        self.score_o_label = None
        self.status_label = None
        
        self.thiet_lap_style()
    
    def thiet_lap_style(self):
        """Thiết lập màu sắc và font chữ"""
        if self.quan_ly_cai_dat.lay_cai_dat('theme') == 'dark':
            # Theme tối
            self.mau_sac = {
                'bg': '#2d2d2d',
                'fg': '#ffffff',
                'primary': '#4a90e2',
                'secondary': '#6c757d',
                'success': '#28a745',
                'danger': '#dc3545',
                'warning': '#ffc107',
                'info': '#17a2b8',
                'light': '#3d3d3d',
                'button_bg': '#4a4a4a'
            }
        else:
            # Theme sáng (mặc định)
            self.mau_sac = {
                'bg': '#f0f2f5',
                'fg': '#2c3e50',
                'primary': '#4a90e2',
                'secondary': '#6c757d',
                'success': '#28a745',
                'danger': '#dc3545',
                'warning': '#ffc107',
                'info': '#17a2b8',
                'light': '#ffffff',
                'button_bg': '#ffffff'
            }
        
        # Đặt màu nền cho cửa sổ
        self.root.configure(bg=self.mau_sac['bg'])
        
        # Font chữ
        self.font_chu = {
            'title': ('Arial', 24, 'bold'),
            'heading': ('Arial', 16, 'bold'),
            'button': ('Arial', 12, 'bold'),
            'text': ('Arial', 10),
            'cell': ('Arial', 20, 'bold')
        }
    
    def xoa_man_hinh(self):
        """Xóa màn hình hiện tại"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def dieu_chinh_kich_thuoc_cua_so(self):
        """Tự động chỉnh kích thước cửa sổ theo bàn cờ"""
        kich_thuoc = self.quan_ly_cai_dat.lay_cai_dat('board_size')
        
        # Kích thước cơ bản
        width_co_ban = 600
        height_co_ban = 700
        
        # Tính toán kích thước nút
        kich_thuoc_nut = max(2, 8 - kich_thuoc // 2)
        pixel_moi_nut = kich_thuoc_nut * 12
        
        # Tính kích thước cần thiết
        width_ban_co = kich_thuoc * pixel_moi_nut + 50
        height_ban_co = kich_thuoc * (pixel_moi_nut // 2) + 300
        
        # Kích thước cửa sổ mới
        width_moi = max(width_co_ban, width_ban_co + 100)
        height_moi = max(height_co_ban, height_ban_co + 200)
        
        # Không cho quá lớn
        max_width = int(self.root.winfo_screenwidth() * 0.9)
        max_height = int(self.root.winfo_screenheight() * 0.9)
        
        width_moi = min(width_moi, max_width)
        height_moi = min(height_moi, max_height)
        
        self.root.geometry(f"{width_moi}x{height_moi}")
        
        # Căn giữa cửa sổ
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (width_moi // 2)
        y = (self.root.winfo_screenheight() // 2) - (height_moi // 2)
        self.root.geometry(f"{width_moi}x{height_moi}+{x}+{y}")
    
    def hien_menu(self, callbacks):
        """Hiển thị menu chính"""
        self.xoa_man_hinh()
        self.man_hinh_hien_tai = 'menu'
        
        # Đặt lại kích thước cho menu
        self.root.geometry("600x700")
        
        # Căn giữa cửa sổ
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"600x700+{x}+{y}")
        
        # Tiêu đề game
        tieu_de = tk.Label(
            self.root, 
            text="🎮 GAME CỜ CARO 🎮",
            font=self.font_chu['title'],
            bg=self.mau_sac['bg'],
            fg=self.mau_sac['fg']
        )
        tieu_de.pack(pady=50)
        
        # Khung chứa các nút
        khung_nut = tk.Frame(self.root, bg=self.mau_sac['bg'])
        khung_nut.pack(pady=20)
        
        # Danh sách các nút menu
        cac_nut = [
            ("👥 Chơi với người", callbacks['choi_voi_nguoi']),
            ("🤖 Chơi với máy", callbacks['choi_voi_may']),
            ("⚙️ Cài đặt", callbacks['cai_dat']),
            ("ℹ️ Hướng dẫn", callbacks['huong_dan']),
            ("❌ Thoát", callbacks['thoat'])
        ]
        
        # Tạo từng nút
        for text, command in cac_nut:
            nut = tk.Button(
                khung_nut,
                text=text,
                font=self.font_chu['button'],
                bg=self.mau_sac['primary'],
                fg='white',
                width=20,
                height=2,
                relief='raised',
                bd=2,
                cursor='hand2',
                command=command
            )
            nut.pack(pady=10)
    
    def cap_nhat_hien_thi_nguoi_choi(self, nguoi_choi):
        """Cập nhật hiển thị người chơi hiện tại"""
        if self.current_player_label:
            self.current_player_label.config(text=f"Lượt của: {nguoi_choi}")
            if nguoi_choi == 'X':
                self.current_player_label.config(fg=self.mau_sac['danger'])
            else:
                self.current_player_label.config(fg=self.mau_sac['primary'])
    
    def cap_nhat_hien_thi_diem(self, diem_so, che_do_game):
        """Cập nhật hiển thị điểm số"""
        if self.score_x_label:
            self.score_x_label.config(text=f"X: {diem_so['X']}")
        
        if self.score_o_label:
            ten_nguoi_o = "🤖 Máy" if che_do_game == 'ai' else "O"
            self.score_o_label.config(text=f"{ten_nguoi_o}: {diem_so['O']}")
    
    def vo_hieu_hoa_tat_ca_nut(self):
        """Vô hiệu hóa tất cả nút trên bàn cờ"""
        kich_thuoc = self.quan_ly_cai_dat.lay_cai_dat('board_size')
        for hang in range(kich_thuoc):
            for cot in range(kich_thuoc):
                self.board_buttons[hang][cot].config(state='disabled')
    
    def lam_noi_bat_o_thang(self, cac_o):
        """Làm nổi bật các ô thắng"""
        for hang, cot in cac_o:
            self.board_buttons[hang][cot].config(bg='lightgreen')
