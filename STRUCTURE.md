## 📁 Cấu trúc file:

### 🏗️ **File chính**:
- **`main.py`**  - File chính khởi chạy game
  - Class `GameCaro` - Điều khiển tổng thể toàn bộ game
  - Kết nối tất cả components lại với nhau
  - Xử lý callbacks và phím tắt

### 🧠 **Logic game**:
- **`game_state.py`** - Quản lý trạng thái game
  - Class `TrangThaiGame` - Lưu trữ bàn cờ, điểm số, lượt chơi
  - Methods: khởi tạo game, đặt quân, chuyển lượt, hoàn tác
  
- **`game_board.py`** - Logic bàn cờ và quy tắc
  - Class `BanCo` - Xử lý logic thắng/thua/hòa
  - Methods: kiểm tra thắng, kiểm tra hòa, tìm nước đi có thể
  
- **`ai_player.py`** - Trí tuệ nhân tạo
  - Class `AIPlayer` - AI với 3 độ khó (dễ, trung bình, khó)
  - Algorithms: Random, Strategic, Minimax
  
- **`game_controller.py`** - Điều khiển luồng game
  - Class `GameController` - Xử lý nước đi, AI turn, kết thúc game
  - Kết nối giữa UI và game logic

### 🎨 **Giao diện người dùng**:
- **`ui_manager.py`** - Quản lý UI cơ bản
  - Class `QuanLyGiaoDien` - Style, màu sắc, font chữ, themes
  - Thiết lập giao diện light/dark mode
  
- **`game_screen.py`** - Màn hình chơi game
  - Class `ManHinhGame` - Tạo bàn cờ, nút điều khiển, header
  - Hiển thị điểm số, thông tin người chơi
  
- **`settings_screen.py`** - Màn hình cài đặt
  - Class `ManHinhCaiDat` - Form cài đặt game chi tiết
  - Combo boxes cho kích thước, độ khó, theme

### ⚙️ **Quản lý dữ liệu**:
- **`settings_manager.py`** - Quản lý cài đặt
  - Class `QuanLyCaiDat` - Load/save cài đặt từ JSON file
  - Lưu trữ: board size, win condition, AI difficulty, theme
