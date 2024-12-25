from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 4000,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

chat_session = model.start_chat(   
    history=[]
)

print("Ambathron: Halo! Aku Ambathron, AI-mu yang serba bisa. Sebelum kita mulai, boleh tahu dong siapa namamu?\n")
user_name = input("User: ").strip()
print(f"Ambathron: Senang bertemu denganmu, {user_name}! Ketik 'exit' untuk udahan ngobrol denganmu.\n")

while True:
    user_input = input(f"{user_name}: ").strip()

    if user_input.lower() == "exit":
        print(f"Ambathron: Sampai jumpa, {user_name}! Semoga harimu menyenangkan!\n")
        break

    if not user_input:
        print(f"Ambathron: Hmm, sepertinya kamu tidak menulis apa-apa. Coba ketik sesuatu, {user_name}!\n")
        continue

    response = chat_session.send_message(user_input)
    print(f"Ambathron: {response.text}\n")
