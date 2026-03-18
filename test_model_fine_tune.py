import os
import torch
import numpy as np
import re
from vieneu import Vieneu

# --- THIẾT LẬP THIẾT BỊ ---
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🚀 Đang sử dụng thiết bị: {device.upper()}")

# --- ĐƯỜNG DẪN MÔ HÌNH ---
custom_model_path = r"D:\GiaHan\TTS-Project\VieNeu-TTS\my_voice_final"

print("⌛ Đang tải mô hình VieNeu-TTS (Giọng của tôi)...")
try:
    # Khởi tạo mô hình và ép chạy trên GPU
    tts = Vieneu(custom_model_path)
except Exception as e:
    print(f"❌ Lỗi: Không thể tải mô hình. Hãy kiểm tra đường dẫn hoặc lệnh Merge. Chi tiết: {e}")
    exit()

# --- THÔNG TIN GIỌNG MẪU (REF AUDIO) ---
# Chọn 1 đoạn audio ngắn (3-10s) trong bộ dữ liệu của bạn để AI lấy tông giọng
REF_AUDIO_PATH = r"D:\GiaHan\TTS-Project\VieNeu-TTS\finetune\dataset\raw_audio\segment_0009.wav"
REF_TEXT = "Tôi biết, dù thân xác này đã định cư ở nơi văn minh, tâm hồn tôi vẫn lưu lạc trong một làng nhỏ bên bờ sông Hậu."

# --- DỮ LIỆU EMAIL ---
email_moi = {
    "sender": "Phòng Hành chính",
    "subject": "Thông báo cắt điện cuối tuần",
    "body": """
        Kính gửi các phòng ban. 
        Ban Quản lý tòa nhà vừa thông báo sẽ tiến hành bảo trì hệ thống điện toàn bộ tòa nhà vào cuối tuần này. 
        Cụ thể, thời gian cắt điện sẽ bắt đầu từ tám giờ sáng Thứ Bảy và dự kiến có điện trở lại vào lúc mười bảy giờ chiều Chủ Nhật. 
        Trong thời gian này, thang máy và hệ thống điều hòa sẽ ngừng hoạt động. 
        Yêu cầu toàn bộ nhân viên lưu lại dữ liệu và tắt máy tính trước khi ra về. 
        Trân trọng.
    """
}

# Chuẩn bị kịch bản đọc
nguoi_gui = email_moi['sender']
kich_ban_doc = f"Thông báo từ {nguoi_gui}. Tiêu đề: {email_moi['subject']}. Nội dung như sau: {email_moi['body']}"

# --- HÀM XỬ LÝ ĐỌC CÂU DÀI (CHUNKING) ---
def synthesize_long_text(text, ref_audio, ref_text):
    # Bước 1: Chia nhỏ văn bản theo dấu chấm, dấu chấm hỏi, dấu chấm than hoặc dấu xuống dòng
    # re.split giúp cắt văn bản một cách thông minh
    sentences = re.split(r'(?<=[.!?]) +|\n+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 2]
    
    all_audio_segments = []
    
    print(f"🎤 Bắt đầu sinh giọng nói cho {len(sentences)} câu...")
    
    for i, sentence in enumerate(sentences):
        print(f"   [+] Đang đọc câu {i+1}/{len(sentences)}: {sentence[:40]}...")
        
        # Sinh âm thanh cho từng câu ngắn
        # AI sẽ luôn giữ được sự ổn định vì mỗi câu là một lần "reset" lại sự chú ý
        audio_chunk = tts.infer(
            text=sentence,
            ref_audio=ref_audio,
            ref_text=ref_text
        )
        
        # Thêm một đoạn im lặng ngắn (0.3 giây) giữa các câu để nghe tự nhiên hơn
        # Thư viện Vieneu thường trả về numpy array, nếu là tensor thì dùng .cpu().numpy()
        if torch.is_tensor(audio_chunk):
            audio_chunk = audio_chunk.cpu().numpy()
            
        all_audio_segments.append(audio_chunk)
        
        # Tạo khoảng lặng 0.3s (với sample rate 24000)
        silence = np.zeros(int(24000 * 0.3))
        all_audio_segments.append(silence)

    # Ghép tất cả các đoạn audio lại thành một
    return np.concatenate(all_audio_segments)

# --- CHẠY CHƯƠNG TRÌNH ---
print("\n--- BẮT ĐẦU XỬ LÝ EMAIL ---")
os.makedirs("thong_bao_email", exist_ok=True)

final_audio = synthesize_long_text(kich_ban_doc, REF_AUDIO_PATH, REF_TEXT)

output_path = "thong_bao_email/email_hoan_hao_MY_VOICE.wav"
tts.save(final_audio, output_path)

print(f"\n✅ THÀNH CÔNG! File audio đã được lưu tại: {output_path}")
print(f"💡 Mẹo: Nếu thấy AI đọc số bị sai, hãy đổi '8h' thành 'tám giờ' trong văn bản.")