import os

def get_dir_size(path=r"D:\GiaHan\TTS-Project\VieNeu-TTS\my_voice_final"):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size / (1024 * 1024) # Đổi sang MB

size = get_dir_size()
print(f"📦 Tổng dung lượng mô hình: {size:.2f} MB")