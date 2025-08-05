# game_state.py - Quản lý trạng thái game
class TrangThaiGame:
    """Class quản lý trạng thái tổng thể của game"""
    
    def __init__(self, kich_thuoc=5):
        self.kich_thuoc = kich_thuoc
        self.ban_co = []
        self.nguoi_choi_hien_tai = 'X'
        self.diem_so = {'X': 0, 'O': 0}
        self.lich_su_nuoc_di = []
        self.game_dang_chay = False
        self.la_luot_ai = False
        self.khoi_tao_game()
    
    def khoi_tao_game(self):
        """Khởi tạo game mới"""
        self.ban_co = [['' for _ in range(self.kich_thuoc)] for _ in range(self.kich_thuoc)]
        self.nguoi_choi_hien_tai = 'X'
        self.lich_su_nuoc_di = []
        self.game_dang_chay = True
        self.la_luot_ai = False
    
    def dat_quan(self, hang, cot, nguoi_choi=None):
        """Đặt quân cờ lên bàn"""
        if nguoi_choi is None:
            nguoi_choi = self.nguoi_choi_hien_tai
        
        if self.kiem_tra_nuoc_di_hop_le(hang, cot):
            self.ban_co[hang][cot] = nguoi_choi
            self.lich_su_nuoc_di.append((hang, cot, nguoi_choi))
            return True
        return False
    
    def kiem_tra_nuoc_di_hop_le(self, hang, cot):
        """Kiểm tra nước đi có hợp lệ không"""
        return (self.game_dang_chay and 
                0 <= hang < self.kich_thuoc and 
                0 <= cot < self.kich_thuoc and 
                self.ban_co[hang][cot] == '')
    
    def chuyen_luot(self):
        """Chuyển lượt chơi"""
        self.nguoi_choi_hien_tai = 'O' if self.nguoi_choi_hien_tai == 'X' else 'X'
    
    def hoan_tac_nuoc_di(self):
        """Hoàn tác nước đi cuối cùng"""
        if self.lich_su_nuoc_di:
            hang, cot, nguoi_choi = self.lich_su_nuoc_di.pop()
            self.ban_co[hang][cot] = ''
            return True
        return False
    
    def lay_cac_o_trong(self):
        """Lấy danh sách các ô trống"""
        cac_o_trong = []
        for hang in range(self.kich_thuoc):
            for cot in range(self.kich_thuoc):
                if self.ban_co[hang][cot] == '':
                    cac_o_trong.append((hang, cot))
        return cac_o_trong
    
    def cap_nhat_diem(self, nguoi_thang):
        """Cập nhật điểm số"""
        if nguoi_thang in self.diem_so:
            self.diem_so[nguoi_thang] += 1
    
    def reset_diem(self):
        """Reset điểm số về 0"""
        self.diem_so = {'X': 0, 'O': 0}
    
    def dat_trang_thai_game(self, trang_thai):
        """Đặt trạng thái game (đang chạy/dừng)"""
        self.game_dang_chay = trang_thai
    
    def dat_luot_ai(self, la_luot_ai):
        """Đặt lượt AI"""
        self.la_luot_ai = la_luot_ai
        
    def lay_trang_thai(self):
        """Lấy trạng thái hiện tại của game"""
        return {
            'ban_co': [hang[:] for hang in self.ban_co],
            'nguoi_choi_hien_tai': self.nguoi_choi_hien_tai,
            'diem_so': self.diem_so.copy(),
            'game_dang_chay': self.game_dang_chay,
            'so_nuoc_da_di': len(self.lich_su_nuoc_di)
        }
