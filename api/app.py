from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
import os
import google.generativeai as genai
import markdown
import html

load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 4000,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

def markdown_to_html(markdown_text):
    return markdown.markdown(markdown_text)

app = Flask(__name__, static_folder="../public", static_url_path="/")

@app.route('/')
def serve_index():
    return send_from_directory('../public', 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_input = data.get('input', '')

        if not user_input:
            return jsonify({'output': "Hmm, looks like you didn't write anything. Try typing something!"})

        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(user_input)
        formatted_response = response.text
        formatted_response = html.unescape(formatted_response)
        formatted_response = html.escape(formatted_response)
        formatted_response = markdown_to_html(formatted_response)

        return jsonify({'output': formatted_response})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'output': f"Sorry, an error occurred. {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)