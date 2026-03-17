from pydub import AudioSegment
import math
import os

def cut_audio(file_path, output_folder="dataset", duration_ms=10000):
    # 1. Tạo folder nếu chưa tồn tại
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Đã tạo thư mục: {output_folder}")
    
    # 2. Load file âm thanh
    audio = AudioSegment.from_wav(file_path)
    
    # 3. Tính toán và cắt
    total_length = len(audio)
    num_segments = math.ceil(total_length / duration_ms)
    
    for i in range(num_segments):
        start = i * duration_ms
        end = (i + 1) * duration_ms
        segment = audio[start:end]
        
        # 4. Xuất file vào folder đã tạo
        file_name = os.path.join(output_folder, f"segment_{i}.wav")
        segment.export(file_name, format="wav")
        print(f"Đã lưu: {file_name}")

# --- CÁCH CHÈN FILE CỦA BẠN ---
# Bạn hãy để file .wav cần cắt vào cùng thư mục với file code .py này
# Sau đó thay tên file vào chỗ này:
TEN_FILE_GOC = "NNN.wav" 

if os.path.exists(TEN_FILE_GOC):
    cut_audio(TEN_FILE_GOC, output_folder="dataset", duration_ms=10000)
else:
    print(f"Lỗi: Không tìm thấy file '{TEN_FILE_GOC}'. Bạn nhớ copy file vào cùng thư mục với script này nhé!")