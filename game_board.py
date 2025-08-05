# game_board.py - Logic bàn cờ và quy tắc
class BanCo:
    """Class xử lý logic bàn cờ và quy tắc thắng/thua"""
    
    def __init__(self, kich_thuoc=5, dieu_kien_thang=5):
        self.kich_thuoc = kich_thuoc
        self.dieu_kien_thang = dieu_kien_thang
    
    def kiem_tra_thang(self, ban_co, hang, cot, nguoi_choi):
        """Kiểm tra xem có thắng hay không"""
        huong_kiem_tra = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for d_hang, d_cot in huong_kiem_tra:
            dem = 1
            cac_o_thang = [(hang, cot)]
            
            # Kiểm tra hướng dương
            for i in range(1, self.dieu_kien_thang):
                hang_moi, cot_moi = hang + i * d_hang, cot + i * d_cot
                if (0 <= hang_moi < self.kich_thuoc and 0 <= cot_moi < self.kich_thuoc and 
                    ban_co[hang_moi][cot_moi] == nguoi_choi):
                    dem += 1
                    cac_o_thang.append((hang_moi, cot_moi))
                else:
                    break
            
            # Kiểm tra hướng âm
            for i in range(1, self.dieu_kien_thang):
                hang_moi, cot_moi = hang - i * d_hang, cot - i * d_cot
                if (0 <= hang_moi < self.kich_thuoc and 0 <= cot_moi < self.kich_thuoc and 
                    ban_co[hang_moi][cot_moi] == nguoi_choi):
                    dem += 1
                    cac_o_thang.append((hang_moi, cot_moi))
                else:
                    break
            
            if dem >= self.dieu_kien_thang:
                return True, cac_o_thang
        
        return False, []
    
    def kiem_tra_hoa(self, ban_co):
        """Kiểm tra xem có hòa hay không (bàn cờ đầy)"""
        for hang in range(self.kich_thuoc):
            for cot in range(self.kich_thuoc):
                if ban_co[hang][cot] == '':
                    return False
        return True
    
    def tim_nuoc_di_co_the(self, ban_co):
        """Tìm tất cả nước đi có thể"""
        nuoc_di = []
        for hang in range(self.kich_thuoc):
            for cot in range(self.kich_thuoc):
                if ban_co[hang][cot] == '':
                    nuoc_di.append((hang, cot))
        return nuoc_di
    
    def tim_nuoc_di_thang(self, ban_co, nguoi_choi):
        """Tìm nước đi có thể thắng ngay"""
        for hang, cot in self.tim_nuoc_di_co_the(ban_co):
            # Thử đặt quân
            ban_co[hang][cot] = nguoi_choi
            co_thang, _ = self.kiem_tra_thang(ban_co, hang, cot, nguoi_choi)
            ban_co[hang][cot] = ''  # Hoàn tác
            
            if co_thang:
                return (hang, cot)
        return None
    
    def danh_gia_vi_tri(self, ban_co, hang, cot, nguoi_choi):
        """Đánh giá độ tốt của một vị trí"""
        diem = 0
        huong_kiem_tra = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for d_hang, d_cot in huong_kiem_tra:
            diem += self._dem_quan_lien_tiep(ban_co, hang, cot, d_hang, d_cot, nguoi_choi)
        
        return diem
    
    def _dem_quan_lien_tiep(self, ban_co, hang, cot, d_hang, d_cot, nguoi_choi):
        """Đếm số quân liên tiếp theo một hướng"""
        dem = 0
        
        # Đếm theo hướng dương
        for i in range(1, self.dieu_kien_thang):
            hang_moi, cot_moi = hang + i * d_hang, cot + i * d_cot
            if (0 <= hang_moi < self.kich_thuoc and 0 <= cot_moi < self.kich_thuoc and 
                ban_co[hang_moi][cot_moi] == nguoi_choi):
                dem += 1
            else:
                break
        
        # Đếm theo hướng âm
        for i in range(1, self.dieu_kien_thang):
            hang_moi, cot_moi = hang - i * d_hang, cot - i * d_cot
            if (0 <= hang_moi < self.kich_thuoc and 0 <= cot_moi < self.kich_thuoc and 
                ban_co[hang_moi][cot_moi] == nguoi_choi):
                dem += 1
            else:
                break
        
        return dem
    
    def lay_vi_tri_trung_tam(self):
        """Lấy vị trí trung tâm bàn cờ"""
        return (self.kich_thuoc // 2, self.kich_thuoc // 2)
    
    def kiem_tra_vi_tri_hop_le(self, hang, cot):
        """Kiểm tra vị trí có hợp lệ không"""
        return 0 <= hang < self.kich_thuoc and 0 <= cot < self.kich_thuoc
