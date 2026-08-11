from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# База знаний нашего ИИ-тренера для демонстрации
AI_RESPONSES = {
    "приседания": "🤖 ИИ-Тренер: Отличный выбор! При приседаниях держите спину ровной, а пятки не отрывайте от пола. Мой ИИ-модуль рекомендует начать с 3 подходов по 15 раз.",
    "бег": "🤖 ИИ-Тренер: Бег развивает выносливость! Начните с легкой разминки 5 минут, затем 20 минут бега в комфортном темпе. Не забывайте следить за пульсом.",
    "офп": "🤖 ИИ-Тренер: Комплекс ОФП на сегодня: 10 отжиманий, 15 приседаний, 30 секунд планки. Повторите 3 раунда!",
    "привет": "🤖 ИИ-Тренер: Привет, Первый! Я твой цифровой наставник. Спроси меня про 'бег', 'приседания' или 'ОФП', и я составлю тебе план тренировки!",
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

# Новый маршрут для обработки запросов к ИИ
@app.route('/ai-chat', methods=['POST'])
def ai_chat():
    user_message = request.json.get('message', '').lower()
    
    # Поиск подходящего ответа по ключевым словам
    reply = "🤖 ИИ-Тренер: Интересный вопрос! Я постоянно учусь. Попробуй спросить меня про 'бег', 'приседания' или 'ОФП', чтобы получить готовую программу тренировок!"
    for key in AI_RESPONSES:
        if key in user_message:
            reply = AI_RESPONSES[key]
            break
            
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)
