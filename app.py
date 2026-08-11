from flask import Flask, render_template, request

app = Flask(__name__)

# Главная страница (Идея проекта)
@app.route('/')
def home():
    role = request.args.get('role', 'Участник')
    return render_template('index.html', active_tab='about', role=role)

# Страница: Механика игры
@app.route('/mechanics')
def mechanics():
    role = request.args.get('role', 'Участник')
    return render_template('index.html', active_tab='mechanics', role=role)

# Страница: Календарь
@app.route('/calendar')
def calendar():
    role = request.args.get('role', 'Участник')
    return render_template('index.html', active_tab='calendar', role=role)

# Страница: Новости
@app.route('/news')
def news():
    role = request.args.get('role', 'Участник')
    return render_template('index.html', active_tab='news', role=role)

# Страница: Обратная связь
@app.route('/feedback')
def feedback():
    role = request.args.get('role', 'Участник')
    return render_template('index.html', active_tab='feedback', role=role)

if __name__ == '__main__':
    app.run(debug=True)
