# ai_player.py - Trí tuệ nhân tạo
import random
import math

class AIPlayer:
    """Class AI với 3 độ khó: dễ, trung bình, khó"""
    
    def __init__(self, do_kho='trung_binh', ky_hieu='O'):
        self.do_kho = do_kho  # 'de', 'trung_binh', 'kho'
        self.ky_hieu = ky_hieu
        self.ky_hieu_doi_thu = 'X' if ky_hieu == 'O' else 'O'
    
    def lay_nuoc_di(self, trang_thai_game, ban_co_logic):
        """Lấy nước đi tốt nhất dựa trên độ khó"""
        if self.do_kho == 'de':
            return self._ai_de(trang_thai_game)
        elif self.do_kho == 'trung_binh':
            return self._ai_trung_binh(trang_thai_game, ban_co_logic)
        else:  # khó
            return self._ai_kho(trang_thai_game, ban_co_logic)
    
    def _ai_de(self, trang_thai_game):
        """AI dễ - đi ngẫu nhiên"""
        cac_o_trong = trang_thai_game.lay_cac_o_trong()
        if cac_o_trong:
            return random.choice(cac_o_trong)
        return None
    
    def _ai_trung_binh(self, trang_thai_game, ban_co_logic):
        """AI trung bình - có chiến thuật cơ bản"""
        ban_co = trang_thai_game.ban_co
        
        # 1. Kiểm tra nước thắng
        nuoc_thang = ban_co_logic.tim_nuoc_di_thang(ban_co, self.ky_hieu)
        if nuoc_thang:
            return nuoc_thang
        
        # 2. Chặn nước thắng của đối thủ
        nuoc_chan = ban_co_logic.tim_nuoc_di_thang(ban_co, self.ky_hieu_doi_thu)
        if nuoc_chan:
            return nuoc_chan
        
        # 3. Chiếm trung tâm nếu có thể
        trung_tam = ban_co_logic.lay_vi_tri_trung_tam()
        if ban_co[trung_tam[0]][trung_tam[1]] == '':
            return trung_tam
        
        # 4. Tìm vị trí tốt nhất
        return self._tim_vi_tri_tot_nhat(trang_thai_game, ban_co_logic)
    
    def _ai_kho(self, trang_thai_game, ban_co_logic):
        """AI khó - sử dụng minimax cho bàn nhỏ"""
        if trang_thai_game.kich_thuoc <= 5:
            return self._minimax_di(trang_thai_game, ban_co_logic)
        else:
            return self._ai_trung_binh(trang_thai_game, ban_co_logic)
    
    def _tim_vi_tri_tot_nhat(self, trang_thai_game, ban_co_logic):
        """Tìm vị trí tốt nhất dựa trên đánh giá"""
        ban_co = trang_thai_game.ban_co
        cac_o_trong = trang_thai_game.lay_cac_o_trong()
        
        if not cac_o_trong:
            return None
        
        diem_cao_nhat = -1
        vi_tri_tot_nhat = None
        
        for hang, cot in cac_o_trong:
            diem = ban_co_logic.danh_gia_vi_tri(ban_co, hang, cot, self.ky_hieu)
            if diem > diem_cao_nhat:
                diem_cao_nhat = diem
                vi_tri_tot_nhat = (hang, cot)
        
        return vi_tri_tot_nhat if vi_tri_tot_nhat else random.choice(cac_o_trong)
    
    def _minimax_di(self, trang_thai_game, ban_co_logic):
        """Thuật toán minimax"""
        diem_tot_nhat = -float('inf')
        nuoc_di_tot_nhat = None
        
        for hang, cot in trang_thai_game.lay_cac_o_trong():
            # Thử đi
            trang_thai_game.ban_co[hang][cot] = self.ky_hieu
            diem = self._minimax(trang_thai_game, ban_co_logic, False, 3)
            trang_thai_game.ban_co[hang][cot] = ''  # Hoàn tác
            
            if diem > diem_tot_nhat:
                diem_tot_nhat = diem
                nuoc_di_tot_nhat = (hang, cot)
        
        return nuoc_di_tot_nhat
    
    def _minimax(self, trang_thai_game, ban_co_logic, la_ai_di, do_sau):
        """Thuật toán minimax với độ sâu giới hạn"""
        if do_sau == 0:
            return self._danh_gia_ban_co(trang_thai_game, ban_co_logic)
        
        cac_nuoc_di = trang_thai_game.lay_cac_o_trong()
        if not cac_nuoc_di:
            return 0
        
        if la_ai_di:
            diem_cao_nhat = -float('inf')
            for hang, cot in cac_nuoc_di:
                trang_thai_game.ban_co[hang][cot] = self.ky_hieu
                diem = self._minimax(trang_thai_game, ban_co_logic, False, do_sau - 1)
                trang_thai_game.ban_co[hang][cot] = ''
                diem_cao_nhat = max(diem, diem_cao_nhat)
            return diem_cao_nhat
        else:
            diem_thap_nhat = float('inf')
            for hang, cot in cac_nuoc_di:
                trang_thai_game.ban_co[hang][cot] = self.ky_hieu_doi_thu
                diem = self._minimax(trang_thai_game, ban_co_logic, True, do_sau - 1)
                trang_thai_game.ban_co[hang][cot] = ''
                diem_thap_nhat = min(diem, diem_thap_nhat)
            return diem_thap_nhat
    
    def _danh_gia_ban_co(self, trang_thai_game, ban_co_logic):
        """Đánh giá tổng thể bàn cờ"""
        diem = 0
        ban_co = trang_thai_game.ban_co
        huong_kiem_tra = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for hang in range(trang_thai_game.kich_thuoc):
            for cot in range(trang_thai_game.kich_thuoc):
                for d_hang, d_cot in huong_kiem_tra:
                    diem += self._danh_gia_dong(ban_co, hang, cot, d_hang, d_cot, 
                                              ban_co_logic, self.ky_hieu) * 10
                    diem -= self._danh_gia_dong(ban_co, hang, cot, d_hang, d_cot, 
                                              ban_co_logic, self.ky_hieu_doi_thu) * 10
        
        return diem
    
    def _danh_gia_dong(self, ban_co, hang, cot, d_hang, d_cot, ban_co_logic, nguoi_choi):
        """Đánh giá một dòng theo hướng cụ thể"""
        dem = 0
        kich_thuoc = len(ban_co)
        dieu_kien_thang = ban_co_logic.dieu_kien_thang
        
        for i in range(dieu_kien_thang):
            h, c = hang + i * d_hang, cot + i * d_cot
            if (0 <= h < kich_thuoc and 0 <= c < kich_thuoc and 
                ban_co[h][c] == nguoi_choi):
                dem += 1
            else:
                break
        
        return dem
    
    def lay_goi_y(self, trang_thai_game, ban_co_logic):
        """Đưa ra gợi ý cho người chơi"""
        return self._ai_trung_binh(trang_thai_game, ban_co_logic)
