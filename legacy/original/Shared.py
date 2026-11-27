class Shared:
    fnt = 'Verdana 35'
    nme = 'Math trainer'

    # Language dictionaries
    languages = {
        "English": {
            "start": "Start",
            "choose_difficulty": "Choose Difficulty",
            "settings": "Settings",
            "language": "Language",
            "problems_solved": "Problems Solved: ",
            "best_score": "Best score: ",
            "right": "Right: ",
            "wrong": "Wrong: ",
            'easy': 'Easy',
            'normal': 'Normal',
            'hard': 'Hard',
            'time_remaining': 'Time remaining: '
        },
        "Russian": {
            "start": "Начать",
            "choose_difficulty": "Выбрать сложность",
            "settings": "Настройки",
            "language": "Язык",
            "problems_solved": "Решено задач: ",
            "best_score": "Лучший результат: ",
            "right": "Верно: ",
            "wrong": "Неверно: ",
            'easy': 'Легко',
            'normal': 'Нормально',
            'hard': 'Сложно',
            'time_remaining': 'Осталось времени: '
        },
        "Kazakh": {
            "start": "Бастау",
            "choose_difficulty": "Тиімсіздікті таңдау",
            "settings": "Параметрлер",
            "language": "Тіл",
            "problems_solved": "Есептер шешілді: ",
            "best_score": "Үздік нәтиже: ",
            "right": "Дұрыс: ",
            "wrong": "Қате: ",
            'easy': 'Оңай',
            'normal': 'Орташа',
            'hard': 'Қиын',
            'time_remaining': 'Қалған уақыт: '
        }
    }

    # Current language, default to Russian
    current_language = "Russian"
    registered_objects = []

    @classmethod
    def get_text(cls, identifier):
        return cls.languages[cls.current_language].get(identifier, "Unknown")

    @classmethod
    def set_language(cls, language):
        cls.current_language = language
        cls.notify_language_change()

    @classmethod
    def register(cls, obj):
        # Register an object to be notified of changes
        cls.registered_objects.append(obj)

    @classmethod
    def notify_language_change(cls):
        # Notify all registered objects of a language change
        for obj in cls.registered_objects:
            obj.update_texts()
