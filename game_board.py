# Class quản lý bàn cờ
class BanCo:
    def __init__(self, kich_thuoc=5, dieu_kien_thang=5):
        self.kich_thuoc = kich_thuoc
        self.dieu_kien_thang = dieu_kien_thang
    
    def kiem_tra_thang(self, ban_co, hang, cot, nguoi_choi):
        """Kiểm tra người chơi có thắng không"""
        cac_huong = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dr, dc in cac_huong:
            so_quan = 1
            cac_o_thang = [(hang, cot)]
            
            # Kiểm tra hướng dương
            for i in range(1, self.dieu_kien_thang):
                hang_moi, cot_moi = hang + i * dr, cot + i * dc
                if (0 <= hang_moi < self.kich_thuoc and 0 <= cot_moi < self.kich_thuoc and 
                    ban_co[hang_moi][cot_moi] == nguoi_choi):
                    so_quan += 1
                    cac_o_thang.append((hang_moi, cot_moi))
                else:
                    break
            
            # Kiểm tra hướng âm
            for i in range(1, self.dieu_kien_thang):
                hang_moi, cot_moi = hang - i * dr, cot - i * dc
                if (0 <= hang_moi < self.kich_thuoc and 0 <= cot_moi < self.kich_thuoc and 
                    ban_co[hang_moi][cot_moi] == nguoi_choi):
                    so_quan += 1
                    cac_o_thang.append((hang_moi, cot_moi))
                else:
                    break
            
            if so_quan >= self.dieu_kien_thang:
                return True, cac_o_thang
        
        return False, []
    
    def kiem_tra_hoa(self, ban_co):
        """Kiểm tra bàn cờ có hòa không"""
        for hang in range(self.kich_thuoc):
            for cot in range(self.kich_thuoc):
                if ban_co[hang][cot] == '':
                    return False
        return True
    
    def lay_cac_nuoc_di_co_the(self, ban_co):
        """Lấy danh sách các nước đi có thể"""
        cac_nuoc_di = []
        for hang in range(self.kich_thuoc):
            for cot in range(self.kich_thuoc):
                if ban_co[hang][cot] == '':
                    cac_nuoc_di.append((hang, cot))
        return cac_nuoc_di
    
    def tim_nuoc_thang(self, ban_co, nguoi_choi):
        """Tìm nước đi có thể thắng ngay"""
        for hang, cot in self.lay_cac_nuoc_di_co_the(ban_co):
            ban_co[hang][cot] = nguoi_choi
            co_thang, _ = self.kiem_tra_thang(ban_co, hang, cot, nguoi_choi)
            ban_co[hang][cot] = ''
            if co_thang:
                return (hang, cot)
        return None
