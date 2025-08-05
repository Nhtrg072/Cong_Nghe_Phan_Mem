# game_screen.py - Màn hình chơi game
import tkinter as tk
from tkinter import messagebox

class ManHinhGame:
    """Class quản lý màn hình chơi game"""
    
    def __init__(self, cua_so_goc, quan_ly_ui, controller, cai_dat):
        self.cua_so_goc = cua_so_goc
        self.quan_ly_ui = quan_ly_ui
        self.controller = controller
        self.cai_dat = cai_dat
        
        self.cac_nut_ban_co = []
        self.label_nguoi_choi = None
        self.label_diem_x = None
        self.label_diem_o = None
        self.label_trang_thai = None
        
        # Đặt callback cho controller
        self.controller.dat_ui_callback(self.xu_ly_callback)
    
    def hien_thi(self, trang_thai_game):
        """Hiển thị màn hình game"""
        self.xoa_man_hinh()
        
        # Header
        self.tao_header()
        
        # Thông tin game
        self.tao_thong_tin_game(trang_thai_game)
        
        # Bàn cờ
        self.tao_ban_co(trang_thai_game)
        
        # Trạng thái game
        self.tao_trang_thai()
        
        # Nút điều khiển
        self.tao_nut_dieu_khien()
        
        # Phím tắt
        self.thiet_lap_phim_tat()
    
    def xoa_man_hinh(self):
        """Xóa tất cả widget trên màn hình"""
        for widget in self.cua_so_goc.winfo_children():
            widget.destroy()
        self.cac_nut_ban_co.clear()
    
    def tao_header(self):
        """Tạo header với menu và settings"""
        style_frame = self.quan_ly_ui.tao_style_frame()
        header_frame = tk.Frame(self.cua_so_goc, **style_frame)
        header_frame.pack(fill='x', padx=10, pady=5)
        
        # Nút back
        style_nut_phu = self.quan_ly_ui.tao_style_nut('phu')
        nut_back = tk.Button(
            header_frame, 
            text="🏠 Menu", 
            command=self.ve_menu,
            **style_nut_phu
        )
        nut_back.pack(side='left')
        
        # Tiêu đề
        style_label = self.quan_ly_ui.tao_style_label('tieu_de_phu')
        tieu_de = tk.Label(header_frame, text="Game Cờ Caro", **style_label)
        tieu_de.pack(side='left', padx=20)
        
        # Nút settings
        style_nut_thong_tin = self.quan_ly_ui.tao_style_nut('thong_tin')
        nut_settings = tk.Button(
            header_frame, 
            text="⚙️", 
            command=self.mo_settings,
            **style_nut_thong_tin
        )
        nut_settings.pack(side='right')
    
    def tao_thong_tin_game(self, trang_thai_game):
        """Tạo thông tin game (người chơi hiện tại, điểm số)"""
        mau_sac = self.quan_ly_ui.lay_tat_ca_mau()
        
        # Frame thông tin
        info_frame = tk.Frame(
            self.cua_so_goc, 
            bg=mau_sac['sang'], 
            relief='raised', 
            bd=2
        )
        info_frame.pack(fill='x', padx=10, pady=5)
        
        # Người chơi hiện tại
        player_frame = tk.Frame(info_frame, bg=mau_sac['sang'])
        player_frame.pack(pady=10)
        
        style_label_heading = self.quan_ly_ui.tao_style_label('tieu_de_phu')
        style_label_heading['bg'] = mau_sac['sang']
        
        self.label_nguoi_choi = tk.Label(
            player_frame, 
            text=f"Lượt của: {trang_thai_game.nguoi_choi_hien_tai}",
            **style_label_heading
        )
        self.label_nguoi_choi.pack()
        
        # Mode game
        mode_text = "🤖 Chơi với máy" if self.cai_dat.lay('che_do_game') == 'ai' else "👥 Hai người chơi"
        style_label_text = self.quan_ly_ui.tao_style_label('chu_thuong')
        style_label_text['bg'] = mau_sac['sang']
        
        tk.Label(player_frame, text=mode_text, **style_label_text).pack()
        
        # Điểm số
        score_frame = tk.Frame(info_frame, bg=mau_sac['sang'])
        score_frame.pack(pady=5)
        
        style_label_nut = self.quan_ly_ui.tao_style_label('nut')
        style_label_nut['bg'] = mau_sac['sang']
        
        tk.Label(score_frame, text="ĐIỂM SỐ", **style_label_nut).pack()
        
        scores_container = tk.Frame(score_frame, bg=mau_sac['sang'])
        scores_container.pack()
        
        # Điểm X
        style_diem_x = self.quan_ly_ui.tao_style_label('chu_thuong')
        style_diem_x.update({
            'bg': mau_sac['sang'],
            'fg': mau_sac['nguy_hiem']
        })
        
        self.label_diem_x = tk.Label(
            scores_container, 
            text=f"X: {trang_thai_game.diem_so['X']}",
            **style_diem_x
        )
        self.label_diem_x.pack(side='left', padx=20)
        
        # Điểm O
        ten_nguoi_choi_o = "🤖 Máy" if self.cai_dat.lay('che_do_game') == 'ai' else "O"
        style_diem_o = self.quan_ly_ui.tao_style_label('chu_thuong')
        style_diem_o.update({
            'bg': mau_sac['sang'],
            'fg': mau_sac['chinh']
        })
        
        self.label_diem_o = tk.Label(
            scores_container, 
            text=f"{ten_nguoi_choi_o}: {trang_thai_game.diem_so['O']}",
            **style_diem_o
        )
        self.label_diem_o.pack(side='right', padx=20)
    
    def tao_ban_co(self, trang_thai_game):
        """Tạo bàn cờ"""
        style_frame = self.quan_ly_ui.tao_style_frame()
        board_frame = tk.Frame(self.cua_so_goc, **style_frame)
        board_frame.pack(pady=20)
        
        kich_thuoc = trang_thai_game.kich_thuoc
        self.cac_nut_ban_co = []
        
        # Tính kích thước nút
        kich_thuoc_nut, kich_thuoc_font = self.quan_ly_ui.tinh_kich_thuoc_nut(kich_thuoc)
        
        mau_sac = self.quan_ly_ui.lay_tat_ca_mau()
        
        for i in range(kich_thuoc):
            hang = []
            for j in range(kich_thuoc):
                nut = tk.Button(
                    board_frame,
                    text='',
                    font=('Arial', kich_thuoc_font, 'bold'),
                    width=kich_thuoc_nut,
                    height=kich_thuoc_nut//2,
                    command=lambda h=i, c=j: self.controller.xu_ly_nuoc_di(h, c),
                    bg=mau_sac['nen_nut'],
                    relief='raised',
                    bd=2,
                    cursor='hand2'
                )
                nut.grid(row=i, column=j, padx=1, pady=1)
                hang.append(nut)
            self.cac_nut_ban_co.append(hang)
    
    def tao_trang_thai(self):
        """Tạo label hiển thị trạng thái game"""
        style_label = self.quan_ly_ui.tao_style_label('tieu_de_phu')
        style_label['fg'] = self.quan_ly_ui.lay_mau('thanh_cong')
        
        self.label_trang_thai = tk.Label(self.cua_so_goc, text="", **style_label)
        self.label_trang_thai.pack(pady=10)
    
    def tao_nut_dieu_khien(self):
        """Tạo các nút điều khiển"""
        style_frame = self.quan_ly_ui.tao_style_frame()
        control_frame = tk.Frame(self.cua_so_goc, **style_frame)
        control_frame.pack(pady=10)
        
        # Nút reset
        style_canh_bao = self.quan_ly_ui.tao_style_nut('canh_bao')
        nut_reset = tk.Button(
            control_frame, 
            text="🔄 Chơi lại", 
            command=self.controller.reset_game,
            **style_canh_bao
        )
        nut_reset.pack(side='left', padx=5)
        
        # Nút game mới
        style_thanh_cong = self.quan_ly_ui.tao_style_nut('thanh_cong')
        nut_moi = tk.Button(
            control_frame, 
            text="🆕 Game mới", 
            command=self.controller.game_moi,
            **style_thanh_cong
        )
        nut_moi.pack(side='left', padx=5)
        
        # Nút gợi ý (chỉ với AI)
        if self.cai_dat.lay('che_do_game') == 'ai':
            style_thong_tin = self.quan_ly_ui.tao_style_nut('thong_tin')
            nut_goi_y = tk.Button(
                control_frame, 
                text="💡 Gợi ý", 
                command=self.controller.lay_goi_y,
                **style_thong_tin
            )
            nut_goi_y.pack(side='left', padx=5)
        
        # Nút hoàn tác
        style_phu = self.quan_ly_ui.tao_style_nut('phu')
        nut_undo = tk.Button(
            control_frame, 
            text="↶ Hoàn tác", 
            command=self.controller.hoan_tac,
            **style_phu
        )
        nut_undo.pack(side='left', padx=5)
    
    def thiet_lap_phim_tat(self):
        """Thiết lập phím tắt"""
        self.cua_so_goc.bind('<Key>', self.xu_ly_phim_tat)
        self.cua_so_goc.focus_set()
    
    def xu_ly_phim_tat(self, event):
        """Xử lý phím tắt"""
        phim = event.char.lower()
        
        if phim == 'r':
            self.controller.reset_game()
        elif phim == 'n':
            self.controller.game_moi()
        elif phim == 'h':
            self.controller.lay_goi_y()
        elif phim == 'u':
            self.controller.hoan_tac()
        elif phim == 'q':
            self.thoat_game()
        
        # Phím số cho bàn 3x3
        if (hasattr(self.controller.trang_thai_game, 'kich_thuoc') and
            self.controller.trang_thai_game.kich_thuoc == 3 and 
            event.char.isdigit() and 1 <= int(event.char) <= 9):
            chi_so = int(event.char) - 1
            hang, cot = chi_so // 3, chi_so % 3
            self.controller.xu_ly_nuoc_di(hang, cot)
    
    def xu_ly_callback(self, hanh_dong, *args):
        """Xử lý callback từ controller"""
        if hanh_dong == 'cap_nhat_o':
            self.cap_nhat_o_co(*args)
        elif hanh_dong == 'xoa_o':
            self.xoa_o_co(*args)
        elif hanh_dong == 'cap_nhat_nguoi_choi':
            self.cap_nhat_nguoi_choi_hien_tai(*args)
        elif hanh_dong == 'highlight_thang':
            self.highlight_cac_o_thang(*args)
        elif hanh_dong == 'cap_nhat_trang_thai':
            self.cap_nhat_trang_thai(*args)
        elif hanh_dong == 'vo_hieu_hoa_ban_co':
            self.vo_hieu_hoa_tat_ca_nut()
        elif hanh_dong == 'reset_ui':
            self.reset_giao_dien()
        elif hanh_dong == 'hien_thi_goi_y':
            self.hien_thi_goi_y(*args)
        elif hanh_dong == 'delay_ai':
            self.cua_so_goc.after(args[0], self.controller.xu_ly_luot_ai)
    
    def cap_nhat_o_co(self, hang, cot, nguoi_choi):
        """Cập nhật ô cờ"""
        if hang < len(self.cac_nut_ban_co) and cot < len(self.cac_nut_ban_co[hang]):
            nut = self.cac_nut_ban_co[hang][cot]
            nut.config(text=nguoi_choi, state='disabled')
            
            mau_sac = self.quan_ly_ui.lay_tat_ca_mau()
            if nguoi_choi == 'X':
                nut.config(fg=mau_sac['nguy_hiem'], bg='#ffe6e6')
            else:
                nut.config(fg=mau_sac['chinh'], bg='#e6f3ff')
    
    def xoa_o_co(self, hang, cot):
        """Xóa ô cờ"""
        if hang < len(self.cac_nut_ban_co) and cot < len(self.cac_nut_ban_co[hang]):
            nut = self.cac_nut_ban_co[hang][cot]
            mau_sac = self.quan_ly_ui.lay_tat_ca_mau()
            nut.config(text='', state='normal', bg=mau_sac['nen_nut'], fg='black')
    
    def cap_nhat_nguoi_choi_hien_tai(self, nguoi_choi):
        """Cập nhật hiển thị người chơi hiện tại"""
        if self.label_nguoi_choi:
            self.label_nguoi_choi.config(text=f"Lượt của: {nguoi_choi}")
            mau_sac = self.quan_ly_ui.lay_tat_ca_mau()
            if nguoi_choi == 'X':
                self.label_nguoi_choi.config(fg=mau_sac['nguy_hiem'])
            else:
                self.label_nguoi_choi.config(fg=mau_sac['chinh'])
    
    def highlight_cac_o_thang(self, cac_o):
        """Highlight các ô thắng"""
        for hang, cot in cac_o:
            if hang < len(self.cac_nut_ban_co) and cot < len(self.cac_nut_ban_co[hang]):
                self.cac_nut_ban_co[hang][cot].config(bg='lightgreen')
    
    def cap_nhat_trang_thai(self, thong_bao):
        """Cập nhật trạng thái game"""
        if self.label_trang_thai:
            self.label_trang_thai.config(text=thong_bao)
    
    def vo_hieu_hoa_tat_ca_nut(self):
        """Vô hiệu hóa tất cả nút bàn cờ"""
        for hang in self.cac_nut_ban_co:
            for nut in hang:
                nut.config(state='disabled')
    
    def reset_giao_dien(self):
        """Reset giao diện về trạng thái ban đầu"""
        # Reset bàn cờ
        mau_sac = self.quan_ly_ui.lay_tat_ca_mau()
        for hang in self.cac_nut_ban_co:
            for nut in hang:
                nut.config(text='', state='normal', bg=mau_sac['nen_nut'], fg='black')
        
        # Reset trạng thái
        if self.label_trang_thai:
            self.label_trang_thai.config(text="")
        
        # Reset người chơi
        if self.label_nguoi_choi:
            self.cap_nhat_nguoi_choi_hien_tai('X')
    
    def hien_thi_goi_y(self, vi_tri):
        """Hiển thị gợi ý"""
        hang, cot = vi_tri
        if hang < len(self.cac_nut_ban_co) and cot < len(self.cac_nut_ban_co[hang]):
            nut = self.cac_nut_ban_co[hang][cot]
            mau_goc = nut.cget('bg')
            nut.config(bg='yellow')
            self.cua_so_goc.after(2000, lambda: nut.config(bg=mau_goc))
    
    def ve_menu(self):
        """Callback để về menu"""
        # Sẽ được implement trong main
        pass
    
    def mo_settings(self):
        """Callback để mở settings"""
        # Sẽ được implement trong main
        pass
    
    def thoat_game(self):
        """Callback để thoát game"""
        # Sẽ được implement trong main
        pass
