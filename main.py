#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Game Cờ Caro - Restructured OOP Version
Cấu trúc theo yêu cầu: main.py với class GameCaro điều khiển tổng thể
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Import các module theo cấu trúc mới
from game_state import TrangThaiGame
from game_board import BanCo
from ai_player import AIPlayer
from game_controller import GameController
from ui_manager import QuanLyGiaoDien
from game_screen import ManHinhGame
from settings_screen import ManHinhCaiDat
from settings_manager import QuanLyCaiDat

class GameCaro:
    """Class chính điều khiển tổng thể toàn bộ game, kết nối tất cả components"""
    
    def __init__(self):
        # Khởi tạo cửa sổ chính
        self.cua_so_chinh = tk.Tk()
        self.cua_so_chinh.title("Game Cờ Caro - Advanced OOP")
        self.cua_so_chinh.resizable(False, False)
        
        # Khởi tạo các managers
        self.quan_ly_cai_dat = QuanLyCaiDat()
        self.quan_ly_ui = QuanLyGiaoDien(self.quan_ly_cai_dat.lay('theme'))
        
        # Khởi tạo game components
        self.trang_thai_game = None
        self.ban_co_logic = None
        self.ai_player = None
        self.controller = None
        
        # Khởi tạo screens
        self.man_hinh_game = None
        self.man_hinh_cai_dat = None
        
        # Trạng thái hiện tại
        self.man_hinh_hien_tai = 'menu'
        
        # Thiết lập giao diện và hiển thị menu
        self.thiet_lap_giao_dien()
        self.hien_thi_menu()
        
        # Thiết lập sự kiện đóng cửa sổ
        self.cua_so_chinh.protocol("WM_DELETE_WINDOW", self.thoat_game)
    
    def thiet_lap_giao_dien(self):
        """Thiết lập giao diện cơ bản"""
        # Cấu hình cửa sổ
        mau_sac = self.quan_ly_ui.lay_tat_ca_mau()
        self.cua_so_chinh.configure(bg=mau_sac['nen'])
        
        # Căn giữa cửa sổ
        self.quan_ly_ui.can_giua_cua_so(self.cua_so_chinh)
        
        # Thiết lập phím tắt toàn cục
        self.cua_so_chinh.bind('<Key>', self.xu_ly_phim_tat_toan_cuc)
    
    def xoa_man_hinh(self):
        """Xóa tất cả widget trên màn hình"""
        for widget in self.cua_so_chinh.winfo_children():
            widget.destroy()
    
    # ===== MENU CHÍNH =====
    def hien_thi_menu(self):
        """Hiển thị menu chính"""
        self.man_hinh_hien_tai = 'menu'
        self.xoa_man_hinh()
        
        # Tiêu đề
        style_tieu_de = self.quan_ly_ui.tao_style_label('tieu_de')
        tieu_de = tk.Label(
            self.cua_so_chinh, 
            text="🎮 GAME CỜ CARO 🎮",
            **style_tieu_de
        )
        tieu_de.pack(pady=50)
        
        # Frame chứa các nút menu
        style_frame = self.quan_ly_ui.tao_style_frame()
        button_frame = tk.Frame(self.cua_so_chinh, **style_frame)
        button_frame.pack(pady=20)
        
        # Các nút menu
        cac_nut_menu = [
            ("👥 Chơi với người", lambda: self.bat_dau_game('human')),
            ("🤖 Chơi với máy", lambda: self.bat_dau_game('ai')),
            ("⚙️ Cài đặt", self.hien_thi_cai_dat),
            ("ℹ️ Hướng dẫn", self.hien_thi_huong_dan),
            ("❌ Thoát", self.thoat_game)
        ]
        
        for text, command in cac_nut_menu:
            style_nut = self.quan_ly_ui.tao_style_nut('chinh')
            nut = tk.Button(
                button_frame,
                text=text,
                command=command,
                width=20,
                height=2,
                **style_nut
            )
            nut.pack(pady=10)
    
    # ===== GAME LOGIC =====
    def bat_dau_game(self, che_do):
        """Bắt đầu game với chế độ được chọn"""
        # Cập nhật cài đặt chế độ game
        self.quan_ly_cai_dat.dat('che_do_game', che_do)
        
        # Khởi tạo game components
        self.khoi_tao_game_components()
        
        # Hiển thị màn hình game
        self.hien_thi_man_hinh_game()
    
    def khoi_tao_game_components(self):
        """Khởi tạo các components của game"""
        # Tạo trạng thái game
        self.trang_thai_game = TrangThaiGame(
            kich_thuoc=self.quan_ly_cai_dat.lay('kich_thuoc_ban_co')
        )
        
        # Tạo logic bàn cờ
        self.ban_co_logic = BanCo(
            kich_thuoc=self.quan_ly_cai_dat.lay('kich_thuoc_ban_co'),
            dieu_kien_thang=self.quan_ly_cai_dat.lay('dieu_kien_thang')
        )
        
        # Tạo AI player nếu cần
        if self.quan_ly_cai_dat.lay('che_do_game') == 'ai':
            self.ai_player = AIPlayer(
                do_kho=self.quan_ly_cai_dat.lay('do_kho_ai'),
                ky_hieu='O'
            )
        else:
            self.ai_player = None
        
        # Tạo controller
        self.controller = GameController(
            self.trang_thai_game,
            self.ban_co_logic,
            self.ai_player
        )
    
    def hien_thi_man_hinh_game(self):
        """Hiển thị màn hình chơi game"""
        self.man_hinh_hien_tai = 'game'
        
        # Tạo màn hình game
        self.man_hinh_game = ManHinhGame(
            self.cua_so_chinh,
            self.quan_ly_ui,
            self.controller,
            self.quan_ly_cai_dat
        )
        
        # Thiết lập callbacks
        self.man_hinh_game.ve_menu = self.hien_thi_menu
        self.man_hinh_game.mo_settings = self.hien_thi_cai_dat
        self.man_hinh_game.thoat_game = self.thoat_game
        
        # Hiển thị
        self.man_hinh_game.hien_thi(self.trang_thai_game)
    
    # ===== CÀI ĐẶT =====
    def hien_thi_cai_dat(self):
        """Hiển thị màn hình cài đặt"""
        self.man_hinh_hien_tai = 'settings'
        
        # Tạo màn hình cài đặt
        self.man_hinh_cai_dat = ManHinhCaiDat(
            self.cua_so_chinh,
            self.quan_ly_ui,
            self.quan_ly_cai_dat
        )
        
        # Thiết lập callback
        self.man_hinh_cai_dat.quay_lai_menu = self.hien_thi_menu
        
        # Hiển thị
        self.man_hinh_cai_dat.hien_thi()
    
    # ===== HƯỚNG DẪN =====
    def hien_thi_huong_dan(self):
        """Hiển thị hướng dẫn chơi game"""
        noi_dung_huong_dan = """
🎯 MỤC TIÊU:
Đặt các quân cờ thành một hàng liên tiếp để thắng.

🎮 CÁCH CHƠI:
• Click vào ô trống để đặt quân
• Người chơi X luôn đi trước
• AI sẽ tự động đi sau bạn

⚙️ CÀI ĐẶT:
• Kích thước bàn: 3x3 đến 10x10
• Số quân thắng: 3-6 quân
• Độ khó AI: Dễ, Trung bình, Khó

⌨️ PHÍM TẮT:
• R: Chơi lại
• N: Game mới
• H: Gợi ý (chỉ với AI)
• U: Hoàn tác
• Q: Thoát

🤖 ĐỘ KHÓ AI:
• Dễ: Đi ngẫu nhiên
• Trung bình: Có chiến thuật
• Khó: Thuật toán thông minh

🎨 THEME:
• Sáng: Giao diện truyền thống
• Tối: Giao diện đậm chất game
        """
        messagebox.showinfo("Hướng dẫn", noi_dung_huong_dan)
    
    # ===== XỬ LÝ PHÍM TẮT =====
    def xu_ly_phim_tat_toan_cuc(self, event):
        """Xử lý phím tắt toàn cục"""
        phim = event.char.lower()
        
        # Phím tắt chung
        if phim == 'q':
            self.thoat_game()
        elif phim == 'm' and self.man_hinh_hien_tai != 'menu':
            self.hien_thi_menu()
        elif phim == 's' and self.man_hinh_hien_tai != 'settings':
            self.hien_thi_cai_dat()
        
        # Chuyển event cho màn hình game nếu đang ở đó
        if (self.man_hinh_hien_tai == 'game' and 
            hasattr(self.man_hinh_game, 'xu_ly_phim_tat')):
            self.man_hinh_game.xu_ly_phim_tat(event)
    
    # ===== THOÁT GAME =====
    def thoat_game(self):
        """Thoát game và lưu cài đặt"""
        if messagebox.askyesno("Thoát", "Bạn có chắc muốn thoát game?"):
            # Lưu cài đặt trước khi thoát
            self.quan_ly_cai_dat.luu_cai_dat()
            
            # Đóng cửa sổ
            self.cua_so_chinh.quit()
            self.cua_so_chinh.destroy()
    
    # ===== CHẠY GAME =====
    def chay_game(self):
        """Khởi chạy game"""
        try:
            # Thiết lập focus để nhận phím tắt
            self.cua_so_chinh.focus_set()
            
            # Bắt đầu main loop
            self.cua_so_chinh.mainloop()
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")
            print(f"Lỗi: {e}")
            import traceback
            traceback.print_exc()

def main():
    """Hàm main chạy game"""
    try:
        # Tạo và chạy game
        game = GameCaro()
        game.chay_game()
        
    except Exception as e:
        print(f"Lỗi khi khởi chạy game: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
