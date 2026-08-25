import os
from dotenv import load_dotenv 
from flask import Flask, render_template, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI
app = Flask(__name__)
AI_KNOWLEDGE = [
    {
        "patterns": ["привет", "здравствуйте", "добрый день", "приветствую"],
        "reply": "🤖 Ассистент: Привет! Рад тебя видеть. Могу рассказать про приложение, задания, Движкоины, мерч и призы."
    },
    {
        "patterns": ["что такое игра первых", "о проекте", "суть игры"],
        "reply": "🤖 Игра Первых — мобильное приложение, где участники выполняют квесты, зарабатывают игровую валюту и соревнуются за призы."
    },
    {
        "patterns": ["движкоины", "как получить движкоины"],
        "reply": "🤖 Движкоины — игровая валюта. Заработай их за выполнение заданий!"
    },]
def build_system_prompt():
    """Формирует системный промт на основе базы знаний."""
    knowledge_text = "\n".join([item["reply"] for item in AI_KNOWLEDGE])
    return f"""
Ты — ИИ‑ассистент мобильного приложения «Игра Первых». Отвечай коротко и дружелюбно 🤖💜.
Используй только факты ниже. Не придумывай лишнего.
Факты о проекте:
{knowledge_text}
""".strip()
SYSTEM_PROMPT = build_system_prompt() 
load_dotenv()
YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
if not YANDEX_API_KEY:
    raise ValueError("API key is missing!")
client = OpenAI(
    api_key=YANDEX_API_KEY,
    base_url="https://llm.api.cloud.yandex.net/foundation-models/v1")
@app.route('/ai-chat', methods=['POST'])
def ai_chat():
    """
    Основной эндпоинт чата.
    Принимает JSON {"message": "<текст>"} и возвращает ответ от нейросети.
    """
    data = request.get_json(silent=True) or {}
    user_message = data.get('message', '').lower().strip()

    if not user_message:
        return jsonify({"reply": "🤖 Напиши что-нибудь!"})

    try:
        response = client.chat.completions.create(
            model="yandexgpt/latest",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}],
            temperature=0.7,
            max_tokens=200)
        
        answer_text = response.choices[0].message.content.strip()
        return jsonify({"reply": answer_text})
    except Exception as e:
        print(f"Ошибка вызова API: {e}")
        return jsonify({"reply": "🤖 Произошла ошибка связи с интеллектом."}), 500
@app.route('/')
def home():
    return render_template('index.html')
@app.errorhandler(500)
def internal_error(error):
    """Обработчик внутренних ошибок Flask."""
    app.logger.exception(error)
    return jsonify({"error": "Произошла внутренняя ошибка. Попробуйте позже."}), 500
if __name__ == '__main__':
    app.run(debug=True)
