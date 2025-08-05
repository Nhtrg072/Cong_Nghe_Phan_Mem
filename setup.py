# Script build exe tối giản - cài thẳng vào thư mục hiện tại
import os
import subprocess
import sys
import shutil

def build_game():
    """Build game exe đơn giản"""
    print("🎮 BUILD CARO GAME")
    print("=" * 30)
    
    # Kiểm tra PyInstaller
    try:
        import PyInstaller
        print("✅ PyInstaller OK")
    except ImportError:
        print("⚙️ Cài PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller đã cài")
    
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
        "--clean",
        "main.py"
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print("✅ Build thành công!")
        
        # Dọn dẹp
        if os.path.exists("build"):
            shutil.rmtree("build")
        if os.path.exists("CaroGame.spec"):
            os.remove("CaroGame.spec")
        print("🧹 Đã dọn dẹp")
        
        print(f"🚀 Game sẵn sàng: {os.path.abspath('CaroGame.exe')}")
        
    except subprocess.CalledProcessError:
        print("❌ Build thất bại")

if __name__ == "__main__":
    build_game()
