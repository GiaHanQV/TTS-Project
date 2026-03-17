import os
import torch
from streamlit import audio
from vieneu import Vieneu
from transformers import AutoTokenizer, AutoModelForCausalLM



device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Đang sử dụng thiết bị: {device.upper()}")

# print("Đang tải mô hình tóm tắt Qwen 0.5B (Chỉ tải lần đầu mất khoảng 1GB)...")
# model_id = "Qwen/Qwen2.5-0.5B-Instruct"
model_id = "Qwen/Qwen2.5-1.5B-Instruct"

# Sử dụng AutoTokenizer và CausalLM chuẩn mới nhất, không lo lỗi version
tokenizer = AutoTokenizer.from_pretrained(model_id)
llm_model = AutoModelForCausalLM.from_pretrained(
    model_id, 
    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    device_map="auto"
)

def tom_tat_offline(noi_dung_email):
    # Tạo câu lệnh (Prompt) yêu cầu AI tóm tắt
    messages =[
        {"role": "system", "content": "Bạn là chuyên gia tóm tắt email. Hãy trích xuất thông tin quan trọng nhất (thời gian, địa điểm, hành động bắt buộc). Viết 1-2 câu ngắn gọn, không bịa đặt thông tin. Chỉ trả về kết quả tóm tắt, không giải thích thêm."},
        {"role": "user", "content": f"Email nội dung như sau:\n{noi_dung_email}\n\nHãy tóm tắt:"}
    ]
    
    # Mã hóa văn bản
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    model_inputs = tokenizer([text], return_tensors="pt").to(llm_model.device)

    # Sinh văn bản tóm tắt
    with torch.no_grad():
        generated_ids = llm_model.generate(
            **model_inputs,
            max_new_tokens=100,
            temperature=0.1,    # Càng thấp (gần 0) thì AI càng tập trung vào sự thật, ít sáng tạo sai lệch
            do_sample=True,
            top_p=0.9
        )
    
    # Cắt bỏ phần câu hỏi, chỉ lấy phần câu trả lời của AI
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]
    
    tom_tat = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return tom_tat.strip()

print("Đang tải mô hình VieNeu-TTS...")
tts = Vieneu()
os.makedirs("thong_bao_email", exist_ok=True)


email_moi = {
    "sender": "Phòng Hành chính <admin@congty.com>",
    "subject": "Thông báo cắt điện cuối tuần",
    "body": """
        Kính gửi các phòng ban,
        Ban Quản lý tòa nhà vừa thông báo sẽ tiến hành bảo trì hệ thống điện toàn bộ tòa nhà vào cuối tuần này. 
        Cụ thể, thời gian cắt điện sẽ bắt đầu từ 8h00 sáng Thứ Bảy (ngày 18) và dự kiến có điện trở lại vào lúc 17h00 chiều Chủ Nhật (ngày 19). 
        Trong thời gian này, thang máy và hệ thống điều hòa sẽ ngừng hoạt động. Yêu cầu toàn bộ nhân viên lưu lại dữ liệu, tắt máy tính và các thiết bị điện tại bàn làm việc trước khi ra về vào chiều thứ Sáu để tránh chập cháy. Hệ thống server nội bộ công ty vẫn sẽ chạy bằng máy phát điện dự phòng.
        Trân trọng,
        Phòng Hành chính
    """
}

print("\n--- BẮT ĐẦU XỬ LÝ EMAIL (100% OFFLINE) ---")
print("AI đang đọc và tóm tắt nội dung (vui lòng đợi vài giây nếu dùng CPU)...")

noi_dung_tom_tat = tom_tat_offline(email_moi["body"])

nguoi_gui = email_moi['sender'].split('<')[0].strip()
kich_ban_doc = f"Thông báo từ {nguoi_gui}. Tiêu đề: {email_moi['subject']}. Tóm tắt: {noi_dung_tom_tat}"

print(f"\n=> Kịch bản AI sẽ đọc:\n{kich_ban_doc}\n")

print("Đang tạo file âm thanh giọng nói...")
audio = tts.infer(
    text=kich_ban_doc,
    ref_audio="VTV_Voice.wav", 
    ref_text="thưa quý vị, chỉ còn ba ngày nữa ngày mười lăm tháng ba năm hai nghìn không trăm hai mươi sáu cử tri cả nước nô nức đi bầu" 
)

output_path = "thong_bao_email/email_voice_VTV.wav"
tts.save(audio, output_path)
print(f"-> HOÀN TẤT! Đã lưu file tại: {output_path}")