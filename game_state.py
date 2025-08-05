# Class quản lý trạng thái game
class TrangThaiGame:
    def __init__(self):
        # Trạng thái game
        self.ban_co = []  # bàn cờ
        self.nguoi_choi_hien_tai = 'X'  # người chơi hiện tại
        self.game_dang_choi = False  # game có đang chơi không
        self.diem_so = {'X': 0, 'O': 0}  # điểm số
        self.lich_su_nuoc_di = []  # lịch sử nước đi
        self.la_luot_ai = False  # có phải lượt AI không
    
    def khoi_tao_game_moi(self, kich_thuoc):
        """Khởi tạo game mới với kích thước bàn cờ"""
        self.ban_co = [['' for _ in range(kich_thuoc)] for _ in range(kich_thuoc)]
        self.nguoi_choi_hien_tai = 'X'
        self.game_dang_choi = True
        self.lich_su_nuoc_di = []
        self.la_luot_ai = False
    
    def dat_quan_co(self, hang, cot, nguoi_choi):
        """Đặt quân cờ tại vị trí"""
        if self.ban_co[hang][cot] == '':
            self.ban_co[hang][cot] = nguoi_choi
            self.lich_su_nuoc_di.append((hang, cot, nguoi_choi))
            return True
        return False
    
    def chuyen_luot(self):
        """Chuyển lượt chơi"""
        self.nguoi_choi_hien_tai = 'O' if self.nguoi_choi_hien_tai == 'X' else 'X'
    
    def hoan_tac_nuoc_di(self, so_nuoc):
        """Hoàn tác số nước đi"""
        for _ in range(so_nuoc):
            if self.lich_su_nuoc_di:
                hang, cot, nguoi_choi = self.lich_su_nuoc_di.pop()
                self.ban_co[hang][cot] = ''
    
    def ket_thuc_game(self, nguoi_thang=None):
        """Kết thúc game và cập nhật điểm"""
        self.game_dang_choi = False
        if nguoi_thang:
            self.diem_so[nguoi_thang] += 1
    
    def reset_diem_so(self):
        """Reset điểm số về 0"""
        self.diem_so = {'X': 0, 'O': 0}
