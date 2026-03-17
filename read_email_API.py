import os
# import google.generativeai as genai
from streamlit import audio
from vieneu import Vieneu

# GEMINI_API_KEY = "AIzaSyAv_2JMErdxLQCfOuYjxnIwc9zo0rVxvoM"
# genai.configure(api_key=GEMINI_API_KEY)
# llm_model = genai.GenerativeModel('models/gemini-2.0-flash')

print("Đang tải mô hình VieNeu-TTS...")
tts = Vieneu()
os.makedirs("thong_bao_email", exist_ok=True)

# Lấy danh sách giọng có sẵn
available_voices = tts.list_preset_voices()
print("\n--- DANH SÁCH GIỌNG ĐỌC CÓ SẴN ---")
for desc, voice_id in available_voices:
    print(f"- {desc} (Mã ID: {voice_id})")
giong_doc_truyen_cam = tts.get_preset_voice("Doan") 

# def tom_tat_bang_ai(noi_dung_email):
#     prompt = f"""
#     Tóm tắt email sau thành 2 câu ngắn gọn tiếng Việt. 
#     Yêu cầu: Không dùng ký tự đặc biệt, văn phong thân thiện, tự nhiên để máy đọc cho người dùng nghe.
#     Nội dung: {noi_dung_email}
#     """
#     try:
#         response = llm_model.generate_content(prompt)
#         tom_tat = response.text.strip().replace("*", "")
#         return tom_tat
#     except Exception as e:
#         print(f"Lỗi API: {e}")
#         return noi_dung_email[:150] + " và một số nội dung khác."

email_moi = {
    "sender": "Sếp Tổng <director@congty.com>",
    "subject": "Thưởng nóng dự án",
    "body": "Chào mọi người, dự án tháng này đạt doanh thu tốt. Công ty quyết định thưởng nóng mỗi người 2 triệu. Chiều nay kế toán sẽ chuyển khoản nhé. Cảm ơn sự cố gắng của anh em."
}

print("\n--- BẮT ĐẦU XỬ LÝ EMAIL ---")
# noi_dung_tom_tat = tom_tat_bang_ai(email_moi["body"])
# kich_ban_doc = f"Bạn có thư từ {email_moi['sender'].split('<')[0]}. Tiêu đề: {email_moi['subject']}. Nội dung tóm tắt: {noi_dung_tom_tat}"
kich_ban_doc = f"Bạn có thư từ {email_moi['sender'].split('<')[0]}. Tiêu đề: {email_moi['subject']}. Nội dung: {email_moi['body']}"

print(f"\nNội dung AI sẽ đọc: {kich_ban_doc}\n")
print("Đang tạo file âm thanh...")

#audio = tts.infer(text=kich_ban_doc, voice=giong_doc_truyen_cam)

audio = tts.infer(
    text=kich_ban_doc,
    ref_audio="VTV_Voice.wav", 
    ref_text="thưa quý vị, chỉ còn ba ngày nữa ngày mười lăm tháng ba năm hai nghìn không trăm hai mươi sáu cử tri cả nước nô nức đi bầu" 
)


output_path = "thong_bao_email/email_truyen_cam_Full.wav"
tts.save(audio, output_path)
print(f"-> HOÀN TẤT! Đã lưu file tại: {output_path}")