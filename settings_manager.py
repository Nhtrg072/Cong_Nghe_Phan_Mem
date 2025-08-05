import json
import os

# Class quản lý cài đặt
class QuanLyCaiDat:
    def __init__(self):
        # Cài đặt mặc định
        self.cai_dat = {
            'board_size': 5,  # kích thước bàn cờ
            'win_condition': 5,  # số quân cần để thắng
            'game_mode': 'human',  # chế độ chơi
            'ai_difficulty': 'medium',  # độ khó AI
            'theme': 'default'  # giao diện
        }
        self.load_cai_dat()
    
    def load_cai_dat(self):
        """Load cài đặt từ file"""
        try:
            if os.path.exists('caro_settings.json'):
                with open('caro_settings.json', 'r') as f:
                    cai_dat_da_luu = json.load(f)
                    self.cai_dat.update(cai_dat_da_luu)
        except:
            pass
    
    def luu_cai_dat(self):
        """Lưu cài đặt vào file"""
        try:
            with open('caro_settings.json', 'w') as f:
                json.dump(self.cai_dat, f)
        except:
            pass
    
    def cap_nhat_cai_dat(self, cai_dat_moi):
        """Cập nhật cài đặt mới"""
        self.cai_dat.update(cai_dat_moi)
        self.luu_cai_dat()
    
    def lay_cai_dat(self, key):
        """Lấy giá trị cài đặt"""
        return self.cai_dat.get(key)
    
    def dat_cai_dat(self, key, value):
        """Đặt giá trị cài đặt"""
        self.cai_dat[key] = value
    
    def lay_cac_gia_tri_win_condition(self, kich_thuoc_ban):
        """Lấy các giá trị có thể cho win condition"""
        return [str(i) for i in range(3, min(kich_thuoc_ban + 1, 7))]
