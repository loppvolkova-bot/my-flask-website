from flask import Flask, render_template, request, jsonify
import re

# Импорты для Data Science и NLP-реализации ИИ
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pymorphy3

app = Flask(__name__)

# Инициализируем лингвистический анализатор для русского языка
morph = pymorphy3.MorphAnalyzer()

# РАСШИРЕННАЯ БАЗА ЗНАНИЙ ИИ ДЛЯ «ИГРЫ ПЕРВЫХ» (Обучающий корпус)
AI_KNOWLEDGE = [
    {
        "intent": "приветствие",
        "patterns": ["привет", "здравствуйте", "добрый день", "приветствую", "ку", "хай", "старт", "начать", "hello"],
        "reply": "🤖 ИИ-Ассистент: Привет, Первый! Рад тебя видеть. Я твой интеллектуальный цифровой гид. Могу рассказать про приложение, задания, Движкоины, мерч, команду проекта или наши соцсети. Что тебя интересует?"
    },
    {
        "intent": "о_приложении",
        "patterns": ["что такое игра первых", "что за приложение", "о проекте", "суть игры", "описание", "зачем это", "программа"],
        "reply": "🤖 ИИ-Ассистент: «Игра Первых» — это интерактивное мобильное приложение, разработанное для вовлечения молодежи в полезные активности. Участники выполняют спортивные, творческие и научные задания, прокачивают навыки, копят игровую валюту и соревнуются в рейтингах."
    },
    {
        "intent": "движкоины",
        "patterns": ["как получить движкоины", "движкоины", "монеты", "валюта", "баллы", "очки", "как заработать", "коины", "деньги"],
        "reply": "🤖 ИИ-Ассистент: Движкоины — это официальная игровая валюта проекта. Заработать их можно за успешное выполнение квестов в приложении, участие во всероссийских акциях, ежедневный вход на платформу и победы в челленджах!"
    },
    {
        "intent": "правила_игры",
        "patterns": ["как играть", "задания", "квесты", "миссии", "что делать", "активности", "челленджи", "правила"],
        "reply": "🤖 ИИ-Ассистент: Играть очень просто: скачай приложение, выбери интересующий трек (спорт, наука, арт), открывай доступные задания и загружай отчеты об их выполнении. За каждое одобренное задание тебе сразу начисляются Движкоины."
    },
    {
        "intent": "мероприятия",
        "patterns": ["какие мероприятия будут", "мероприятия", "события", "календарь", "акции", "конкурсы", "слёты"],
        "reply": "🤖 ИИ-Ассистент: Все актуальные события собраны у нас в разделе «Календарь». Вас ждут масштабные региональные хакатоны, спортивные марафоны, творческие фестивали и, конечно же, этот Всероссийский конкурс по прикладному ИИ!"
    },
    {
        "intent": "соцсети",
        "patterns": ["вконтакте", "соцсети", "паблик", "группа", "где найти", "ссылка", "vk", "вк"],
        "reply": "🤖 ИИ-Ассистент: Официальное сообщество «Движения Первых» во ВКонтакте доступно по ссылке: ://vk.com. Подписывайся, чтобы первым узнавать о релизах, обновлениях приложения и амбассадорах проекта!"
    },
    {
        "intent": "мерч",
        "patterns": ["призы", "мерч", "подарки", "магазин", "маркет", "на что потратить", "купить", "обменять", "одежда"],
        "reply": "🤖 ИИ-Ассистент: Заработанные Движкоины можно потратить в игровом Маркете! Там доступны брендированные худи, футболки, блокноты, стикерпаки «Движения Первых», а также уникальные билеты на закрытые федеральные форумы."
    },
    {
        "intent": "команда",
        "patterns": ["кто создал", "разработчики", "команда", "автор", "кто сделал", "стек", "технологии"],
        "reply": "🤖 ИИ-Ассистент: Данная веб-платформа и интеллектуальный ассистент разработаны специально для конкурса по прикладному применению ИИ. Бэкенд написан на Python/Flask, а ИИ базируется на продвинутых алгоритмах обработки естественного языка NLP (TF-IDF + Лемматизация + Косинусное сходство векторов)."
    }
]

def clean_and_lemmatize(text):
    """
    Инженерная функция предобработки текста (NLP-пайплайн):
    Очищает текст от символов и приводит каждое слово к начальной форме (лемме).
    Пример: 'хочу заработать коинов' -> 'хотеть заработать коин'
    """
    text = re.sub(r'[^а-яа-ёa-z\s]', '', text.lower())
    words = text.split()
    lemmatized_words = [morph.parse(word)[0].normal_form for word in words]
    return " ".join(lemmatized_words)

# НАСТРОЙКА И ОБУЧЕНИЕ NLP-МОДЕЛИ ПРИ СТАРТЕ СЕРВЕРА
corpus = []
reply_mapping = []

for item in AI_KNOWLEDGE:
    # Собираем все ключевые слова темы, очищаем их и лемматизируем
    combined_patterns = " ".join(item["patterns"])
    normalized_patterns = clean_and_lemmatize(combined_patterns)
    corpus.append(normalized_patterns)
    reply_mapping.append(item["reply"])

# Инициализируем векторизатор TF-IDF
vectorizer = TfidfVectorizer()
X_corpus = vectorizer.fit_transform(corpus)


@app.route('/')
def home():
    return render_template('index.html', active_tab='about', role='Участник')

@app.route('/mechanics')
def mechanics():
    return render_template('index.html', active_tab='mechanics', role='Участник')

@app.route('/calendar')
def calendar():
    return render_template('index.html', active_tab='calendar', role='Участник')

@app.route('/news')
def news():
    return render_template('index.html', active_tab='news', role='Участник')

@app.route('/feedback')
def feedback():
    return render_template('index.html', active_tab='feedback', role='Участник')

# ИНТЕЛЛЕКТУАЛЬНЫЙ ЭНДПОИНТ ЧАТА
@app.route('/ai-chat', methods=['POST'])
def ai_chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({"reply": "🤖 ИИ-Ассистент: Напиши что-нибудь, и я обязательно отвечу!"})
    
    # 1. Применяем лемматизацию к входящему запросу пользователя
    normalized_user_message = clean_and_lemmatize(user_message)
    
    # 2. Векторизуем очищенный текст через TF-IDF
    X_user = vectorizer.transform([normalized_user_message])
    
    # 3. Рассчитываем косинусное сходство векторов
    similarity_scores = cosine_similarity(X_user, X_corpus)
    max_score_index = similarity_scores.argmax()
    max_score = similarity_scores[max_score_index]
    
    # Переводим уверенность ИИ в проценты для вывода в консоль / отладки
    confidence_percentage = round(float(max_score) * 100, 1)
    print(f"[AI Debug] Message: '{user_message}' -> Confidence: {confidence_percentage}%")
    
    # Порог уверенности (снижен до 8%, так как после лемматизации совпадения стали точнее)
    if max_score > 0.08:
        reply = reply_mapping[max_score_index]
    else:
        # Интеллектуальная динамическая заглушка
        reply = "🤖 ИИ-Ассистент: Я пока не знаю точного ответа на этот вопрос в рамках демонстрационного прототипа. Попробуй спросить: «Что такое Игра Первых?», «Как получить Движкоины?», «Что можно купить на монеты?» или «Где найти вас в ВК?»."
            
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)
