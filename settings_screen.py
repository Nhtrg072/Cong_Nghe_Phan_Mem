# Class quản lý màn hình cài đặt
import tkinter as tk
from tkinter import messagebox, ttk

class ManHinhCaiDat:
    def __init__(self, root, quan_ly_ui, callbacks):
        self.root = root
        self.quan_ly_ui = quan_ly_ui
        self.callbacks = callbacks
        
        # Biến cho các control
        self.board_size_var = None
        self.win_condition_var = None
        self.ai_difficulty_var = None
        self.theme_var = None
        self.win_condition_combo = None
    
    def hien_thi(self, quan_ly_cai_dat):
        """Hiển thị màn hình cài đặt"""
        self.quan_ly_ui.xoa_man_hinh()
        self.quan_ly_ui.man_hinh_hien_tai = 'settings'
        
        # Tiêu đề
        title = tk.Label(
            self.root,
            text="⚙️ Cài đặt Game",
            font=self.quan_ly_ui.font_chu['title'],
            bg=self.quan_ly_ui.mau_sac['bg'],
            fg=self.quan_ly_ui.mau_sac['fg']
        )
        title.pack(pady=30)
        
        # Khung cài đặt
        settings_frame = tk.Frame(self.root, bg=self.quan_ly_ui.mau_sac['bg'])
        settings_frame.pack(pady=20, padx=50, fill='both', expand=True)
        
        # Các control cài đặt
        self.tao_cac_control_cai_dat(settings_frame, quan_ly_cai_dat)
        
        # Các nút
        self.tao_nut_dieu_khien(settings_frame)
    
    def tao_cac_control_cai_dat(self, parent, quan_ly_cai_dat):
        """Tạo các control cài đặt"""
        # Kích thước bàn cờ
        tk.Label(parent, text="Kích thước bàn cờ:", 
                font=self.quan_ly_ui.font_chu['heading'], 
                bg=self.quan_ly_ui.mau_sac['bg'], 
                fg=self.quan_ly_ui.mau_sac['fg']).pack(anchor='w', pady=(0, 5))
        
        self.board_size_var = tk.StringVar(value=str(quan_ly_cai_dat.lay_cai_dat('board_size')))
        board_size_combo = ttk.Combobox(parent, textvariable=self.board_size_var, 
                                      values=['3', '4', '5', '6', '7', '8', '9', '10'], 
                                      state='readonly', font=self.quan_ly_ui.font_chu['text'])
        board_size_combo.pack(fill='x', pady=(0, 15))
        board_size_combo.bind('<<ComboboxSelected>>', self.thay_doi_kich_thuoc_ban)
        
        # Điều kiện thắng
        tk.Label(parent, text="Số quân cần để thắng:", 
                font=self.quan_ly_ui.font_chu['heading'], 
                bg=self.quan_ly_ui.mau_sac['bg'], 
                fg=self.quan_ly_ui.mau_sac['fg']).pack(anchor='w', pady=(0, 5))
        
        self.win_condition_var = tk.StringVar(value=str(quan_ly_cai_dat.lay_cai_dat('win_condition')))
        self.win_condition_combo = ttk.Combobox(parent, textvariable=self.win_condition_var, 
                                              state='readonly', font=self.quan_ly_ui.font_chu['text'])
        self.win_condition_combo.pack(fill='x', pady=(0, 15))
        self.cap_nhat_tuy_chon_win_condition(quan_ly_cai_dat)
        
        # Độ khó AI
        tk.Label(parent, text="Độ khó AI:", 
                font=self.quan_ly_ui.font_chu['heading'], 
                bg=self.quan_ly_ui.mau_sac['bg'], 
                fg=self.quan_ly_ui.mau_sac['fg']).pack(anchor='w', pady=(0, 5))
        
        self.ai_difficulty_var = tk.StringVar(value=quan_ly_cai_dat.lay_cai_dat('ai_difficulty'))
        ai_combo = ttk.Combobox(parent, textvariable=self.ai_difficulty_var, 
                              values=['easy', 'medium', 'hard'], state='readonly', 
                              font=self.quan_ly_ui.font_chu['text'])
        ai_combo.pack(fill='x', pady=(0, 15))
        
        # Giao diện
        tk.Label(parent, text="Giao diện:", 
                font=self.quan_ly_ui.font_chu['heading'], 
                bg=self.quan_ly_ui.mau_sac['bg'], 
                fg=self.quan_ly_ui.mau_sac['fg']).pack(anchor='w', pady=(0, 5))
        
        self.theme_var = tk.StringVar(value=quan_ly_cai_dat.lay_cai_dat('theme'))
        theme_combo = ttk.Combobox(parent, textvariable=self.theme_var, 
                                 values=['default', 'dark'], state='readonly', 
                                 font=self.quan_ly_ui.font_chu['text'])
        theme_combo.pack(fill='x', pady=(0, 15))
    
    def tao_nut_dieu_khien(self, parent):
        """Tạo các nút điều khiển"""
        button_frame = tk.Frame(parent, bg=self.quan_ly_ui.mau_sac['bg'])
        button_frame.pack(pady=30)
        
        save_btn = tk.Button(button_frame, text="💾 Lưu cài đặt", 
                           font=self.quan_ly_ui.font_chu['button'], 
                           bg=self.quan_ly_ui.mau_sac['success'], fg='white', 
                           command=self.luu_cai_dat)
        save_btn.pack(side='left', padx=10)
        
        back_btn = tk.Button(button_frame, text="🔙 Quay lại", 
                           font=self.quan_ly_ui.font_chu['button'], 
                           bg=self.quan_ly_ui.mau_sac['secondary'], fg='white', 
                           command=self.callbacks['ve_menu'])
        back_btn.pack(side='right', padx=10)
    
    def thay_doi_kich_thuoc_ban(self, event=None):
        """Xử lý thay đổi kích thước bàn"""
        kich_thuoc = int(self.board_size_var.get())
        cac_tuy_chon = [str(i) for i in range(3, min(kich_thuoc + 1, 7))]
        self.win_condition_combo['values'] = cac_tuy_chon
        if self.win_condition_var.get() not in cac_tuy_chon:
            self.win_condition_var.set(str(min(5, kich_thuoc)))
    
    def cap_nhat_tuy_chon_win_condition(self, quan_ly_cai_dat):
        """Cập nhật tùy chọn win condition"""
        kich_thuoc = int(self.board_size_var.get())
        cac_tuy_chon = quan_ly_cai_dat.lay_cac_gia_tri_win_condition(kich_thuoc)
        self.win_condition_combo['values'] = cac_tuy_chon
        if self.win_condition_var.get() not in cac_tuy_chon:
            self.win_condition_var.set(str(min(5, kich_thuoc)))
    
    def luu_cai_dat(self):
        """Lưu cài đặt"""
        cai_dat_moi = {
            'board_size': int(self.board_size_var.get()),
            'win_condition': int(self.win_condition_var.get()),
            'ai_difficulty': self.ai_difficulty_var.get(),
            'theme': self.theme_var.get()
        }
        
        self.callbacks['luu_cai_dat'](cai_dat_moi)
