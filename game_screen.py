# Class quản lý màn hình game
import tkinter as tk
from tkinter import messagebox

class ManHinhGame:
    def __init__(self, root, quan_ly_ui, callbacks):
        self.root = root
        self.quan_ly_ui = quan_ly_ui
        self.callbacks = callbacks
    
    def hien_thi(self, trang_thai_game, quan_ly_cai_dat):
        """Hiển thị màn hình game"""
        self.quan_ly_ui.xoa_man_hinh()
        self.quan_ly_ui.man_hinh_hien_tai = 'game'
        
        # Đặt kích thước cố định
        self.quan_ly_ui.dat_kich_thuoc_co_dinh()
        
        # Tạo header
        self.tao_header()
        
        # Tạo thông tin game
        self.tao_khung_thong_tin(trang_thai_game, quan_ly_cai_dat)
        
        # Tạo bàn cờ
        self.tao_ban_co(quan_ly_cai_dat)
        
        # Trạng thái game
        self.quan_ly_ui.status_label = tk.Label(self.root, text="", 
                                              font=self.quan_ly_ui.font_chu['heading'], 
                                              bg=self.quan_ly_ui.mau_sac['bg'], 
                                              fg=self.quan_ly_ui.mau_sac['success'])
        self.quan_ly_ui.status_label.pack(pady=5)
        
        # Các nút điều khiển
        self.tao_nut_dieu_khien(quan_ly_cai_dat)
        
        # Gán phím tắt
        self.root.bind('<Key>', self.callbacks['xu_ly_phim'])
        self.root.focus_set()
    
    def tao_header(self):
        """Tạo phần header"""
        header_frame = tk.Frame(self.root, bg=self.quan_ly_ui.mau_sac['bg'])
        header_frame.pack(fill='x', padx=10, pady=5)
        
        back_btn = tk.Button(header_frame, text="🏠 Menu", 
                           font=self.quan_ly_ui.font_chu['button'], 
                           bg=self.quan_ly_ui.mau_sac['secondary'], fg='white',
                           width=12, height=2,
                           command=self.callbacks['ve_menu'])
        back_btn.pack(side='left')
        
        title = tk.Label(header_frame, text="Game Cờ Caro", 
                        font=self.quan_ly_ui.font_chu['heading'], 
                        bg=self.quan_ly_ui.mau_sac['bg'], 
                        fg=self.quan_ly_ui.mau_sac['fg'])
        title.pack(side='left', padx=20)
        
        settings_btn = tk.Button(header_frame, text="⚙️", 
                               font=self.quan_ly_ui.font_chu['button'], 
                               bg=self.quan_ly_ui.mau_sac['info'], fg='white', 
                               command=self.callbacks['cai_dat'])
        settings_btn.pack(side='right')
    
    def tao_khung_thong_tin(self, trang_thai_game, quan_ly_cai_dat):
        """Tạo khung thông tin game"""
        info_frame = tk.Frame(self.root, bg=self.quan_ly_ui.mau_sac['light'], relief='raised', bd=2)
        info_frame.pack(fill='x', padx=10, pady=5)
        
        # Người chơi hiện tại
        player_frame = tk.Frame(info_frame, bg=self.quan_ly_ui.mau_sac['light'])
        player_frame.pack(pady=10)
        
        self.quan_ly_ui.current_player_label = tk.Label(player_frame, 
                                                       text=f"Lượt của: {trang_thai_game.nguoi_choi_hien_tai}", 
                                                       font=self.quan_ly_ui.font_chu['heading'], 
                                                       bg=self.quan_ly_ui.mau_sac['light'])
        self.quan_ly_ui.current_player_label.pack()
        
        mode_text = "🤖 Chơi với máy" if quan_ly_cai_dat.lay_cai_dat('game_mode') == 'ai' else "👥 Hai người chơi"
        tk.Label(player_frame, text=mode_text, font=self.quan_ly_ui.font_chu['text'], 
                bg=self.quan_ly_ui.mau_sac['light']).pack()
        
        # Điểm số
        self.tao_khung_diem_so(info_frame, trang_thai_game, quan_ly_cai_dat)
    
    def tao_khung_diem_so(self, parent, trang_thai_game, quan_ly_cai_dat):
        """Tạo khung điểm số"""
        score_frame = tk.Frame(parent, bg=self.quan_ly_ui.mau_sac['light'])
        score_frame.pack(pady=5)
        
        tk.Label(score_frame, text="ĐIỂM SỐ", font=self.quan_ly_ui.font_chu['button'], 
                bg=self.quan_ly_ui.mau_sac['light']).pack()
        
        scores_container = tk.Frame(score_frame, bg=self.quan_ly_ui.mau_sac['light'])
        scores_container.pack()
        
        self.quan_ly_ui.score_x_label = tk.Label(scores_container, 
                                                text=f"X: {trang_thai_game.diem_so['X']}", 
                                                font=self.quan_ly_ui.font_chu['text'], 
                                                bg=self.quan_ly_ui.mau_sac['light'], 
                                                fg=self.quan_ly_ui.mau_sac['danger'])
        self.quan_ly_ui.score_x_label.pack(side='left', padx=20)
        
        player_o_name = "🤖 Máy" if quan_ly_cai_dat.lay_cai_dat('game_mode') == 'ai' else "O"
        self.quan_ly_ui.score_o_label = tk.Label(scores_container, 
                                               text=f"{player_o_name}: {trang_thai_game.diem_so['O']}", 
                                               font=self.quan_ly_ui.font_chu['text'], 
                                               bg=self.quan_ly_ui.mau_sac['light'], 
                                               fg=self.quan_ly_ui.mau_sac['primary'])
        self.quan_ly_ui.score_o_label.pack(side='right', padx=20)
    
    def tao_ban_co(self, quan_ly_cai_dat):
        """Tạo bàn cờ với kích thước phù hợp cửa sổ cố định"""
        board_container = tk.Frame(self.root, bg=self.quan_ly_ui.mau_sac['bg'])
        board_container.pack(pady=10, fill='both', expand=True)
        
        khung_ban_co = tk.Frame(board_container, bg=self.quan_ly_ui.mau_sac['bg'])
        khung_ban_co.pack(expand=True)
        
        kich_thuoc = quan_ly_cai_dat.lay_cai_dat('board_size')
        self.quan_ly_ui.board_buttons = []
        
        # Tính kích thước nút cho cửa sổ cố định 800x800 - to hơn nữa
        if kich_thuoc <= 5:
            kich_thuoc_nut = 5
            co_chu = 18
        elif kich_thuoc <= 7:
            kich_thuoc_nut = 4
            co_chu = 16
        else:  # 8, 9, 10
            kich_thuoc_nut = 3
            co_chu = 14
        
        # Tạo các nút cho bàn cờ
        for i in range(kich_thuoc):
            hang = []
            for j in range(kich_thuoc):
                nut = tk.Button(
                    khung_ban_co,
                    text='',
                    font=('Arial', co_chu, 'bold'),
                    width=kich_thuoc_nut,
                    height=kich_thuoc_nut//2,
                    command=lambda r=i, c=j: self.callbacks['nuoc_di'](r, c),
                    bg=self.quan_ly_ui.mau_sac['button_bg'],
                    relief='raised',
                    bd=2,
                    cursor='hand2'
                )
                nut.grid(row=i, column=j, padx=1, pady=1)
                hang.append(nut)
            self.quan_ly_ui.board_buttons.append(hang)
    
    def tao_nut_dieu_khien(self, quan_ly_cai_dat):
        """Tạo các nút điều khiển với kích thước cố định"""
        control_frame = tk.Frame(self.root, bg=self.quan_ly_ui.mau_sac['bg'])
        control_frame.pack(side='bottom', pady=10, fill='x')
        
        buttons_container = tk.Frame(control_frame, bg=self.quan_ly_ui.mau_sac['bg'])
        buttons_container.pack()
        
        # Kích thước cố định cho các nút - to hơn
        button_width = 14
        button_height = 2
        font_size = ('Arial', 11, 'bold')
        
        # Reset button
        reset_btn = tk.Button(buttons_container, text="🔄 Chơi lại", 
                            font=font_size, 
                            bg=self.quan_ly_ui.mau_sac['warning'], fg='white',
                            width=button_width, height=button_height,
                            command=self.callbacks['reset'])
        reset_btn.pack(side='left', padx=5)
        
        # New game button
        new_btn = tk.Button(buttons_container, text="🆕 Game mới", 
                          font=font_size, 
                          bg=self.quan_ly_ui.mau_sac['success'], fg='white',
                          width=button_width, height=button_height,
                          command=self.callbacks['game_moi'])
        new_btn.pack(side='left', padx=5)
        
        # Hint button cho AI
        if quan_ly_cai_dat.lay_cai_dat('game_mode') == 'ai':
            hint_btn = tk.Button(buttons_container, text="💡 Gợi ý", 
                               font=font_size, 
                               bg=self.quan_ly_ui.mau_sac['info'], fg='white',
                               width=button_width, height=button_height,
                               command=self.callbacks['goi_y'])
            hint_btn.pack(side='left', padx=5)
        
        # Undo button
        undo_btn = tk.Button(buttons_container, text="↶ Hoàn tác", 
                           font=font_size, 
                           bg=self.quan_ly_ui.mau_sac['secondary'], fg='white',
                           width=button_width, height=button_height,
                           command=self.callbacks['hoan_tac'])
        undo_btn.pack(side='left', padx=5)
