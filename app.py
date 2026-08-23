import ollama
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ... ваш массив AI_KNOWLEDGE остается здесь для справки ...
AI_KNOWLEDGE = [
    # ... ваши данные из массива ...
]

# Формируем системный промпт на основе вашей базы знаний
def build_system_prompt():
    knowledge_text = "\n".join([f"- {item['reply']}" for item in AI_KNOWLEDGE])
    return f"""Ты — ИИ-ассистент интерактивного мобильного приложения «Игра Первых». Твоя задача — помогать молодежи разбираться в проекте.
Соблюдай следующие правила:
1. Отвечай коротко, энергично и дружелюбно. Используй эмодзи 🤖💜🪙🏆.
2. Говори только о том, что написано ниже. Не придумывай лишнего.
3. Если вопрос не касается проекта, вежливо верни пользователя к теме.

Факты о проекте:
{knowledge_text}
"""

SYSTEM_PROMPT = build_system_prompt()

from openai import OpenAI

# Загружаем секрет из переменных окружения
load_dotenv()
YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
if not YANDEX_API_KEY:
    raise ValueError("API key is missing!")

client = OpenAI(
    api_key=YANDEX_API_KEY,
    base_url="https://llm.api.cloud.yandex.net/foundation-models/v1"
)

@app.route('/ai-chat', methods=['POST'])
def ai_chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get('message', '').strip().lower()
    
    if not user_message:
        return jsonify({"reply": "🤖 Ассистент: Напиши что-нибудь!"})

    # Формируем системный промт на основе вашей базы знаний AI_KNOWLEDGE
    system_prompt = "Ты — ИИ‑ассистент «Игры Первых». Отвечай кратко и дружелюбно.\n"
    for item in AI_KNOWLEDGE:
        patterns_str = ", ".join(item["patterns"])
        reply = item["reply"].replace("\n", " ").strip()[:40]  # Берём начало ответа
        system_prompt += f"- Если вопрос похож на '{patterns_str}', ответь примерно так: {reply}\n"

    try:
        response = client.chat.completions.create(
            model="yandexgpt/latest",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        answer_text = response.choices[0].message.content.strip()
        return jsonify({"reply": answer_text})

    except Exception as e:
        print(f"Ошибка вызова API: {e}")
        return jsonify({"reply": "🤖 Произошла ошибка связи с интеллектом."}), 500
def ai_chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({"reply": "🤖 Напиши что-нибудь, и я обязательно отвечу!"})

    try:
        # Вызов локальной модели Ollama
        response = ollama.chat(
            model='gemma:2b',
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            stream=False  # Для начала лучше использовать False, чтобы убедиться в работоспособности
        )
        
        reply = response['message']['content']
        
        return jsonify({"reply": reply})

    except Exception as e:
        # В случае падения Ollama возвращаем понятную ошибку
        print(f"Ошибка LLM: {e}")
        return jsonify({"reply": "🤖 Мой мозг сейчас перезагружается. Попробуй еще раз через пару секунд!"})

if __name__ == '__main__':
    app.run(debug=True)
