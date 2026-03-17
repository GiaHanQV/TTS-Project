import google.generativeai as genai

# Thay bằng API Key của bạn
API_KEY = "AIzaSyAv_2JMErdxLQCfOuYjxnIwc9zo0rVxvoM"
genai.configure(api_key=API_KEY)

print("Các mô hình bạn có thể sử dụng hiện tại là:")
for m in genai.list_models():
    # Chỉ lọc các mô hình hỗ trợ tạo văn bản (generateContent)
    if 'generateContent' in m.supported_generation_methods:
        print(f"- {m.name}")