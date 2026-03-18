import os
from faster_whisper import WhisperModel
from pydub import AudioSegment

# --- CẤU HÌNH ---
INPUT_FILE = r"D:\QVProject\TTS-Voice-Project\Dataset\NNN.wav" 
OUTPUT_DIR = "dataset_output"
AUDIO_SUBDIR = "wavs"
METADATA_FILE = "metadata.csv"

# CHỈNH Ở ĐÂY: 
# Nếu có card NVIDIA, hãy đổi thành "cuda". Nếu không để "cpu"
# Dùng "medium" để cân bằng giữa tốc độ và độ chính xác
DEVICE = "cpu" 
MODEL_SIZE = "medium" 

if not os.path.exists(os.path.join(OUTPUT_DIR, AUDIO_SUBDIR)):
    os.makedirs(os.path.join(OUTPUT_DIR, AUDIO_SUBDIR))

def process_audio():
    print(f"🚀 Đang tải mô hình Whisper ({MODEL_SIZE})...")
    model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type="int8")

    print(f"⌛ Đang phân tích file (50 phút có thể mất 15-30 phút trên CPU)...")
    # Thêm vad_filter để tự động bỏ qua các đoạn im lặng dài
    segments, info = model.transcribe(INPUT_FILE, beam_size=5, language="vi", vad_filter=True)

    print("🔈 Đang load audio vào bộ nhớ...")
    audio = AudioSegment.from_wav(INPUT_FILE)
    
    metadata = []
    count = 1

    print("✂️ Bắt đầu cắt và lưu file...")
    for segment in segments:
        start_ms = segment.start * 1000
        end_ms = segment.end * 1000
        duration = segment.end - segment.start

        if 2.0 <= duration <= 15.0:
            text = segment.text.strip()
            if not text: continue
            
            filename = f"segment_{count:04d}.wav"
            filepath = os.path.join(OUTPUT_DIR, AUDIO_SUBDIR, filename)

            extract = audio[start_ms:end_ms]
            # Ép kiểu về 24000Hz, Mono (chuẩn cho VieNeu-TTS)
            extract = extract.set_frame_rate(24000).set_channels(1)
            extract.export(filepath, format="wav")

            metadata.append(f"{filename}|{text}")
            
            # In tiến độ mỗi 10 đoạn để tránh trôi màn hình
            if count % 10 == 0:
                print(f"Đã xử lý xong {count} đoạn... (Thời gian hiện tại: {segment.end/60:.2f} phút)")
            count += 1

    with open(os.path.join(OUTPUT_DIR, METADATA_FILE), "w", encoding="utf-8") as f:
        for line in metadata:
            f.write(line + "\n")

    print(f"✅ Xong! Tổng cộng {len(metadata)} file đã được tạo tại {OUTPUT_DIR}")

if __name__ == "__main__":
    process_audio()