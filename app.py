from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# База знаний нашего ИИ-тренера
AI_RESPONSES = {
    "приседания": "🤖 ИИ-Тренер: Отличный выбор! При приседаниях держите спину ровной. Мой ИИ-модуль рекомендует начать с 3 подходов по 15 раз.",
    "бег": "🤖 ИИ-Тренер: Бег развивает выносливость! Начните с легкой разминки 5 минут, затем 20 минут бега в комфортном темпе.",
    "офп": "🤖 ИИ-Тренер: Комплекс ОФП на сегодня: 10 отжиманий, 15 приседаний, 30 секунд планки. Повторите 3 раунда!",
    "привет": "🤖 ИИ-Тренер: Привет, Первый! Спроси меня про 'бег', 'приседания' или 'ОФП', и я составлю тебе план тренировки!",
}

@app.route('/')
def home():
    role = request.args.get('role', 'Участник')
    return render_template('index.html', active_tab='about', role=role)

@app.route('/mechanics')
def mechanics():
    role = request.args.get('role', 'Участник')
    return render_template('index.html', active_tab='mechanics', role=role)

@app.route('/calendar')
def calendar():
    role = request.args.get('role', 'Участник')
    return render_template('index.html', active_tab='calendar', role=role)

@app.route('/news')
def news():
    role = request.args.get('role', 'Участник')
    return render_template('index.html', active_tab='news', role=role)

@app.route('/feedback')
def feedback():
    role = request.args.get('role', 'Участник')
    return render_template('index.html', active_tab='feedback', role=role)

@app.route('/ai-chat', methods=['POST'])
def ai_chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get('message', '').lower()
    
    reply = "🤖 ИИ-Тренер: Интересный вопрос! Попробуй спросить меня про 'бег', 'приседания' или 'ОФП'."
    for key in AI_RESPONSES:
        if key in user_message:
            reply = AI_RESPONSES[key]
            break
            
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)
