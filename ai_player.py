import random
import math

# Class AI với các thuật toán
class AIPlayer:
    def __init__(self, do_kho='medium'):
        self.do_kho = do_kho
    
    def lay_nuoc_di_ai(self, ban_co_obj, trang_thai_game):
        """Lấy nước đi của AI theo độ khó"""
        if self.do_kho == 'easy':
            return self.nuoc_di_de(ban_co_obj, trang_thai_game.ban_co)
        elif self.do_kho == 'medium':
            return self.nuoc_di_trung_binh(ban_co_obj, trang_thai_game.ban_co)
        else:  # hard
            return self.nuoc_di_kho(ban_co_obj, trang_thai_game)
    
    def nuoc_di_de(self, ban_co_obj, ban_co):
        """AI dễ - đi ngẫu nhiên"""
        cac_nuoc_di = ban_co_obj.lay_cac_nuoc_di_co_the(ban_co)
        return random.choice(cac_nuoc_di) if cac_nuoc_di else None
    
    def nuoc_di_trung_binh(self, ban_co_obj, ban_co):
        """AI trung bình - có chiến thuật cơ bản"""
        # Kiểm tra nước thắng
        nuoc_di = ban_co_obj.tim_nuoc_thang(ban_co, 'O')
        if nuoc_di:
            return nuoc_di
        
        # Chặn nước thắng của người chơi
        nuoc_di = ban_co_obj.tim_nuoc_thang(ban_co, 'X')
        if nuoc_di:
            return nuoc_di
        
        # Đi ô giữa nếu còn trống
        giua = ban_co_obj.kich_thuoc // 2
        if ban_co[giua][giua] == '':
            return (giua, giua)
        
        # Đi ngẫu nhiên
        return self.nuoc_di_de(ban_co_obj, ban_co)
    
    def nuoc_di_kho(self, ban_co_obj, trang_thai_game):
        """AI khó - sử dụng minimax cho bàn nhỏ"""
        if ban_co_obj.kich_thuoc <= 5:
            return self.minimax_move(ban_co_obj, trang_thai_game.ban_co)
        else:
            return self.nuoc_di_trung_binh(ban_co_obj, trang_thai_game.ban_co)
    
    def minimax_move(self, ban_co_obj, ban_co):
        """Thuật toán minimax"""
        diem_cao_nhat = -float('inf')
        nuoc_di_tot_nhat = None
        
        for hang, cot in ban_co_obj.lay_cac_nuoc_di_co_the(ban_co):
            ban_co[hang][cot] = 'O'
            diem = self.minimax(ban_co_obj, ban_co, False, 3)
            ban_co[hang][cot] = ''
            
            if diem > diem_cao_nhat:
                diem_cao_nhat = diem
                nuoc_di_tot_nhat = (hang, cot)
        
        return nuoc_di_tot_nhat
    
    def minimax(self, ban_co_obj, ban_co, la_max, do_sau):
        """Thuật toán minimax đệ quy"""
        if do_sau == 0:
            return self.danh_gia_ban_co(ban_co_obj, ban_co)
        
        cac_nuoc_di = ban_co_obj.lay_cac_nuoc_di_co_the(ban_co)
        if not cac_nuoc_di:
            return 0
        
        if la_max:
            diem_max = -float('inf')
            for hang, cot in cac_nuoc_di:
                ban_co[hang][cot] = 'O'
                diem = self.minimax(ban_co_obj, ban_co, False, do_sau - 1)
                ban_co[hang][cot] = ''
                diem_max = max(diem, diem_max)
            return diem_max
        else:
            diem_min = float('inf')
            for hang, cot in cac_nuoc_di:
                ban_co[hang][cot] = 'X'
                diem = self.minimax(ban_co_obj, ban_co, True, do_sau - 1)
                ban_co[hang][cot] = ''
                diem_min = min(diem, diem_min)
            return diem_min
    
    def danh_gia_ban_co(self, ban_co_obj, ban_co):
        """Hàm đánh giá bàn cờ đơn giản"""
        diem = 0
        cac_huong = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for hang in range(ban_co_obj.kich_thuoc):
            for cot in range(ban_co_obj.kich_thuoc):
                for dr, dc in cac_huong:
                    diem += self.danh_gia_dong(ban_co_obj, ban_co, hang, cot, dr, dc, 'O') * 10
                    diem -= self.danh_gia_dong(ban_co_obj, ban_co, hang, cot, dr, dc, 'X') * 10
        
        return diem
    
    def danh_gia_dong(self, ban_co_obj, ban_co, hang, cot, dr, dc, nguoi_choi):
        """Đánh giá một dòng quân cờ"""
        so_quan = 0
        
        for i in range(ban_co_obj.dieu_kien_thang):
            r, c = hang + i * dr, cot + i * dc
            if (0 <= r < ban_co_obj.kich_thuoc and 
                0 <= c < ban_co_obj.kich_thuoc and 
                ban_co[r][c] == nguoi_choi):
                so_quan += 1
            else:
                break
        
        return so_quan
