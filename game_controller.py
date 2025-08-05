# Class điều khiển logic game
from tkinter import messagebox

class GameController:
    def __init__(self, trang_thai_game, ban_co, ai_player, quan_ly_ui, quan_ly_cai_dat):
        self.trang_thai_game = trang_thai_game
        self.ban_co = ban_co
        self.ai_player = ai_player
        self.quan_ly_ui = quan_ly_ui
        self.quan_ly_cai_dat = quan_ly_cai_dat
    
    def thuc_hien_nuoc_di(self, hang, cot):
        """Thực hiện nước đi"""
        # Kiểm tra xem có thể đi không
        if (not self.trang_thai_game.game_dang_choi or 
            self.trang_thai_game.ban_co[hang][cot] != '' or 
            self.trang_thai_game.la_luot_ai):
            return
        
        # Đặt quân cờ
        nguoi_choi = self.trang_thai_game.nguoi_choi_hien_tai
        self.trang_thai_game.dat_quan_co(hang, cot, nguoi_choi)
        
        # Cập nhật giao diện
        nut = self.quan_ly_ui.board_buttons[hang][cot]
        nut.config(text=nguoi_choi, state='disabled')
        if nguoi_choi == 'X':
            nut.config(fg=self.quan_ly_ui.mau_sac['danger'], bg='#ffe6e6')
        else:
            nut.config(fg=self.quan_ly_ui.mau_sac['primary'], bg='#e6f3ff')
        
        # Kiểm tra thắng/hòa
        co_thang, cac_o_thang = self.ban_co.kiem_tra_thang(self.trang_thai_game.ban_co, hang, cot, nguoi_choi)
        if co_thang:
            self.xu_ly_ket_thuc_game('win', nguoi_choi, cac_o_thang)
            return
        
        if self.ban_co.kiem_tra_hoa(self.trang_thai_game.ban_co):
            self.xu_ly_ket_thuc_game('draw')
            return
        
        # Chuyển lượt
        self.trang_thai_game.chuyen_luot()
        self.quan_ly_ui.cap_nhat_hien_thi_nguoi_choi(self.trang_thai_game.nguoi_choi_hien_tai)
        
        # Nước đi của AI
        if (self.quan_ly_cai_dat.lay_cai_dat('game_mode') == 'ai' and 
            self.trang_thai_game.nguoi_choi_hien_tai == 'O'):
            self.trang_thai_game.la_luot_ai = True
            return True  # Báo hiệu cần gọi AI
        
        return False
    
    def thuc_hien_nuoc_di_ai(self):
        """AI thực hiện nước đi"""
        if not self.trang_thai_game.game_dang_choi:
            return
        
        nuoc_di = self.ai_player.lay_nuoc_di_ai(self.ban_co, self.trang_thai_game)
        
        if nuoc_di:
            self.trang_thai_game.la_luot_ai = False
            self.thuc_hien_nuoc_di(nuoc_di[0], nuoc_di[1])
    
    def xu_ly_ket_thuc_game(self, ket_qua, nguoi_thang=None, cac_o_thang=None):
        """Xử lý kết thúc game"""
        self.trang_thai_game.ket_thuc_game(nguoi_thang)
        
        if ket_qua == 'win':
            if cac_o_thang:
                self.quan_ly_ui.lam_noi_bat_o_thang(cac_o_thang)
            
            if self.quan_ly_cai_dat.lay_cai_dat('game_mode') == 'ai':
                if nguoi_thang == 'X':
                    title = "🎉 Bạn thắng!"
                    message = "Chúc mừng! Bạn đã đánh bại máy tính!"
                else:
                    title = "🤖 Máy thắng!"
                    message = "Máy tính đã thắng! Hãy thử lại nhé!"
            else:
                title = f"🎉 Người chơi {nguoi_thang} thắng!"
                message = f"Chúc mừng! Người chơi {nguoi_thang} đã giành chiến thắng!"
            
            self.quan_ly_ui.status_label.config(text=title)
            messagebox.showinfo("Kết quả", message)
        else:
            title = "🤝 Hòa!"
            message = "Trận đấu kết thúc với kết quả hòa!"
            self.quan_ly_ui.status_label.config(text=title)
            messagebox.showinfo("Kết quả", message)
        
        self.quan_ly_ui.cap_nhat_hien_thi_diem(self.trang_thai_game.diem_so, 
                                              self.quan_ly_cai_dat.lay_cai_dat('game_mode'))
        self.quan_ly_ui.vo_hieu_hoa_tat_ca_nut()
    
    def hien_goi_y(self):
        """Hiển thị gợi ý"""
        if (self.quan_ly_cai_dat.lay_cai_dat('game_mode') != 'ai' or 
            self.trang_thai_game.nguoi_choi_hien_tai != 'X'):
            messagebox.showwarning("Gợi ý", "Gợi ý chỉ khả dụng khi chơi với máy và đến lượt bạn!")
            return
        
        # Tạo AI tạm để lấy gợi ý
        from ai_player import AIPlayer
        ai_tam = AIPlayer('medium')
        nuoc_di = ai_tam.lay_nuoc_di_ai(self.ban_co, self.trang_thai_game)
        
        if nuoc_di:
            nut = self.quan_ly_ui.board_buttons[nuoc_di[0]][nuoc_di[1]]
            mau_goc = nut.cget('bg')
            nut.config(bg='yellow')
            # Cần có root để dùng after
            import tkinter as tk
            root = nut.winfo_toplevel()
            root.after(2000, lambda: nut.config(bg=mau_goc))
            messagebox.showinfo("Gợi ý", f"Đề xuất: Hàng {nuoc_di[0]+1}, Cột {nuoc_di[1]+1}")
    
    def hoan_tac_nuoc_di(self):
        """Hoàn tác nước đi"""
        if not self.trang_thai_game.lich_su_nuoc_di:
            messagebox.showwarning("Hoàn tác", "Không có nước đi nào để hoàn tác!")
            return
        
        # Hoàn tác nước đi
        so_nuoc_hoan_tac = 2 if self.quan_ly_cai_dat.lay_cai_dat('game_mode') == 'ai' else 1
        so_nuoc_hoan_tac = min(so_nuoc_hoan_tac, len(self.trang_thai_game.lich_su_nuoc_di))
        
        for _ in range(so_nuoc_hoan_tac):
            if self.trang_thai_game.lich_su_nuoc_di:
                hang, cot, nguoi_choi = self.trang_thai_game.lich_su_nuoc_di.pop()
                self.trang_thai_game.ban_co[hang][cot] = ''
                nut = self.quan_ly_ui.board_buttons[hang][cot]
                nut.config(text='', state='normal', 
                          bg=self.quan_ly_ui.mau_sac['button_bg'], fg='black')
        
        # Đặt lại người chơi hiện tại
        so_nuoc = len(self.trang_thai_game.lich_su_nuoc_di)
        self.trang_thai_game.nguoi_choi_hien_tai = 'X' if so_nuoc % 2 == 0 else 'O'
        self.trang_thai_game.la_luot_ai = False
        self.quan_ly_ui.cap_nhat_hien_thi_nguoi_choi(self.trang_thai_game.nguoi_choi_hien_tai)
