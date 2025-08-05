# game_controller.py - Điều khiển luồng game
from tkinter import messagebox

class GameController:
    """Class điều khiển luồng game, kết nối giữa UI và game logic"""
    
    def __init__(self, trang_thai_game, ban_co_logic, ai_player=None):
        self.trang_thai_game = trang_thai_game
        self.ban_co_logic = ban_co_logic
        self.ai_player = ai_player
        self.ui_callback = None
        self.cac_o_thang = []
    
    def dat_ui_callback(self, callback):
        """Đặt callback để cập nhật UI"""
        self.ui_callback = callback
    
    def xu_ly_nuoc_di(self, hang, cot):
        """Xử lý nước đi của người chơi"""
        if (not self.trang_thai_game.game_dang_chay or 
            not self.trang_thai_game.kiem_tra_nuoc_di_hop_le(hang, cot) or 
            self.trang_thai_game.la_luot_ai):
            return False
        
        # Thực hiện nước đi
        nguoi_choi = self.trang_thai_game.nguoi_choi_hien_tai
        if self.trang_thai_game.dat_quan(hang, cot, nguoi_choi):
            # Cập nhật UI
            if self.ui_callback:
                self.ui_callback('cap_nhat_o', hang, cot, nguoi_choi)
            
            # Kiểm tra thắng
            co_thang, cac_o_thang = self.ban_co_logic.kiem_tra_thang(
                self.trang_thai_game.ban_co, hang, cot, nguoi_choi)
            
            if co_thang:
                self._xu_ly_ket_thuc_game('thang', nguoi_choi, cac_o_thang)
                return True
            
            # Kiểm tra hòa
            if self.ban_co_logic.kiem_tra_hoa(self.trang_thai_game.ban_co):
                self._xu_ly_ket_thuc_game('hoa')
                return True
            
            # Chuyển lượt
            self.trang_thai_game.chuyen_luot()
            if self.ui_callback:
                self.ui_callback('cap_nhat_nguoi_choi', self.trang_thai_game.nguoi_choi_hien_tai)
            
            # Lượt AI (nếu có)
            if (self.ai_player and 
                self.trang_thai_game.nguoi_choi_hien_tai == self.ai_player.ky_hieu):
                self.trang_thai_game.dat_luot_ai(True)
                if self.ui_callback:
                    # Delay một chút để AI không đi quá nhanh
                    self.ui_callback('delay_ai', 500)
        
        return True
    
    def xu_ly_luot_ai(self):
        """Xử lý lượt của AI"""
        if (not self.trang_thai_game.game_dang_chay or 
            not self.ai_player or 
            not self.trang_thai_game.la_luot_ai):
            return
        
        nuoc_di = self.ai_player.lay_nuoc_di(self.trang_thai_game, self.ban_co_logic)
        if nuoc_di:
            self.trang_thai_game.dat_luot_ai(False)
            self.xu_ly_nuoc_di(nuoc_di[0], nuoc_di[1])
    
    def _xu_ly_ket_thuc_game(self, ket_qua, nguoi_thang=None, cac_o_thang=None):
        """Xử lý khi game kết thúc"""
        self.trang_thai_game.dat_trang_thai_game(False)
        
        if ket_qua == 'thang':
            # Cập nhật điểm
            self.trang_thai_game.cap_nhat_diem(nguoi_thang)
            
            # Highlight các ô thắng
            if cac_o_thang:
                self.cac_o_thang = cac_o_thang
                if self.ui_callback:
                    self.ui_callback('highlight_thang', cac_o_thang)
            
            # Hiển thị thông báo
            self._hien_thi_thong_bao_thang(nguoi_thang)
        
        elif ket_qua == 'hoa':
            self._hien_thi_thong_bao_hoa()
        
        # Vô hiệu hóa bàn cờ
        if self.ui_callback:
            self.ui_callback('vo_hieu_hoa_ban_co')
    
    def _hien_thi_thong_bao_thang(self, nguoi_thang):
        """Hiển thị thông báo thắng"""
        if self.ai_player:
            if nguoi_thang == 'X':
                tieu_de = "🎉 Bạn thắng!"
                thong_bao = "Chúc mừng! Bạn đã đánh bại máy tính!"
            else:
                tieu_de = "🤖 Máy thắng!"
                thong_bao = "Máy tính đã thắng! Hãy thử lại nhé!"
        else:
            tieu_de = f"🎉 Người chơi {nguoi_thang} thắng!"
            thong_bao = f"Chúc mừng! Người chơi {nguoi_thang} đã giành chiến thắng!"
        
        if self.ui_callback:
            self.ui_callback('cap_nhat_trang_thai', tieu_de)
        messagebox.showinfo("Kết quả", thong_bao)
    
    def _hien_thi_thong_bao_hoa(self):
        """Hiển thị thông báo hòa"""
        tieu_de = "🤝 Hòa!"
        thong_bao = "Trận đấu kết thúc với kết quả hòa!"
        
        if self.ui_callback:
            self.ui_callback('cap_nhat_trang_thai', tieu_de)
        messagebox.showinfo("Kết quả", thong_bao)
    
    def reset_game(self):
        """Reset game"""
        self.trang_thai_game.khoi_tao_game()
        self.cac_o_thang = []
        if self.ui_callback:
            self.ui_callback('reset_ui')
        messagebox.showinfo("Reset", "Game đã được reset!")
    
    def game_moi(self):
        """Bắt đầu game mới"""
        self.trang_thai_game.reset_diem()
        self.reset_game()
        messagebox.showinfo("Game mới", "Bắt đầu game mới!")
    
    def hoan_tac(self):
        """Hoàn tác nước đi"""
        if not self.trang_thai_game.lich_su_nuoc_di:
            messagebox.showwarning("Hoàn tác", "Không có nước đi nào để hoàn tác!")
            return
        
        # Số nước cần hoàn tác (1 cho người vs người, 2 cho người vs AI)
        so_nuoc_hoan_tac = 2 if self.ai_player else 1
        so_nuoc_hoan_tac = min(so_nuoc_hoan_tac, len(self.trang_thai_game.lich_su_nuoc_di))
        
        for _ in range(so_nuoc_hoan_tac):
            if self.trang_thai_game.hoan_tac_nuoc_di():
                # Lấy nước đi cuối để xóa UI
                if self.trang_thai_game.lich_su_nuoc_di:
                    nuoc_di_cuoi = self.trang_thai_game.lich_su_nuoc_di[-1]
                    if self.ui_callback:
                        self.ui_callback('xoa_o', nuoc_di_cuoi[0], nuoc_di_cuoi[1])
        
        # Reset trạng thái
        so_nuoc_da_di = len(self.trang_thai_game.lich_su_nuoc_di)
        self.trang_thai_game.nguoi_choi_hien_tai = 'X' if so_nuoc_da_di % 2 == 0 else 'O'
        self.trang_thai_game.dat_luot_ai(False)
        
        if self.ui_callback:
            self.ui_callback('cap_nhat_nguoi_choi', self.trang_thai_game.nguoi_choi_hien_tai)
    
    def lay_goi_y(self):
        """Lấy gợi ý từ AI"""
        if (not self.ai_player or 
            self.trang_thai_game.nguoi_choi_hien_tai != 'X'):
            messagebox.showwarning("Gợi ý", "Gợi ý chỉ khả dụng khi chơi với máy và đến lượt bạn!")
            return None
        
        goi_y = self.ai_player.lay_goi_y(self.trang_thai_game, self.ban_co_logic)
        if goi_y and self.ui_callback:
            self.ui_callback('hien_thi_goi_y', goi_y)
            messagebox.showinfo("Gợi ý", f"Đề xuất: Hàng {goi_y[0]+1}, Cột {goi_y[1]+1}")
        
        return goi_y
    
    def dat_ai_player(self, ai_player):
        """Đặt AI player mới"""
        self.ai_player = ai_player
