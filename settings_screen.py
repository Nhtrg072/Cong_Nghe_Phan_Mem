# settings_screen.py - Màn hình cài đặt
import tkinter as tk
from tkinter import ttk, messagebox

class ManHinhCaiDat:
    """Class quản lý màn hình cài đặt game"""
    
    def __init__(self, cua_so_goc, quan_ly_ui, quan_ly_cai_dat):
        self.cua_so_goc = cua_so_goc
        self.quan_ly_ui = quan_ly_ui
        self.quan_ly_cai_dat = quan_ly_cai_dat
        
        # Biến lưu trữ cài đặt tạm thời
        self.bien_kich_thuoc = None
        self.bien_dieu_kien_thang = None
        self.bien_do_kho_ai = None
        self.bien_theme = None
        self.combo_dieu_kien_thang = None
    
    def hien_thi(self):
        """Hiển thị màn hình cài đặt"""
        self.xoa_man_hinh()
        
        # Tiêu đề
        self.tao_tieu_de()
        
        # Form cài đặt
        self.tao_form_cai_dat()
        
        # Nút điều khiển
        self.tao_nut_dieu_khien()
    
    def xoa_man_hinh(self):
        """Xóa tất cả widget trên màn hình"""
        for widget in self.cua_so_goc.winfo_children():
            widget.destroy()
    
    def tao_tieu_de(self):
        """Tạo tiêu đề màn hình"""
        style_label = self.quan_ly_ui.tao_style_label('tieu_de')
        tieu_de = tk.Label(
            self.cua_so_goc,
            text="⚙️ Cài đặt Game",
            **style_label
        )
        tieu_de.pack(pady=30)
    
    def tao_form_cai_dat(self):
        """Tạo form cài đặt chi tiết"""
        style_frame = self.quan_ly_ui.tao_style_frame()
        settings_frame = tk.Frame(self.cua_so_goc, **style_frame)
        settings_frame.pack(pady=20, padx=50, fill='both', expand=True)
        
        # Kích thước bàn cờ
        self.tao_cai_dat_kich_thuoc(settings_frame)
        
        # Điều kiện thắng
        self.tao_cai_dat_dieu_kien_thang(settings_frame)
        
        # Độ khó AI
        self.tao_cai_dat_do_kho_ai(settings_frame)
        
        # Theme
        self.tao_cai_dat_theme(settings_frame)
    
    def tao_cai_dat_kich_thuoc(self, parent):
        """Tạo cài đặt kích thước bàn cờ"""
        style_label = self.quan_ly_ui.tao_style_label('tieu_de_phu')
        
        tk.Label(
            parent, 
            text="Kích thước bàn cờ:", 
            **style_label
        ).pack(anchor='w', pady=(0, 5))
        
        self.bien_kich_thuoc = tk.StringVar(value=str(self.quan_ly_cai_dat.lay('kich_thuoc_ban_co')))
        
        combo_kich_thuoc = ttk.Combobox(
            parent, 
            textvariable=self.bien_kich_thuoc, 
            values=[str(i) for i in self.quan_ly_cai_dat.lay_kich_thuoc_hop_le()], 
            state='readonly',
            font=self.quan_ly_ui.lay_font('chu_thuong')
        )
        combo_kich_thuoc.pack(fill='x', pady=(0, 15))
        combo_kich_thuoc.bind('<<ComboboxSelected>>', self.thay_doi_kich_thuoc)
    
    def tao_cai_dat_dieu_kien_thang(self, parent):
        """Tạo cài đặt điều kiện thắng"""
        style_label = self.quan_ly_ui.tao_style_label('tieu_de_phu')
        
        tk.Label(
            parent, 
            text="Số quân cần để thắng:", 
            **style_label
        ).pack(anchor='w', pady=(0, 5))
        
        self.bien_dieu_kien_thang = tk.StringVar(value=str(self.quan_ly_cai_dat.lay('dieu_kien_thang')))
        
        self.combo_dieu_kien_thang = ttk.Combobox(
            parent, 
            textvariable=self.bien_dieu_kien_thang, 
            state='readonly',
            font=self.quan_ly_ui.lay_font('chu_thuong')
        )
        self.combo_dieu_kien_thang.pack(fill='x', pady=(0, 15))
        self.cap_nhat_dieu_kien_thang()
    
    def tao_cai_dat_do_kho_ai(self, parent):
        """Tạo cài đặt độ khó AI"""
        style_label = self.quan_ly_ui.tao_style_label('tieu_de_phu')
        
        tk.Label(
            parent, 
            text="Độ khó AI:", 
            **style_label
        ).pack(anchor='w', pady=(0, 5))
        
        self.bien_do_kho_ai = tk.StringVar(value=self.quan_ly_cai_dat.lay('do_kho_ai'))
        
        cac_do_kho = {
            'de': 'Dễ',
            'trung_binh': 'Trung bình', 
            'kho': 'Khó'
        }
        
        combo_do_kho = ttk.Combobox(
            parent, 
            textvariable=self.bien_do_kho_ai, 
            values=list(cac_do_kho.keys()), 
            state='readonly',
            font=self.quan_ly_ui.lay_font('chu_thuong')
        )
        combo_do_kho.pack(fill='x', pady=(0, 15))
    
    def tao_cai_dat_theme(self, parent):
        """Tạo cài đặt theme"""
        style_label = self.quan_ly_ui.tao_style_label('tieu_de_phu')
        
        tk.Label(
            parent, 
            text="Giao diện:", 
            **style_label
        ).pack(anchor='w', pady=(0, 5))
        
        self.bien_theme = tk.StringVar(value=self.quan_ly_cai_dat.lay('theme'))
        
        cac_theme = {
            'light': 'Sáng',
            'dark': 'Tối'
        }
        
        combo_theme = ttk.Combobox(
            parent, 
            textvariable=self.bien_theme, 
            values=list(cac_theme.keys()), 
            state='readonly',
            font=self.quan_ly_ui.lay_font('chu_thuong')
        )
        combo_theme.pack(fill='x', pady=(0, 15))
    
    def tao_nut_dieu_khien(self):
        """Tạo các nút điều khiển"""
        style_frame = self.quan_ly_ui.tao_style_frame()
        button_frame = tk.Frame(self.cua_so_goc, **style_frame)
        button_frame.pack(pady=30)
        
        # Nút lưu
        style_thanh_cong = self.quan_ly_ui.tao_style_nut('thanh_cong')
        nut_luu = tk.Button(
            button_frame, 
            text="💾 Lưu cài đặt", 
            command=self.luu_cai_dat,
            **style_thanh_cong
        )
        nut_luu.pack(side='left', padx=10)
        
        # Nút reset
        style_canh_bao = self.quan_ly_ui.tao_style_nut('canh_bao')
        nut_reset = tk.Button(
            button_frame, 
            text="🔄 Reset", 
            command=self.reset_cai_dat,
            **style_canh_bao
        )
        nut_reset.pack(side='left', padx=10)
        
        # Nút quay lại
        style_phu = self.quan_ly_ui.tao_style_nut('phu')
        nut_back = tk.Button(
            button_frame, 
            text="🔙 Quay lại", 
            command=self.quay_lai_menu,
            **style_phu
        )
        nut_back.pack(side='right', padx=10)
    
    def thay_doi_kich_thuoc(self, event=None):
        """Xử lý khi thay đổi kích thước bàn cờ"""
        self.cap_nhat_dieu_kien_thang()
    
    def cap_nhat_dieu_kien_thang(self):
        """Cập nhật các lựa chọn điều kiện thắng"""
        kich_thuoc = int(self.bien_kich_thuoc.get())
        cac_lua_chon = [str(i) for i in range(3, min(kich_thuoc + 1, 7))]
        self.combo_dieu_kien_thang['values'] = cac_lua_chon
        
        # Đặt giá trị mặc định nếu giá trị hiện tại không hợp lệ
        if self.bien_dieu_kien_thang.get() not in cac_lua_chon:
            self.bien_dieu_kien_thang.set(str(min(5, kich_thuoc)))
    
    def luu_cai_dat(self):
        """Lưu cài đặt"""
        theme_cu = self.quan_ly_cai_dat.lay('theme')
        
        # Cập nhật cài đặt mới
        cai_dat_moi = {
            'kich_thuoc_ban_co': int(self.bien_kich_thuoc.get()),
            'dieu_kien_thang': int(self.bien_dieu_kien_thang.get()),
            'do_kho_ai': self.bien_do_kho_ai.get(),
            'theme': self.bien_theme.get()
        }
        
        # Lưu vào file
        thanh_cong = True
        for key, value in cai_dat_moi.items():
            if not self.quan_ly_cai_dat.dat(key, value):
                thanh_cong = False
                break
        
        if thanh_cong:
            self.quan_ly_cai_dat.luu_cai_dat()
            
            # Kiểm tra thay đổi theme
            if theme_cu != self.bien_theme.get():
                messagebox.showinfo(
                    "Cài đặt", 
                    "Cài đặt đã được lưu! Khởi động lại để áp dụng theme mới."
                )
            else:
                messagebox.showinfo("Cài đặt", "Cài đặt đã được lưu!")
        else:
            messagebox.showerror("Lỗi", "Không thể lưu cài đặt!")
    
    def reset_cai_dat(self):
        """Reset về cài đặt mặc định"""
        if messagebox.askyesno("Reset", "Bạn có chắc muốn reset về cài đặt mặc định?"):
            self.quan_ly_cai_dat.reset_ve_mac_dinh()
            
            # Cập nhật giao diện
            self.bien_kich_thuoc.set(str(self.quan_ly_cai_dat.lay('kich_thuoc_ban_co')))
            self.bien_dieu_kien_thang.set(str(self.quan_ly_cai_dat.lay('dieu_kien_thang')))
            self.bien_do_kho_ai.set(self.quan_ly_cai_dat.lay('do_kho_ai'))
            self.bien_theme.set(self.quan_ly_cai_dat.lay('theme'))
            
            self.cap_nhat_dieu_kien_thang()
            messagebox.showinfo("Reset", "Đã reset về cài đặt mặc định!")
    
    def quay_lai_menu(self):
        """Callback để quay lại menu"""
        # Sẽ được implement trong main
        pass
