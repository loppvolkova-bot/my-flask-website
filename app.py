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

@app.route('/ai-chat', methods=['POST'])
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
