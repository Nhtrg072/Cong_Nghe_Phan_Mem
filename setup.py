# Script build exe tối giản - cài thẳng vào thư mục hiện tại
import os
import subprocess
import sys
import shutil
from PIL import Image

def build_game():
    """Build game exe đơn giản"""
    print("🎮 BUILD CARO GAME")
    print("=" * 30)
    
    # Kiểm tra và cài đặt dependencies
    dependencies = ["pyinstaller", "pillow"]
    for dep in dependencies:
        try:
            if dep == "pyinstaller":
                import PyInstaller
            elif dep == "pillow":
                import PIL
            print(f"✅ {dep} OK")
        except ImportError:
            print(f"⚙️ Cài {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✅ {dep} đã cài")
    
    # Chuyển đổi icon.jpg thành icon.ico
    icon_path = os.path.abspath("icon.jpg")
    print(f"🔍 Tìm kiếm icon tại: {icon_path}")
    
    if os.path.exists(icon_path):
        print("🖼️ Chuyển đổi icon...")
        try:
            from PIL import Image
            img = Image.open(icon_path)
            # Resize về kích thước chuẩn cho icon
            img = img.resize((256, 256), Image.Resampling.LANCZOS)
            img.save("icon.ico", format="ICO")
            print("✅ Icon đã sẵn sàng")
        except Exception as e:
            print(f"⚠️ Lỗi chuyển đổi icon: {e}")
            print("⚠️ Sẽ build không có icon")
    else:
        print("⚠️ Không tìm thấy icon.jpg")
    
    # Xóa exe cũ nếu có
    if os.path.exists("CaroGame.exe"):
        os.remove("CaroGame.exe")
        print("🗑️ Đã xóa game cũ")
    
    # Build exe
    print("🔨 Building...")
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed", 
        "--name=CaroGame",
        "--distpath=.",  # Cài thẳng vào thư mục hiện tại
        "--clean"
    ]
    
    # Thêm icon nếu có
    if os.path.exists("icon.ico"):
        cmd.extend(["--icon=icon.ico"])
        print("🖼️ Sử dụng icon tùy chỉnh")
    
    cmd.append("main.py")
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print("✅ Build thành công!")
        
        # Dọn dẹp
        if os.path.exists("build"):
            shutil.rmtree("build")
        if os.path.exists("CaroGame.spec"):
            os.remove("CaroGame.spec")
        # Giữ lại icon.ico để tái sử dụng
        print("🧹 Đã dọn dẹp")
        
        print(f"🚀 Game sẵn sàng: {os.path.abspath('CaroGame.exe')}")
        
    except subprocess.CalledProcessError:
        print("❌ Build thất bại")

if __name__ == "__main__":
    build_game()
