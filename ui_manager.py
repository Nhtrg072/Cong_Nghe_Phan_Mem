# ui_manager.py - Quản lý UI cơ bản
class QuanLyGiaoDien:
    """Class quản lý style, màu sắc, font chữ và themes"""
    
    def __init__(self, theme='light'):
        self.theme = theme
        self.thiet_lap_theme()
    
    def thiet_lap_theme(self):
        """Thiết lập theme màu sắc"""
        if self.theme == 'dark':
            self.mau_sac = {
                'nen': '#2d2d2d',
                'chu': '#ffffff',
                'chinh': '#4a90e2',
                'phu': '#6c757d',
                'thanh_cong': '#28a745',
                'nguy_hiem': '#dc3545',
                'canh_bao': '#ffc107',
                'thong_tin': '#17a2b8',
                'sang': '#3d3d3d',
                'nen_nut': '#4a4a4a',
                'vien': '#555555'
            }
        else:  # light theme
            self.mau_sac = {
                'nen': '#f0f2f5',
                'chu': '#2c3e50',
                'chinh': '#4a90e2',
                'phu': '#6c757d',
                'thanh_cong': '#28a745',
                'nguy_hiem': '#dc3545',
                'canh_bao': '#ffc107',
                'thong_tin': '#17a2b8',
                'sang': '#ffffff',
                'nen_nut': '#ffffff',
                'vien': '#dee2e6'
            }
        
        self.font_chu = {
            'tieu_de': ('Arial', 24, 'bold'),
            'tieu_de_phu': ('Arial', 16, 'bold'),
            'nut': ('Arial', 12, 'bold'),
            'chu_thuong': ('Arial', 10),
            'o_co': ('Arial', 20, 'bold'),
            'nho': ('Arial', 8)
        }
    
    def dat_theme(self, theme_moi):
        """Đặt theme mới"""
        self.theme = theme_moi
        self.thiet_lap_theme()
    
    def lay_mau(self, ten_mau):
        """Lấy màu theo tên"""
        return self.mau_sac.get(ten_mau, '#000000')
    
    def lay_font(self, ten_font):
        """Lấy font theo tên"""
        return self.font_chu.get(ten_font, ('Arial', 12))
    
    def lay_tat_ca_mau(self):
        """Lấy tất cả màu sắc"""
        return self.mau_sac.copy()
    
    def lay_tat_ca_font(self):
        """Lấy tất cả font chữ"""
        return self.font_chu.copy()
    
    def tinh_kich_thuoc_nut(self, kich_thuoc_ban_co):
        """Tính kích thước nút dựa trên kích thước bàn cờ"""
        kich_thuoc_nut = max(2, 8 - kich_thuoc_ban_co // 2)
        kich_thuoc_font = max(12, 24 - kich_thuoc_ban_co * 2)
        return kich_thuoc_nut, kich_thuoc_font
    
    def can_giua_cua_so(self, cua_so, rong=600, cao=700):
        """Căn giữa cửa sổ trên màn hình"""
        cua_so.update_idletasks()
        x = (cua_so.winfo_screenwidth() // 2) - (rong // 2)
        y = (cua_so.winfo_screenheight() // 2) - (cao // 2)
        cua_so.geometry(f"{rong}x{cao}+{x}+{y}")
    
    def tao_style_nut(self, loai_nut='chinh'):
        """Tạo style cho nút"""
        mau_nen = self.lay_mau(loai_nut)
        mau_chu = 'white' if loai_nut not in ['sang', 'nen_nut'] else self.lay_mau('chu')
        
        return {
            'font': self.lay_font('nut'),
            'bg': mau_nen,
            'fg': mau_chu,
            'relief': 'raised',
            'bd': 2,
            'cursor': 'hand2',
            'activebackground': self._lam_dam_mau(mau_nen),
            'activeforeground': mau_chu
        }
    
    def tao_style_label(self, loai_label='chu_thuong'):
        """Tạo style cho label"""
        return {
            'font': self.lay_font(loai_label),
            'bg': self.lay_mau('nen'),
            'fg': self.lay_mau('chu')
        }
    
    def tao_style_frame(self, co_vien=False):
        """Tạo style cho frame"""
        style = {
            'bg': self.lay_mau('nen')
        }
        
        if co_vien:
            style.update({
                'relief': 'raised',
                'bd': 1,
                'highlightbackground': self.lay_mau('vien'),
                'highlightthickness': 1
            })
        
        return style
    
    def _lam_dam_mau(self, mau_hex):
        """Làm đậm màu (cho active state)"""
        # Chuyển hex sang RGB
        mau_hex = mau_hex.lstrip('#')
        if len(mau_hex) == 6:
            r = int(mau_hex[0:2], 16)
            g = int(mau_hex[2:4], 16)
            b = int(mau_hex[4:6], 16)
            
            # Làm đậm 20%
            r = max(0, min(255, int(r * 0.8)))
            g = max(0, min(255, int(g * 0.8)))
            b = max(0, min(255, int(b * 0.8)))
            
            return f"#{r:02x}{g:02x}{b:02x}"
        
        return mau_hex  # Trả về màu gốc nếu không parse được
