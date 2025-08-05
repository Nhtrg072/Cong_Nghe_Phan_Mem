import tkinter as tk
from tkinter import messagebox

# Import các class đã tách
from game_state import TrangThaiGame
from game_board import BanCo
from ai_player import AIPlayer
from ui_manager import QuanLyGiaoDien
from settings_manager import QuanLyCaiDat
from game_screen import ManHinhGame
from settings_screen import ManHinhCaiDat
from game_controller import GameController

# Class chính ngắn gọn
class GameCaro:
    def __init__(self):
        # Khởi tạo cơ bản
        self.root = tk.Tk()
        self.root.title("Game Cờ Caro - OOP Structure")
        self.root.geometry("800x800")
        self.root.resizable(False, False)  # Cố định kích thước
        
        # Khởi tạo managers
        self.quan_ly_cai_dat = QuanLyCaiDat()
        self.quan_ly_ui = QuanLyGiaoDien(self.root, self.quan_ly_cai_dat)
        self.trang_thai_game = TrangThaiGame()
        
        # Khởi tạo game components
        self.cap_nhat_game_components()
        
        # Khởi tạo màn hình
        self.man_hinh_game = ManHinhGame(self.root, self.quan_ly_ui, self.lay_callbacks_game())
        self.man_hinh_cai_dat = ManHinhCaiDat(self.root, self.quan_ly_ui, self.lay_callbacks_cai_dat())
        
        # Hiển thị menu
        self.hien_menu()
    
    def cap_nhat_game_components(self):
        """Cập nhật bàn cờ, AI và controller"""
        kich_thuoc = self.quan_ly_cai_dat.lay_cai_dat('board_size')
        dieu_kien_thang = self.quan_ly_cai_dat.lay_cai_dat('win_condition')
        do_kho_ai = self.quan_ly_cai_dat.lay_cai_dat('ai_difficulty')
        
        self.ban_co = BanCo(kich_thuoc, dieu_kien_thang)
        self.ai_player = AIPlayer(do_kho_ai)
        self.game_controller = GameController(self.trang_thai_game, self.ban_co, 
                                            self.ai_player, self.quan_ly_ui, self.quan_ly_cai_dat)
    
    def hien_menu(self):
        """Hiển thị menu chính"""
        callbacks = {
            'choi_voi_nguoi': lambda: self.bat_dau_game('human'),
            'choi_voi_may': lambda: self.bat_dau_game('ai'),
            'cai_dat': self.hien_cai_dat,
            'huong_dan': self.hien_huong_dan,
            'thoat': self.thoat_game
        }
        self.quan_ly_ui.hien_menu(callbacks)
    
    def lay_callbacks_game(self):
        """Lấy callbacks cho màn hình game"""
        return {
            've_menu': self.hien_menu,
            'cai_dat': self.hien_cai_dat,
            'nuoc_di': self.xu_ly_nuoc_di,
            'reset': self.reset_game,
            'game_moi': self.game_moi,
            'goi_y': self.game_controller.hien_goi_y,
            'hoan_tac': self.game_controller.hoan_tac_nuoc_di,
            'xu_ly_phim': self.xu_ly_phim_tat
        }
    
    def lay_callbacks_cai_dat(self):
        """Lấy callbacks cho màn hình cài đặt"""
        return {
            've_menu': self.hien_menu,
            'luu_cai_dat': self.luu_cai_dat
        }
    
    def bat_dau_game(self, che_do):
        """Bắt đầu game"""
        self.quan_ly_cai_dat.dat_cai_dat('game_mode', che_do)
        self.trang_thai_game.khoi_tao_game_moi(self.quan_ly_cai_dat.lay_cai_dat('board_size'))
        self.man_hinh_game.hien_thi(self.trang_thai_game, self.quan_ly_cai_dat)
    
    def xu_ly_nuoc_di(self, hang, cot):
        """Xử lý nước đi"""
        can_goi_ai = self.game_controller.thuc_hien_nuoc_di(hang, cot)
        if can_goi_ai:
            self.root.after(500, self.game_controller.thuc_hien_nuoc_di_ai)
    
    def reset_game(self):
        """Reset game"""
        self.trang_thai_game.khoi_tao_game_moi(self.quan_ly_cai_dat.lay_cai_dat('board_size'))
        self.man_hinh_game.hien_thi(self.trang_thai_game, self.quan_ly_cai_dat)
        messagebox.showinfo("Reset", "Game đã được reset!")
    
    def game_moi(self):
        """Game mới"""
        self.trang_thai_game.reset_diem_so()
        self.reset_game()
        messagebox.showinfo("Game mới", "Bắt đầu game mới!")
    
    def hien_cai_dat(self):
        """Hiển thị cài đặt"""
        self.man_hinh_cai_dat.hien_thi(self.quan_ly_cai_dat)
    
    def luu_cai_dat(self, cai_dat_moi):
        """Lưu cài đặt"""
        theme_cu = self.quan_ly_cai_dat.lay_cai_dat('theme')
        self.quan_ly_cai_dat.cap_nhat_cai_dat(cai_dat_moi)
        
        # Cập nhật lại components
        self.cap_nhat_game_components()
        
        if theme_cu != self.quan_ly_cai_dat.lay_cai_dat('theme'):
            self.quan_ly_ui.thiet_lap_style()
            messagebox.showinfo("Cài đặt", "Cài đặt đã được lưu! Khởi động lại để áp dụng theme mới.")
        else:
            messagebox.showinfo("Cài đặt", "Cài đặt đã được lưu!")
    
    def hien_huong_dan(self):
        """Hiển thị hướng dẫn"""
        noi_dung = """
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
        """
        messagebox.showinfo("Hướng dẫn", noi_dung)
    
    def xu_ly_phim_tat(self, event):
        """Xử lý phím tắt"""
        key = event.char.lower()
        
        if key == 'r' and self.quan_ly_ui.man_hinh_hien_tai == 'game':
            self.reset_game()
        elif key == 'n' and self.quan_ly_ui.man_hinh_hien_tai == 'game':
            self.game_moi()
        elif key == 'h' and self.quan_ly_ui.man_hinh_hien_tai == 'game':
            self.game_controller.hien_goi_y()
        elif key == 'u' and self.quan_ly_ui.man_hinh_hien_tai == 'game':
            self.game_controller.hoan_tac_nuoc_di()
        elif key == 'q':
            self.thoat_game()
    
    def thoat_game(self):
        """Thoát game"""
        if messagebox.askyesno("Thoát", "Bạn có chắc muốn thoát game?"):
            self.quan_ly_cai_dat.luu_cai_dat()
            self.root.quit()
    
    def chay_game(self):
        """Chạy game"""
        # Căn giữa cửa sổ
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
        
        self.root.protocol("WM_DELETE_WINDOW", self.thoat_game)
        self.root.mainloop()

# Chạy game
if __name__ == "__main__":
    game = GameCaro()
    game.chay_game()
