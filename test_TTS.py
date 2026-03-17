import os
from vieneu import Vieneu

# 1. Khởi tạo mô hình
# Mặc định tts = Vieneu() sẽ tự động tải model 0.3B-Q4 GGUF siêu nhẹ và chạy trên CPU
print("Đang tải mô hình VieNeu-TTS...")
tts = Vieneu()

# Tạo thư mục chứa file âm thanh đầu ra
os.makedirs("thong_bao", exist_ok=True)

# 2. Danh sách các kịch bản phát thông báo
danh_sach_thong_bao =[
    "Alo alo, xin thông báo: Đã đến giờ nghỉ trưa, mời toàn thể nhân viên xuống nhà ăn để dùng bữa.",
    "Kính chào quý khách. Hiện tại quầy thu ngân số 3 đang trống, xin mời quý khách di chuyển sang quầy số 3 để thanh toán.",
    "Chú ý! Vui lòng không đỗ xe trước cổng ra vào của công ty. Xin cảm ơn."
]


print("\n--- BẮT ĐẦU TẠO THÔNG BÁO ---")
for i, van_ban in enumerate(danh_sach_thong_bao):
    output_path = f"thong_bao/thong_bao_{i+1}.wav"
    print(f"Đang xử lý thông báo {i+1}...")
    
    # BƯỚC QUAN TRỌNG: Dùng hàm infer() để tạo giọng nói
    audio = tts.infer(text=van_ban)
    
    # Dùng hàm save() để lưu mảng audio thành file .wav
    tts.save(audio, output_path)
    
    print(f" -> Đã lưu thành công: {output_path}")

print("\nHoàn tất! Hãy kiểm tra thư mục 'thong_bao'.")