# settings_manager.py - Quản lý cài đặt
import json
import os

class QuanLyCaiDat:
    """Class quản lý load/save cài đặt từ JSON file"""
    
    def __init__(self, ten_file='caro_settings.json'):
        self.ten_file = ten_file
        self.cai_dat_mac_dinh = {
            'kich_thuoc_ban_co': 5,
            'dieu_kien_thang': 5,
            'che_do_game': 'human',  # 'human' hoặc 'ai'
            'do_kho_ai': 'trung_binh',  # 'de', 'trung_binh', 'kho'
            'theme': 'light'  # 'light' hoặc 'dark'
        }
        self.cai_dat = self.cai_dat_mac_dinh.copy()
        self.tai_cai_dat()
    
    def tai_cai_dat(self):
        """Tải cài đặt từ file JSON"""
        try:
            if os.path.exists(self.ten_file):
                with open(self.ten_file, 'r', encoding='utf-8') as f:
                    cai_dat_da_luu = json.load(f)
                    self.cai_dat.update(cai_dat_da_luu)
                    self.kiem_tra_tinh_hop_le()
        except Exception as e:
            print(f"Lỗi khi tải cài đặt: {e}")
            self.cai_dat = self.cai_dat_mac_dinh.copy()
    
    def luu_cai_dat(self):
        """Lưu cài đặt ra file JSON"""
        try:
            with open(self.ten_file, 'w', encoding='utf-8') as f:
                json.dump(self.cai_dat, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Lỗi khi lưu cài đặt: {e}")
            return False
    
    def lay(self, key):
        """Lấy giá trị cài đặt theo key"""
        return self.cai_dat.get(key, self.cai_dat_mac_dinh.get(key))
    
    def dat(self, key, value):
        """Đặt giá trị cài đặt"""
        if key in self.cai_dat_mac_dinh:
            self.cai_dat[key] = value
            return True
        return False
    
    def lay_tat_ca(self):
        """Lấy tất cả cài đặt"""
        return self.cai_dat.copy()
    
    def reset_ve_mac_dinh(self):
        """Reset về cài đặt mặc định"""
        self.cai_dat = self.cai_dat_mac_dinh.copy()
    
    def kiem_tra_tinh_hop_le(self):
        """Kiểm tra và sửa các cài đặt không hợp lệ"""
        # Kiểm tra kích thước bàn cờ
        if self.lay('kich_thuoc_ban_co') not in self.lay_kich_thuoc_hop_le():
            self.dat('kich_thuoc_ban_co', 5)
        
        # Kiểm tra điều kiện thắng
        kich_thuoc = self.lay('kich_thuoc_ban_co')
        if self.lay('dieu_kien_thang') not in self.lay_dieu_kien_thang_hop_le(kich_thuoc):
            self.dat('dieu_kien_thang', min(5, kich_thuoc))
        
        # Kiểm tra độ khó AI
        if self.lay('do_kho_ai') not in self.lay_do_kho_ai_hop_le():
            self.dat('do_kho_ai', 'trung_binh')
        
        # Kiểm tra theme
        if self.lay('theme') not in self.lay_theme_hop_le():
            self.dat('theme', 'light')
        
        # Kiểm tra chế độ game
        if self.lay('che_do_game') not in ['human', 'ai']:
            self.dat('che_do_game', 'human')
    
    def lay_kich_thuoc_hop_le(self):
        """Lấy danh sách kích thước bàn cờ hợp lệ"""
        return list(range(3, 11))  # 3x3 đến 10x10
    
    def lay_dieu_kien_thang_hop_le(self, kich_thuoc=None):
        """Lấy danh sách điều kiện thắng hợp lệ"""
        if kich_thuoc is None:
            kich_thuoc = self.lay('kich_thuoc_ban_co')
        return list(range(3, min(kich_thuoc + 1, 7)))
    
    def lay_do_kho_ai_hop_le(self):
        """Lấy danh sách độ khó AI hợp lệ"""
        return ['de', 'trung_binh', 'kho']
    
    def lay_theme_hop_le(self):
        """Lấy danh sách theme hợp lệ"""
        return ['light', 'dark']
    
    def lay_che_do_game_hop_le(self):
        """Lấy danh sách chế độ game hợp lệ"""
        return ['human', 'ai']
    
    def lay_thong_tin_cai_dat(self):
        """Lấy thông tin chi tiết về cài đặt hiện tại"""
        info = {
            'Kích thước bàn cờ': f"{self.lay('kich_thuoc_ban_co')}x{self.lay('kich_thuoc_ban_co')}",
            'Điều kiện thắng': f"{self.lay('dieu_kien_thang')} quân liên tiếp",
            'Chế độ game': 'Chơi với máy' if self.lay('che_do_game') == 'ai' else 'Hai người chơi',
            'Độ khó AI': self.lay('do_kho_ai').title(),
            'Theme': 'Tối' if self.lay('theme') == 'dark' else 'Sáng'
        }
        return info
    
    def sao_luu_cai_dat(self, ten_file_backup=None):
        """Sao lưu cài đặt hiện tại"""
        if ten_file_backup is None:
            ten_file_backup = f"{self.ten_file}.backup"
        
        try:
            with open(ten_file_backup, 'w', encoding='utf-8') as f:
                json.dump(self.cai_dat, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Lỗi khi sao lưu cài đặt: {e}")
            return False
    
    def khoi_phuc_cai_dat(self, ten_file_backup=None):
        """Khôi phục cài đặt từ file backup"""
        if ten_file_backup is None:
            ten_file_backup = f"{self.ten_file}.backup"
        
        try:
            if os.path.exists(ten_file_backup):
                with open(ten_file_backup, 'r', encoding='utf-8') as f:
                    cai_dat_backup = json.load(f)
                    self.cai_dat.update(cai_dat_backup)
                    self.kiem_tra_tinh_hop_le()
                    return True
            return False
        except Exception as e:
            print(f"Lỗi khi khôi phục cài đặt: {e}")
            return False
