import requests
import json
import os

# --- CẤU HÌNH API CỦA GPT-SoVITS ---
# Đảm bảo bạn đã bật file 'api.py' hoặc 'go-api.bat' trong thư mục GPT-SoVITS
API_URL = "http://127.0.0.1:9880/tts" 

# File âm thanh mẫu ngắn (khoảng 5-10s) TRÍCH TỪ CHÍNH DATA BẠN ĐÃ TRAIN
# Nó dùng file này làm "gợi ý cảm xúc" để biết nên nhấn nhá thế nào cho đoạn text sắp đọc
REFER_WAV_PATH = "D:/Data_Giong/cau_mau_ngan.wav"
# Nội dung của cái file âm thanh mẫu ở trên
PROMPT_TEXT = "Xin chào, hôm nay tôi sẽ hướng dẫn các bạn cách làm việc." 
PROMPT_LANGUAGE = "vi" # Ngôn ngữ của file mẫu

def doc_email_bang_gpt_sovits(email_text, output_file="email_output.wav"):
    """
    Gửi nội dung Email đến server GPT-SoVITS đã được Train giọng của bạn 
    để tổng hợp thành file âm thanh với đầy đủ nhấn nhá.
    """
    print("Đang gửi Email cho AI (GPT-SoVITS) xử lý...")
    
    # Chuẩn bị dữ liệu gửi đi
    payload = {
        "refer_wav_path": REFER_WAV_PATH,
        "prompt_text": PROMPT_TEXT,
        "prompt_language": PROMPT_LANGUAGE,
        "text": email_text,       # Nội dung Email cần đọc
        "text_language": "vi",    # Ngôn ngữ của Email
        "cut_punc": ".,;?!"       # Tự động ngắt câu theo dấu câu để thở tự nhiên
    }

    try:
        # Gọi API
        response = requests.post(API_URL, json=payload)
        
        # Nếu thành công, lưu file Audio trả về
        if response.status_code == 200:
            with open(output_file, "wb") as f:
                f.write(response.content)
            print(f"🎉 Hoàn thành! Đã lưu giọng đọc Email tại: {output_file}")
            
            # (Tùy chọn) Tự động mở file nghe luôn trên Windows
            os.system(f"start {output_file}")
        else:
            print(f"Lỗi từ Server: {response.text}")
            
    except Exception as e:
        print(f"Không thể kết nối đến GPT-SoVITS API. Lỗi: {e}")
        print("Vui lòng kiểm tra xem bạn đã bật API Server của GPT-SoVITS chưa!")

if __name__ == "__main__":
    # Ví dụ bạn dùng thư viện imaplib lấy được nội dung email này:
    noi_dung_email = """
    Chào anh, dự án của chúng ta đã hoàn thành xuất sắc trong quý này. 
    Khách hàng rất hài lòng và muốn ký thêm hợp đồng mới vào tuần sau.
    Anh sắp xếp thời gian để chúng ta cùng họp nhé!
    """
    
    doc_email_bang_gpt_sovits(noi_dung_email)