"""Accessible Tkinter interface for the Mental Math Trainer."""

import time
import tkinter as tk
from tkinter import ttk

from .audio import AudioManager
from .core import CURRICULUM, make_formula_question, make_question, make_topic_question, tutorial_questions
from .storage import load_settings, load_stats, record_session, save_curriculum, save_settings


COLORS = {
    "background": "#f3f6fb",
    "surface": "#ffffff",
    "ink": "#17243b",
    "muted": "#69778d",
    "line": "#dfe6f0",
    "accent": "#4169e1",
    "accent_hover": "#3158cb",
    "success": "#18794e",
    "success_bg": "#e8f5ee",
    "error": "#b5473c",
    "error_bg": "#fff0ed",
}


TEXT = {
    "English": {
        "app_name": "Mental Math Trainer", "brand_note": "IT STEP ACADEMY · PERSONAL PROJECT",
        "practice": "Practice", "guide": "FSU guide", "settings": "Settings", "language": "Language",
        "eyebrow": "THINK CLEAR. CALCULATE CALMLY.", "headline": "A sharper mind, one problem at a time.",
        "home_copy": "Build speed and confidence with short mental arithmetic sessions. Your progress stays on this device.",
        "quick_start": "Quick practice", "choose_level": "Choose a level", "start_practice": "Start practice",
        "easy": "Easy", "normal": "Normal", "hard": "Hard", "easy_desc": "Add and subtract up to 20 · 60 seconds",
        "normal_desc": "Four operations · 45 seconds", "hard_desc": "Larger numbers · untimed focus",
        "personal_record": "Personal records", "best_score": "Best score", "no_record": "Play a round to set a record.",
        "games_played": "Sessions played", "correct_total": "Correct answers", "tutorial_title": "Start with the basics",
        "tutorial_copy": "A calm, guided lesson with small numbers and a hint for every step.", "open_tutorial": "Begin tutorial",
        "fsu_card_title": "FSU formula practice", "fsu_card_copy": "Practice the three core abbreviated multiplication identities with quick multiple-choice rounds.", "start_fsu": "Practice FSU formulas",
        "guide_card_title": "Learn a few shortcuts", "guide_card_copy": "See how the trainer works and review mental math strategies.",
        "open_guide": "Read the FSU guide", "footer": "A small daily practice makes a lasting difference.",
        "session": "PRACTICE SESSION", "practice_title": "Stay with the next step.", "timed": "TIME LEFT",
        "untimed": "UNTIMED FOCUS", "score": "SCORE", "correct": "Correct", "mistakes": "Mistakes",
        "finish": "Finish session", "answer_placeholder": "Type your answer", "submit": "Submit answer",
        "need_number": "Enter a whole number to continue.", "right_feedback": "Correct. Keep your rhythm.",
        "wrong_feedback": "Not quite. The answer was {answer}.", "show_hint": "Show a hint", "hide_hint": "Hide hint",
        "try_again": "Try again", "results_title": "Round complete", "results_copy": "Nice work showing up for practice.",
        "your_score": "Correct answers", "record_label": "Your best at this level", "new_record": "New personal best",
        "play_again": "Play this level again", "back_home": "Back to home", "tutorial_overline": "GUIDED BEGINNER LESSON",
        "tutorial_title_page": "Learn the small steps first.", "tutorial_intro": "Work through six simple examples. Use a hint whenever you need one.",
        "step": "Step {current} of {total}", "tutorial_right": "Exactly right. Here is the next one.",
        "tutorial_wrong": "Try once more, or open the hint for a nudge.", "tutorial_done": "You have finished the beginner lesson.",
        "fsu_overline": "FORMULA PRACTICE", "fsu_title": "Recognize the pattern.", "fsu_intro": "Choose the identity that completes the expression. This untimed round focuses on the three core abbreviated multiplication formulas.",
        "fsu_right": "Correct identity. Keep going.", "fsu_wrong": "Not quite. The identity is {answer}.",
        "fsu_hint_difference": "A difference of squares factors into the difference and the sum of the same two terms.",
        "fsu_hint_sum_square": "Square the first term, add twice their product, then add the square of the second term.",
        "fsu_hint_difference_square": "The middle term is negative twice the product; the final square stays positive.",
        "hint_easy": "Bridge to a multiple of ten or split a number into tens and ones.",
        "hint_normal": "Use a familiar fact, then split the calculation into easier steps.",
        "hint_hard": "Look for a place-value shortcut or split the calculation into parts.",
        "tutorial_hint_1": "Start at 3 and count forward two steps: 4, then 5.",
        "tutorial_hint_2": "Split 5 into 2 and 3. First make 10, then add the remaining 3.",
        "tutorial_hint_3": "Subtract 4 to reach 10, then subtract the remaining 2.",
        "tutorial_hint_4": "Think of 4 groups of 3: 3 + 3 + 3 + 3.",
        "tutorial_hint_5": "Ask how many groups of 5 make 20.",
        "tutorial_hint_6": "Add 1 to reach 20, then add the remaining 5.",
        "guide_title": "A quick guide to FSU practice", "guide_intro": "FSU here means abbreviated multiplication formulas. Learn the three identities, then use them to work with expressions mentally.",
        "guide_flow_title": "How a round works", "guide_flow": "Choose a level, solve the prompt mentally, then enter a whole-number answer. Easy and Normal rounds have a visible countdown. Hard is untimed. Your score counts correct answers. FSU practice is a separate untimed formula round.",
        "guide_fsu_sum_title": "Square of a sum", "guide_fsu_sum": "(a + b)² = a² + 2ab + b². Square each term and add twice their product.",
        "guide_fsu_diff_title": "Square of a difference", "guide_fsu_diff": "(a − b)² = a² − 2ab + b². The middle term is negative; both squared terms are positive.",
        "guide_fsu_squares_title": "Difference of squares", "guide_fsu_squares": "a² − b² = (a − b)(a + b). This is the factorization demonstrated in the original FSU prototype.",
        "guide_add_title": "Addition · make a friendly number", "guide_add": "Split an addend to reach the next ten. For 38 + 17, think 38 + 10 + 7 = 48 + 7 = 55.",
        "guide_sub_title": "Subtraction · bridge through ten", "guide_sub": "Take away enough to reach a round number, then finish the rest. For 14 − 6, subtract 4 to reach 10, then subtract 2: the answer is 8.",
        "guide_mult_title": "Multiplication · split into parts", "guide_mult": "Use a fact you know and distribute. For 7 × 12, calculate 7 × 10 and 7 × 2, then add 70 + 14 = 84.",
        "guide_div_title": "Division · think in groups", "guide_div": "Ask which multiplication fact matches. For 36 ÷ 4, ask how many groups of 4 make 36. Since 4 × 9 = 36, the answer is 9.",
        "guide_tip_title": "Keep the practice useful", "guide_tip": "Say the steps quietly, look for a shortcut, and take your time between rounds. A hint is a learning tool, not a score penalty.",
        "settings_title": "Make the trainer yours", "settings_intro": "Your preferences and best scores are saved locally on this device.",
        "feedback_setting": "Shake on a mistake", "feedback_desc": "Briefly moves the app window and gives a soft tone as desktop feedback.",
        "fsu_hints_setting": "Show hints in FSU practice", "fsu_hints_desc": "Keep an optional strategy hint available during formula rounds.",
        "music_setting": "Loop background music", "music_desc": "Play a quiet, original ambient loop during practice.",
        "music_unavailable": "Audio could not start. Check that this device has an available audio output.",
        "music_ready": "Preference saved.", "music_off": "Background music is off.", "language_desc": "Choose the interface language.",
        "easy_tag": "FOUNDATIONS", "normal_tag": "STEADY PACE", "hard_tag": "DEEP FOCUS",
        "choose_level": "Your level adjusts as you practice", "adaptive_desc": "Start at your current topic. The trainer adjusts question difficulty from your recent accuracy and pace.",
        "mastery_progress": "Topic {current} of {total} · {count} of 20 answers", "mastered_next": "Topic mastered. Your next topic is {topic}.",
        "keep_practicing": "Keep practicing this topic. Aim for at least 90% accuracy and under 3 seconds per answer.", "path_complete": "You completed every topic in the learning path.",
    },
    "Russian": {
        "app_name": "Тренажёр устного счёта", "brand_note": "IT STEP ACADEMY · ЛИЧНЫЙ ПРОЕКТ",
        "practice": "Тренировка", "guide": "Руководство FSU", "settings": "Настройки", "language": "Язык",
        "eyebrow": "ДУМАЙТЕ ЯСНО. СЧИТАЙТЕ СПОКОЙНО.", "headline": "Сильнее мышление — один пример за раз.",
        "home_copy": "Развивайте скорость и уверенность в коротких тренировках устного счёта. Прогресс хранится на этом устройстве.",
        "quick_start": "Быстрая тренировка", "choose_level": "Уровень меняется автоматически по вашим ответам", "start_practice": "Начать обучение",
        "easy": "Лёгкий", "normal": "Средний", "hard": "Сложный", "easy_desc": "Сложение и вычитание до 20 · 60 секунд",
        "normal_desc": "Четыре действия · 45 секунд", "hard_desc": "Большие числа · без таймера",
        "personal_record": "Личные рекорды", "best_score": "Лучший результат", "no_record": "Сыграйте раунд, чтобы установить рекорд.",
        "games_played": "Сессий сыграно", "correct_total": "Верных ответов", "tutorial_title": "Начните с основ",
        "tutorial_copy": "Спокойный урок с небольшими числами и подсказкой на каждом шаге.", "open_tutorial": "Начать урок",
        "fsu_card_title": "Тренировка формул ФСУ", "fsu_card_copy": "Повторите три основные формулы сокращённого умножения в коротких раундах с выбором ответа.", "start_fsu": "Тренировать формулы ФСУ",
        "guide_card_title": "Изучите короткие приёмы", "guide_card_copy": "Узнайте, как работает тренажёр, и повторите стратегии устного счёта.",
        "open_guide": "Открыть руководство FSU", "footer": "Небольшая ежедневная практика даёт заметный результат.",
        "session": "ТРЕНИРОВКА", "practice_title": "Сосредоточьтесь на следующем шаге.", "timed": "ОСТАЛОСЬ",
        "untimed": "БЕЗ ТАЙМЕРА", "score": "СЧЁТ", "correct": "Верно", "mistakes": "Ошибки",
        "finish": "Завершить сессию", "answer_placeholder": "Введите ответ", "submit": "Ответить",
        "need_number": "Введите целое число.", "right_feedback": "Верно. Продолжайте в том же ритме.",
        "wrong_feedback": "Почти. Правильный ответ: {answer}.", "show_hint": "Показать подсказку", "hide_hint": "Скрыть подсказку",
        "try_again": "Ещё раз", "results_title": "Раунд завершён", "results_copy": "Отличная работа: вы нашли время для тренировки.",
        "your_score": "Верных ответов", "record_label": "Ваш лучший результат на этом уровне", "new_record": "Новый личный рекорд",
        "play_again": "Повторить этот уровень", "back_home": "На главную", "tutorial_overline": "УРОК ДЛЯ НАЧИНАЮЩИХ",
        "tutorial_title_page": "Сначала разберём простые шаги.", "tutorial_intro": "Решите шесть простых примеров. Подсказка доступна на каждом шаге.",
        "step": "Шаг {current} из {total}", "tutorial_right": "Именно так. Переходим дальше.",
        "tutorial_wrong": "Попробуйте ещё раз или откройте подсказку.", "tutorial_done": "Вы завершили вводный урок.",
        "fsu_overline": "ТРЕНИРОВКА ФОРМУЛ", "fsu_title": "Найдите знакомую формулу.", "fsu_intro": "Выберите формулу, которая завершает равенство. В этом раунде без таймера повторяются три основные формулы сокращённого умножения.",
        "fsu_right": "Верная формула. Продолжайте.", "fsu_wrong": "Почти. Правильная формула: {answer}.",
        "fsu_hint_difference": "Разность квадратов раскладывается на разность и сумму тех же двух выражений.",
        "fsu_hint_sum_square": "Возведите первое слагаемое в квадрат, прибавьте удвоенное произведение и квадрат второго.",
        "fsu_hint_difference_square": "Средний член — удвоенное произведение со знаком минус. Квадраты в начале и конце положительные.",
        "hint_easy": "Дойдите до круглого десятка или разложите число на десятки и единицы.",
        "hint_normal": "Используйте знакомый пример и разбейте вычисление на простые шаги.",
        "hint_hard": "Ищите приём с разрядностью или разбейте вычисление на части.",
        "tutorial_hint_1": "Начните с 3 и отсчитайте два шага вперёд: сначала 4, затем 5.",
        "tutorial_hint_2": "Разбейте 5 на 2 и 3. Сначала получите 10, затем прибавьте оставшиеся 3.",
        "tutorial_hint_3": "Вычтите 4, чтобы получить 10, затем вычтите ещё 2.",
        "tutorial_hint_4": "Представьте 4 группы по 3: 3 + 3 + 3 + 3.",
        "tutorial_hint_5": "Подумайте, сколько групп по 5 составляют 20.",
        "tutorial_hint_6": "Прибавьте 1, чтобы получить 20, затем прибавьте оставшиеся 5.",
        "guide_title": "Краткое руководство по формулам ФСУ", "guide_intro": "ФСУ — формулы сокращённого умножения. Изучите три тождества и используйте их для быстрых вычислений.",
        "guide_flow_title": "Как проходит раунд", "guide_flow": "Выберите уровень, решите пример в уме и введите целый ответ. В уровнях «Лёгкий» и «Средний» виден таймер. Сложный уровень проходит без таймера. В счёт идут верные ответы. ФСУ — отдельный раунд по формулам без таймера.",
        "guide_fsu_sum_title": "Квадрат суммы", "guide_fsu_sum": "(a + b)² = a² + 2ab + b². Возведите слагаемые в квадрат и прибавьте удвоенное произведение.",
        "guide_fsu_diff_title": "Квадрат разности", "guide_fsu_diff": "(a − b)² = a² − 2ab + b². Средний член отрицательный, оба квадрата положительные.",
        "guide_fsu_squares_title": "Разность квадратов", "guide_fsu_squares": "a² − b² = (a − b)(a + b). Именно эту формулу раскладывала первая версия тренажёра.",
        "guide_add_title": "Сложение · составьте круглое число", "guide_add": "Разбейте слагаемое, чтобы дойти до десятка. Для 38 + 17: 38 + 10 + 7 = 48 + 7 = 55.",
        "guide_sub_title": "Вычитание · пройдите через десяток", "guide_sub": "Сначала вычтите до круглого числа, затем остальное. Для 14 − 6: вычтите 4 до 10, затем ещё 2. Ответ — 8.",
        "guide_mult_title": "Умножение · разбейте на части", "guide_mult": "Используйте знакомый пример. Для 7 × 12: посчитайте 7 × 10 и 7 × 2, затем сложите 70 + 14 = 84.",
        "guide_div_title": "Деление · думайте о группах", "guide_div": "Найдите подходящий пример на умножение. Для 36 ÷ 4 спросите, сколько групп по 4 составляют 36. Так как 4 × 9 = 36, ответ — 9.",
        "guide_tip_title": "Пользуйтесь тренировкой с пользой", "guide_tip": "Проговаривайте шаги, ищите короткий путь и отдыхайте между раундами. Подсказка помогает учиться и не снижает результат.",
        "settings_title": "Настройте тренажёр", "settings_intro": "Настройки и рекорды хранятся локально на этом устройстве.",
        "feedback_setting": "Встряхивать окно при ошибке", "feedback_desc": "Окно ненадолго смещается и звучит тихий сигнал — обратная связь для компьютера.",
        "fsu_hints_setting": "Показывать подсказки в ФСУ", "fsu_hints_desc": "Во время раунда с формулами будет доступна необязательная подсказка.",
        "music_setting": "Фоновая музыка по кругу", "music_desc": "Во время тренировки звучит тихая оригинальная фоновая мелодия.",
        "music_unavailable": "Не удалось включить звук. Проверьте, доступен ли аудиовыход устройства.",
        "music_ready": "Настройка сохранена.", "music_off": "Фоновая музыка выключена.", "language_desc": "Выберите язык интерфейса.",
        "easy_tag": "ОСНОВЫ", "normal_tag": "РОВНЫЙ ТЕМП", "hard_tag": "ПОЛНАЯ КОНЦЕНТРАЦИЯ",
    },
    "Kazakh": {
        "app_name": "Ауызша есеп тренажері", "brand_note": "IT STEP ACADEMY · ЖЕКЕ ЖОБА",
        "practice": "Жаттығу", "guide": "FSU нұсқаулығы", "settings": "Баптаулар", "language": "Тіл",
        "eyebrow": "ОЙЫҢЫЗДЫ ЖИНАҚТАП, САБЫРМЕН ЕСЕПТЕҢІЗ.", "headline": "Әр есеп ойлау қабілетін шыңдайды.",
        "home_copy": "Қысқа ауызша есеп жаттығулары арқылы жылдамдық пен сенімділікті арттырыңыз. Нәтижелер осы құрылғыда сақталады.",
        "quick_start": "Жылдам жаттығу", "choose_level": "Деңгей жауаптарыңызға қарай автоматты өзгереді", "start_practice": "Оқуды бастау",
        "easy": "Оңай", "normal": "Орташа", "hard": "Күрделі", "easy_desc": "20-ға дейін қосу және азайту · 60 секунд",
        "normal_desc": "Төрт амал · 45 секунд", "hard_desc": "Үлкен сандар · уақыт шектеусіз",
        "personal_record": "Жеке рекордтар", "best_score": "Үздік нәтиже", "no_record": "Рекорд орнату үшін бір айналым ойнаңыз.",
        "games_played": "Жаттығу саны", "correct_total": "Дұрыс жауаптар", "tutorial_title": "Негіздерден бастаңыз",
        "tutorial_copy": "Шағын сандармен өтетін сабырлы сабақ. Әр қадамда көмек бар.", "open_tutorial": "Сабақты бастау",
        "fsu_card_title": "Қысқаша көбейту формулалары", "fsu_card_copy": "Үш негізгі формуланы қысқа таңдаулы жауап жаттығуларында қайталаңыз.", "start_fsu": "ФСУ жаттығуын бастау",
        "guide_card_title": "Есептеу тәсілдерін үйреніңіз", "guide_card_copy": "Тренажердің жұмысын көріп, ауызша есеп стратегияларын қайталаңыз.",
        "open_guide": "FSU нұсқаулығын оқу", "footer": "Күнделікті шағын жаттығу үлкен нәтиже береді.",
        "session": "ЖАТТЫҒУ", "practice_title": "Келесі қадамға назар аударыңыз.", "timed": "ҚАЛҒАН УАҚЫТ",
        "untimed": "УАҚЫТСЫЗ ЖАТТЫҒУ", "score": "ҰПАЙ", "correct": "Дұрыс", "mistakes": "Қате",
        "finish": "Жаттығуды аяқтау", "answer_placeholder": "Жауапты енгізіңіз", "submit": "Жауап беру",
        "need_number": "Жалғастыру үшін бүтін сан енгізіңіз.", "right_feedback": "Дұрыс. Осы қарқынды сақтаңыз.",
        "wrong_feedback": "Дәл емес. Дұрыс жауап: {answer}.", "show_hint": "Көмекті көрсету", "hide_hint": "Көмекті жасыру",
        "try_again": "Қайталап көру", "results_title": "Жаттығу аяқталды", "results_copy": "Жаттығуға уақыт бөлгеніңіз жақсы болды.",
        "your_score": "Дұрыс жауаптар", "record_label": "Осы деңгейдегі үздік нәтижеңіз", "new_record": "Жаңа жеке рекорд",
        "play_again": "Осы деңгейді қайталау", "back_home": "Басты бетке оралу", "tutorial_overline": "БАСТАУШЫЛАРҒА АРНАЛҒАН САБАҚ",
        "tutorial_title_page": "Алдымен қарапайым қадамдарды үйреніңіз.", "tutorial_intro": "Алты қарапайым есепті шығарыңыз. Әр қадамда көмек алуға болады.",
        "step": "{total}-ден {current}-қадам", "tutorial_right": "Дұрыс. Келесі есепке өтейік.",
        "tutorial_wrong": "Қайта көріңіз немесе көмекті ашыңыз.", "tutorial_done": "Бастапқы сабақты аяқтадыңыз.",
        "fsu_overline": "ФОРМУЛА ЖАТТЫҒУЫ", "fsu_title": "Формуланы таныңыз.", "fsu_intro": "Өрнекті толықтыратын формуланы таңдаңыз. Таймерсіз жаттығуда қысқаша көбейтудің үш негізгі формуласы қамтылады.",
        "fsu_right": "Дұрыс формула. Жалғастырыңыз.", "fsu_wrong": "Дәл емес. Дұрыс формула: {answer}.",
        "fsu_hint_difference": "Квадраттар айырмасы сол екі өрнектің айырмасы мен қосындысының көбейтіндісіне жіктеледі.",
        "fsu_hint_sum_square": "Бірінші қосылғышты квадраттап, олардың екі еселенген көбейтіндісін және екінші квадратты қосыңыз.",
        "fsu_hint_difference_square": "Ортаңғы мүше — теріс таңбалы екі еселенген көбейтінді. Екі квадрат та оң болады.",
        "hint_easy": "Дөңгелек ондыққа жетіңіз немесе санды ондықтар мен бірліктерге бөліңіз.",
        "hint_normal": "Өзіңіз білетін амалды қолданып, есепті қарапайым қадамдарға бөліңіз.",
        "hint_hard": "Разрядтық тәсілді қолданыңыз немесе есепті бірнеше бөлікке бөліңіз.",
        "tutorial_hint_1": "3 санынан бастап екі қадам алға санаңыз: 4, содан кейін 5.",
        "tutorial_hint_2": "5 санын 2 мен 3-ке бөліңіз. Алдымен 10 жасаңыз, содан кейін қалған 3-ті қосыңыз.",
        "tutorial_hint_3": "10-ға жету үшін 4-ті азайтып, содан кейін тағы 2-ні азайтыңыз.",
        "tutorial_hint_4": "3-тен төрт топ деп ойлаңыз: 3 + 3 + 3 + 3.",
        "tutorial_hint_5": "20 санында 5-тен неше топ бар екенін ойлаңыз.",
        "tutorial_hint_6": "20-ға жету үшін 1-ді, содан кейін қалған 5-ті қосыңыз.",
        "guide_title": "Қысқаша көбейту формулалары", "guide_intro": "FSU — қысқаша көбейту формулалары. Үш тепе-теңдікті үйреніп, ойша есептеуде қолданыңыз.",
        "guide_flow_title": "Жаттығу қалай өтеді", "guide_flow": "Деңгейді таңдап, есепті ойша шығарып, бүтін жауапты енгізіңіз. Оңай және Орташа деңгейлерде таймер көрінеді. Күрделі деңгей уақытсыз өтеді. Ұпайға дұрыс жауаптар есептеледі. ФСУ — формулаларға арналған бөлек, уақытсыз жаттығу.",
        "guide_fsu_sum_title": "Қосындының квадраты", "guide_fsu_sum": "(a + b)² = a² + 2ab + b². Қосылғыштарды квадраттаңыз да, екі еселенген көбейтіндіні қосыңыз.",
        "guide_fsu_diff_title": "Айырманың квадраты", "guide_fsu_diff": "(a − b)² = a² − 2ab + b². Ортаңғы мүше теріс, ал квадраттар оң болады.",
        "guide_fsu_squares_title": "Квадраттар айырмасы", "guide_fsu_squares": "a² − b² = (a − b)(a + b). Бұл формула тренажердің алғашқы нұсқасында болған.",
        "guide_add_title": "Қосу · ондық санға жеткізу", "guide_add": "Келесі ондыққа жету үшін санды бөліңіз. 38 + 17 үшін: 38 + 10 + 7 = 48 + 7 = 55.",
        "guide_sub_title": "Азайту · ондық арқылы өту", "guide_sub": "Алдымен дөңгелек санға дейін, содан кейін қалған бөлігін азайтыңыз. 14 − 6 үшін: 10-ға дейін 4-ті, тағы 2-ні азайтыңыз. Жауап — 8.",
        "guide_mult_title": "Көбейту · бөліктерге ажырату", "guide_mult": "Өзіңіз білетін көбейту амалын қолданыңыз. 7 × 12 үшін: 7 × 10 және 7 × 2 есептеп, 70 + 14 = 84 қосыңыз.",
        "guide_div_title": "Бөлу · топтармен ойлау", "guide_div": "Сәйкес көбейту амалын табыңыз. 36 ÷ 4 үшін 4-тен қанша топ 36 болатынын ойлаңыз. 4 × 9 = 36, демек жауап — 9.",
        "guide_tip_title": "Жаттығуды пайдалы өткізіңіз", "guide_tip": "Қадамдарды іштей айтып, қысқа жол іздеңіз және айналымдар арасында демалыңыз. Көмек оқу үшін берілген, ұпайды төмендетпейді.",
        "settings_title": "Тренажерді өзіңізге бейімдеңіз", "settings_intro": "Баптаулар мен рекордтар осы құрылғыда сақталады.",
        "feedback_setting": "Қате болса, терезе қозғалсын", "feedback_desc": "Терезе сәл қозғалып, дыбыс береді — компьютерге арналған қысқа белгі.",
        "fsu_hints_setting": "ФСУ жаттығуында көмек көрсету", "fsu_hints_desc": "Формула жаттығуларында қосымша көмек қолжетімді болады.",
        "music_setting": "Фондық әуенді қайталау", "music_desc": "Жаттығу кезінде баяу, арнайы жасалған әуен ойнайды.",
        "music_unavailable": "Дыбысты қосу мүмкін болмады. Құрылғының дыбыс шығысын тексеріңіз.",
        "music_ready": "Баптау сақталды.", "music_off": "Фондық әуен өшірулі.", "language_desc": "Интерфейс тілін таңдаңыз.",
        "easy_tag": "НЕГІЗДЕР", "normal_tag": "БІРҚАЛЫПТЫ ҚАРҚЫН", "hard_tag": "ТЕРЕҢ ЗЕЙІН",
    },
}


class MentalMathApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.settings = load_settings()
        self.stats = load_stats()
        self.audio = AudioManager()
        self.language = self.settings["language"]
        self.music_available = True
        self.screen = "home"
        self.selected_difficulty = "normal"
        self.session_active = False
        self.timer_job = None
        self.advance_job = None
        self.correct = 0
        self.wrong = 0
        self.tutorial_items = ()
        self.tutorial_index = 0
        self.hint_visible = False
        self.answer_locked = False
        self.question = None
        self.result = {}

        self.title(self.t("app_name"))
        self.geometry("960x690")
        self.minsize(790, 610)
        self.configure(bg=COLORS["background"])
        self.protocol("WM_DELETE_WINDOW", self._close)
        self._configure_style()
        self._render()
        if self.settings["music_enabled"]:
            self.music_available = self.audio.set_music(True)

    def t(self, key: str, **values) -> str:
        text = TEXT.get(self.language, TEXT["English"]).get(key, TEXT["English"].get(key, key))
        return text.format(**values) if values else text

    def _configure_style(self) -> None:
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("App.TFrame", background=COLORS["background"])
        style.configure("Card.TFrame", background=COLORS["surface"], relief="flat")
        style.configure("Hero.TFrame", background="#eaf0ff", relief="flat")
        style.configure("TLabel", background=COLORS["background"], foreground=COLORS["ink"], font=("TkDefaultFont", 11))
        style.configure("Card.TLabel", background=COLORS["surface"], foreground=COLORS["ink"], font=("TkDefaultFont", 11))
        style.configure("Muted.TLabel", background=COLORS["background"], foreground=COLORS["muted"], font=("TkDefaultFont", 10))
        style.configure("CardMuted.TLabel", background=COLORS["surface"], foreground=COLORS["muted"], font=("TkDefaultFont", 10))
        style.configure("Brand.TLabel", background=COLORS["surface"], foreground=COLORS["ink"], font=("TkDefaultFont", 13, "bold"))
        style.configure("Kicker.TLabel", background=COLORS["background"], foreground=COLORS["accent"], font=("TkDefaultFont", 9, "bold"))
        style.configure("HeroKicker.TLabel", background="#eaf0ff", foreground=COLORS["accent"], font=("TkDefaultFont", 9, "bold"))
        style.configure("CardKicker.TLabel", background=COLORS["surface"], foreground=COLORS["accent"], font=("TkDefaultFont", 9, "bold"))
        style.configure("HeroTitle.TLabel", background="#eaf0ff", foreground=COLORS["ink"], font=("TkDefaultFont", 27, "bold"))
        style.configure("PageTitle.TLabel", background=COLORS["background"], foreground=COLORS["ink"], font=("TkDefaultFont", 23, "bold"))
        style.configure("Section.TLabel", background=COLORS["surface"], foreground=COLORS["ink"], font=("TkDefaultFont", 15, "bold"))
        style.configure("Question.TLabel", background=COLORS["surface"], foreground=COLORS["ink"], font=("TkDefaultFont", 37, "bold"))
        style.configure("Score.TLabel", background=COLORS["surface"], foreground=COLORS["accent"], font=("TkDefaultFont", 29, "bold"))
        style.configure("TButton", font=("TkDefaultFont", 10, "bold"), padding=(14, 10), borderwidth=0)
        style.configure("Accent.TButton", background=COLORS["accent"], foreground="#ffffff", font=("TkDefaultFont", 10, "bold"), padding=(16, 11))
        style.map("Accent.TButton", background=[("active", COLORS["accent_hover"]), ("disabled", "#aab8d7")], foreground=[("disabled", "#f8faff")])
        style.configure("Secondary.TButton", background="#edf1f7", foreground=COLORS["ink"], padding=(13, 10))
        style.map("Secondary.TButton", background=[("active", "#e1e8f2")])
        style.configure("Nav.TButton", background=COLORS["surface"], foreground=COLORS["muted"], padding=(9, 8))
        style.map("Nav.TButton", background=[("active", "#edf1f7")], foreground=[("active", COLORS["ink"])])
        style.configure("TEntry", padding=(11, 10), fieldbackground="#ffffff", foreground=COLORS["ink"], bordercolor=COLORS["line"], insertcolor=COLORS["ink"])
        style.configure("TCombobox", padding=(8, 7), fieldbackground="#ffffff", background="#ffffff", foreground=COLORS["ink"])
        style.map("TCombobox", fieldbackground=[("readonly", "#ffffff")], foreground=[("readonly", COLORS["ink"])])
        style.configure("TCheckbutton", background=COLORS["surface"], foreground=COLORS["ink"], font=("TkDefaultFont", 11))
        style.map("TCheckbutton", background=[("active", COLORS["surface"])])
        style.configure("Accent.Horizontal.TProgressbar", troughcolor="#e5eaf2", background=COLORS["accent"], thickness=10)

    def _render(self) -> None:
        self.title(self.t("app_name"))
        for child in self.winfo_children():
            child.destroy()

        header = ttk.Frame(self, style="Card.TFrame", padding=(27, 13))
        header.pack(fill="x")
        header.columnconfigure(1, weight=1)
        ttk.Label(header, text="MENTAL MATH", style="Brand.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(header, text=self.t("brand_note"), style="CardMuted.TLabel").grid(row=1, column=0, sticky="w", pady=(2, 0))

        nav = ttk.Frame(header, style="Card.TFrame")
        nav.grid(row=0, column=1, rowspan=2, sticky="e", padx=(15, 19))
        for screen, label in (("home", "practice"), ("guide", "guide"), ("settings", "settings")):
            style = "Accent.TButton" if (self.screen in ("home", "practice", "results", "tutorial", "fsu") and screen == "home") or self.screen == screen else "Nav.TButton"
            ttk.Button(nav, text=self.t(label), style=style, command=lambda selected=screen: self._navigate(selected)).pack(side="left", padx=3)

        language_box = ttk.Frame(header, style="Card.TFrame")
        language_box.grid(row=0, column=2, rowspan=2, sticky="e")
        ttk.Label(language_box, text=self.t("language"), style="CardMuted.TLabel").pack(anchor="w")
        self.language_var = tk.StringVar(value=self.language)
        language_select = ttk.Combobox(language_box, textvariable=self.language_var, values=("English", "Russian", "Kazakh"), state="readonly", width=11)
        language_select.pack(anchor="e", pady=(3, 0))
        language_select.bind("<<ComboboxSelected>>", self._language_changed)

        page = ttk.Frame(self, style="App.TFrame", padding=(34, 27, 34, 17))
        page.pack(fill="both", expand=True)
        if self.screen == "home":
            self._render_home(page)
        elif self.screen == "practice":
            self._render_practice(page)
        elif self.screen == "tutorial":
            self._render_tutorial(page)
        elif self.screen == "fsu":
            self._render_fsu(page)
        elif self.screen == "guide":
            self._render_guide(page)
        elif self.screen == "settings":
            self._render_settings(page)
        else:
            self._render_results(page)

    def _navigate(self, screen: str) -> None:
        if self.screen in ("practice", "tutorial", "fsu"):
            self._stop_session()
        self.screen = screen
        self._render()

    def _language_changed(self, _event=None) -> None:
        self.language = self.language_var.get()
        self.settings["language"] = self.language
        save_settings(self.settings)
        self._render()

    def _render_home(self, parent) -> None:
        hero = ttk.Frame(parent, style="Hero.TFrame", padding=(27, 23))
        hero.pack(fill="x")
        ttk.Label(hero, text=self.t("eyebrow"), style="HeroKicker.TLabel").pack(anchor="w")
        ttk.Label(hero, text=self.t("headline"), style="HeroTitle.TLabel", wraplength=820, justify="left").pack(anchor="w", pady=(7, 7))
        ttk.Label(hero, text=self.t("home_copy"), style="Muted.TLabel", wraplength=800, justify="left").pack(anchor="w")

        columns = ttk.Frame(parent, style="App.TFrame")
        columns.pack(fill="x", pady=(17, 0))
        columns.columnconfigure(0, weight=3, uniform="home")
        columns.columnconfigure(1, weight=2, uniform="home")
        quick = ttk.Frame(columns, style="Card.TFrame", padding=19)
        quick.grid(row=0, column=0, sticky="nsew", padx=(0, 9))
        ttk.Label(quick, text=self.t("quick_start"), style="Section.TLabel").pack(anchor="w")
        ttk.Label(quick, text=self.t("choose_level"), style="CardMuted.TLabel").pack(anchor="w", pady=(12, 5))
        topic_id = self.stats.get("curriculum_topic", CURRICULUM[0].id)
        current = next((item for item in CURRICULUM if item.id == topic_id), CURRICULUM[0])
        ttk.Label(quick, text=f"{current.stage}. {current.title}", style="Card.TLabel", font=("TkDefaultFont", 12, "bold")).pack(anchor="w", pady=(4, 3))
        ttk.Label(quick, text=f"{current.description}\n{self.t('adaptive_desc')}", style="CardMuted.TLabel", wraplength=420).pack(anchor="w", pady=(2, 12))
        ttk.Button(quick, text=self.t("start_practice"), style="Accent.TButton", command=self._start_practice).pack(anchor="w")

        records = ttk.Frame(columns, style="Card.TFrame", padding=19)
        records.grid(row=0, column=1, sticky="nsew", padx=(9, 0))
        ttk.Label(records, text=self.t("personal_record"), style="Section.TLabel").pack(anchor="w")
        ttk.Label(records, text=self.t("best_score"), style="CardMuted.TLabel").pack(anchor="w", pady=(10, 2))
        values = [f"{self.t(key)}  ·  {self.stats['best_scores'].get(key, '—')}" for key in ("easy", "normal", "hard")]
        for value in values:
            ttk.Label(records, text=value, style="Card.TLabel", font=("TkDefaultFont", 11, "bold")).pack(anchor="w", pady=3)
        ttk.Label(records, text=f"FSU  ·  {self.stats['best_scores'].get('fsu', '—')}", style="Card.TLabel", font=("TkDefaultFont", 11, "bold")).pack(anchor="w", pady=3)
        ttk.Label(records, text=f"{self.t('games_played')}: {self.stats['games_played']}", style="CardMuted.TLabel").pack(anchor="w", pady=(9, 2))
        ttk.Label(records, text=f"{self.t('correct_total')}: {self.stats['correct_total']}", style="CardMuted.TLabel").pack(anchor="w")

        lower = ttk.Frame(parent, style="App.TFrame")
        lower.pack(fill="x", pady=(14, 0))
        for column in range(3):
            lower.columnconfigure(column, weight=1, uniform="lower")
        self._home_link_card(lower, 0, "tutorial_title", "tutorial_copy", "open_tutorial", "tutorial")
        self._home_link_card(lower, 1, "fsu_card_title", "fsu_card_copy", "start_fsu", "fsu")
        self._home_link_card(lower, 2, "guide_card_title", "guide_card_copy", "open_guide", "guide")
        ttk.Label(parent, text=self.t("footer"), style="Muted.TLabel").pack(anchor="w", pady=(13, 0))

    def _home_link_card(self, parent, column, title_key, copy_key, button_key, screen) -> None:
        card = ttk.Frame(parent, style="Card.TFrame", padding=16)
        card.grid(row=0, column=column, sticky="nsew", padx=(0, 5) if column == 0 else (5, 0) if column == 2 else 5)
        ttk.Label(card, text=self.t(title_key), style="Section.TLabel").pack(anchor="w")
        ttk.Label(card, text=self.t(copy_key), style="CardMuted.TLabel", wraplength=260, justify="left").pack(anchor="w", pady=(5, 11))
        if screen == "tutorial":
            command = self._begin_tutorial
        elif screen == "fsu":
            command = self._start_fsu
        else:
            command = lambda: self._navigate(screen)
        ttk.Button(card, text=self.t(button_key), style="Secondary.TButton", command=command).pack(anchor="w")

    def _select_difficulty(self, displayed: str) -> None:
        for level in ("easy", "normal", "hard"):
            if displayed == self.t(level):
                self.selected_difficulty = level
                self.level_description.config(text=self.t(f"{level}_desc"))
                return

    def _start_practice(self) -> None:
        self.correct = 0
        self.wrong = 0
        self.selected_difficulty = "curriculum"
        self.active_topic = next((item for item in CURRICULUM if item.id == self.stats.get("curriculum_topic")), CURRICULUM[0])
        self.topic_answer_times = []
        self.topic_outcomes = []
        self.seen_topic_questions = set()
        self.topic_started = time.monotonic()
        self.question_started = self.topic_started
        self.adaptive_band = 0
        self.question = self._new_curriculum_question()
        self.session_started = time.monotonic()
        self.session_active = True
        self.screen = "practice"
        self._render()
        self.answer_entry.focus_set()
        self._tick_clock()

    def _render_practice(self, parent) -> None:
        ttk.Label(parent, text=self.t("session"), style="Kicker.TLabel").pack(anchor="w")
        ttk.Label(parent, text=self.t("practice_title"), style="PageTitle.TLabel").pack(anchor="w", pady=(4, 14))

        stats = ttk.Frame(parent, style="App.TFrame")
        stats.pack(fill="x", pady=(0, 12))
        if self.selected_difficulty in ("easy", "normal"):
            self.timer_label = ttk.Label(stats, text="", style="Card.TLabel", font=("TkDefaultFont", 10, "bold"))
            self.timer_label.pack(anchor="w")
            self.progress = ttk.Progressbar(stats, style="Accent.Horizontal.TProgressbar", maximum=100)
            self.progress.pack(fill="x", pady=(5, 3))
        else:
            ttk.Label(stats, text=self.t("untimed"), style="Kicker.TLabel").pack(anchor="w")

        card = ttk.Frame(parent, style="Card.TFrame", padding=(28, 23))
        card.pack(fill="both", expand=True)
        score_row = ttk.Frame(card, style="Card.TFrame")
        score_row.pack(fill="x")
        if self.selected_difficulty == "curriculum":
            self.topic_progress_label = ttk.Label(card, text=f"{self.active_topic.stage}. {self.active_topic.title} · {self.t('mastery_progress', current=self.active_topic.stage, total=len(CURRICULUM), count=self.correct+self.wrong)}", style="CardMuted.TLabel")
            self.topic_progress_label.pack(anchor="w", pady=(10, 0))
        ttk.Label(score_row, text=f"{self.t('score')}  {self.correct}", style="Card.TLabel", font=("TkDefaultFont", 11, "bold")).pack(side="left")
        ttk.Label(score_row, text=f"{self.t('mistakes')}  {self.wrong}", style="CardMuted.TLabel").pack(side="right")

        self.question_label = ttk.Label(card, text=self.question.prompt, style="Question.TLabel", anchor="center")
        self.question_label.pack(fill="x", pady=(29, 21))
        answer_row = ttk.Frame(card, style="Card.TFrame")
        answer_row.pack()
        self.answer_var = tk.StringVar()
        self.answer_entry = ttk.Entry(answer_row, textvariable=self.answer_var, font=("TkDefaultFont", 16), width=22, justify="center")
        self.answer_entry.pack(side="left", padx=(0, 9))
        if self.answer_locked:
            self.answer_entry.state(["disabled"])
        self.answer_entry.bind("<Return>", self._submit_practice)
        self.submit_button = ttk.Button(answer_row, text=self.t("submit"), style="Accent.TButton", command=self._submit_practice)
        self.submit_button.pack(side="left")
        if self.answer_locked:
            self.submit_button.state(["disabled"])

        actions = ttk.Frame(card, style="Card.TFrame")
        actions.pack(fill="x", pady=(16, 0))
        self.hint_label = ttk.Label(actions, text="", style="CardMuted.TLabel", wraplength=580)
        self.hint_label.pack(side="left", anchor="w", fill="x", expand=True)
        self.hint_button = ttk.Button(actions, text=self.t("show_hint"), style="Secondary.TButton", command=self._show_practice_hint)
        self.hint_button.pack(side="right")
        self.feedback = ttk.Label(card, text="", style="CardMuted.TLabel", anchor="center", font=("TkDefaultFont", 11, "bold"))
        self.feedback.pack(fill="x", pady=(12, 0))

        ttk.Button(parent, text=self.t("finish"), style="Nav.TButton", command=self._finish_practice).pack(anchor="e", pady=(11, 0))

    def _tick_clock(self) -> None:
        if not self.session_active or self.screen != "practice" or self.selected_difficulty in ("hard", "curriculum"):
            return
        limit = 60 if self.selected_difficulty == "easy" else 45
        elapsed = time.monotonic() - self.session_started
        remaining = max(0, limit - elapsed)
        if hasattr(self, "timer_label") and self.timer_label.winfo_exists():
            self.timer_label.config(text=f"{self.t('timed')}  {int(remaining + 0.999)}s")
            self.progress.configure(value=100 * remaining / limit)
        if remaining <= 0:
            self._finish_practice()
        else:
            self.timer_job = self.after(120, self._tick_clock)

    def _submit_practice(self, _event=None):
        if not self.session_active or self.answer_locked:
            return "break"
        value = self.answer_var.get().strip()
        try:
            answer = int(value)
        except ValueError:
            self.feedback.config(text=self.t("need_number"), foreground=COLORS["error"])
            return "break"
        if answer == self.question.answer:
            self.correct += 1
            if self.selected_difficulty == "curriculum": self.topic_outcomes.append(True)
            self.feedback.config(text=self.t("right_feedback"), foreground=COLORS["success"])
        else:
            self.wrong += 1
            if self.selected_difficulty == "curriculum": self.topic_outcomes.append(False)
            self.feedback.config(text=self.t("wrong_feedback", answer=self.question.answer), foreground=COLORS["error"])
            self._mistake_feedback()
        if self.selected_difficulty == "curriculum":
            self.topic_answer_times.append(time.monotonic() - self.question_started)
            recent = self.topic_answer_times[-5:]
            recent_accuracy = sum(self.topic_outcomes[-5:]) / len(self.topic_outcomes[-5:]) if self.topic_outcomes else 0
            recent_speed = sum(recent) / len(recent) if recent else 0
            if len(recent) >= 5:
                if recent_accuracy >= .8 and recent_speed < 3:
                    self.adaptive_band = min(2, self.adaptive_band + 1)
                elif recent_accuracy < .6 or recent_speed > 5:
                    self.adaptive_band = max(0, self.adaptive_band - 1)
        self.answer_locked = True
        self.submit_button.state(["disabled"])
        self.answer_entry.state(["disabled"])
        self._update_session_counts()
        self.advance_job = self.after(620, self._finish_practice if self.selected_difficulty == "curriculum" and self.correct + self.wrong >= 20 else self._next_practice_question)
        return "break"

    def _new_curriculum_question(self):
        """Generate a fresh prompt for this topic run, avoiding repeats."""
        for _ in range(100):
            question = make_topic_question(self.active_topic.id, self.adaptive_band)
            if question.prompt not in self.seen_topic_questions:
                self.seen_topic_questions.add(question.prompt)
                return question
        return question

    def _update_session_counts(self) -> None:
        if self.selected_difficulty == "curriculum" and hasattr(self, "topic_progress_label") and self.topic_progress_label.winfo_exists():
            count = self.correct + self.wrong
            self.topic_progress_label.config(text=f"{self.active_topic.stage}. {self.active_topic.title} · {self.t('mastery_progress', current=self.active_topic.stage, total=len(CURRICULUM), count=count)}")
        if hasattr(self, "question_label") and self.question_label.winfo_exists():
            for child in self.question_label.master.winfo_children():
                if isinstance(child, ttk.Frame) and child.winfo_children():
                    first = child.winfo_children()[0]
                    if isinstance(first, ttk.Label) and first.cget("text").startswith(self.t("score")):
                        first.config(text=f"{self.t('score')}  {self.correct}")
                        child.winfo_children()[1].config(text=f"{self.t('mistakes')}  {self.wrong}")
                        break

    def _next_practice_question(self) -> None:
        self.advance_job = None
        if not self.session_active or self.screen != "practice":
            return
        self.question = self._new_curriculum_question() if self.selected_difficulty == "curriculum" else make_question(self.selected_difficulty)
        self.question_started = time.monotonic()
        self.answer_locked = False
        self.question_label.config(text=self.question.prompt)
        self.answer_var.set("")
        self.feedback.config(text="")
        self.hint_label.config(text="")
        self.hint_button.config(text=self.t("show_hint"), command=self._show_practice_hint)
        self.submit_button.state(["!disabled"])
        self.answer_entry.state(["!disabled"])
        self.answer_entry.focus_set()

    def _show_practice_hint(self) -> None:
        self.hint_label.config(text=self.t(self.question.hint_key))
        self.hint_button.config(text=self.t("hide_hint"), command=self._hide_practice_hint)

    def _hide_practice_hint(self) -> None:
        self.hint_label.config(text="")
        self.hint_button.config(text=self.t("show_hint"), command=self._show_practice_hint)

    def _finish_practice(self) -> None:
        if not self.session_active:
            return
        if self.selected_difficulty == "curriculum":
            total = self.correct + self.wrong
            accuracy = self.correct / total if total else 0
            average = sum(self.topic_answer_times) / len(self.topic_answer_times) if self.topic_answer_times else float("inf")
            mastered = total >= 20 and accuracy >= .9 and average < 3
            mastered_topics = list(self.stats.get("mastered_topics", []))
            topic_index = next(i for i, item in enumerate(CURRICULUM) if item.id == self.active_topic.id)
            if mastered and self.active_topic.id not in mastered_topics:
                mastered_topics.append(self.active_topic.id)
            next_topic = CURRICULUM[topic_index + 1] if mastered and topic_index + 1 < len(CURRICULUM) else self.active_topic
            records = dict(self.stats.get("topic_records", {}))
            records[self.active_topic.id] = {"correct": self.correct, "total": total, "accuracy": accuracy, "average_seconds": average if average != float("inf") else None}
            record_session("curriculum", self.correct)
            self.stats = save_curriculum(next_topic.id, mastered_topics, records)
            self.result = {"curriculum": True, "mastered": mastered, "next_topic": next_topic.title, "complete": mastered and topic_index + 1 >= len(CURRICULUM), "score": self.correct}
            self._stop_session(); self.screen = "results"; self._render(); return
        self._finish_round(self.selected_difficulty, tutorial=False)

    def _start_fsu(self) -> None:
        self.correct = 0
        self.wrong = 0
        self.question = make_formula_question()
        self.answer_locked = False
        self.session_active = True
        self.screen = "fsu"
        self._render()

    def _render_fsu(self, parent) -> None:
        ttk.Label(parent, text=self.t("fsu_overline"), style="Kicker.TLabel").pack(anchor="w")
        ttk.Label(parent, text=self.t("fsu_title"), style="PageTitle.TLabel").pack(anchor="w", pady=(4, 3))
        ttk.Label(parent, text=self.t("fsu_intro"), style="Muted.TLabel", wraplength=820).pack(anchor="w", pady=(0, 12))
        card = ttk.Frame(parent, style="Card.TFrame", padding=(26, 21))
        card.pack(fill="both", expand=True)
        score_row = ttk.Frame(card, style="Card.TFrame")
        score_row.pack(fill="x")
        ttk.Label(score_row, text=f"{self.t('score')}  {self.correct}", style="Card.TLabel", font=("TkDefaultFont", 11, "bold")).pack(side="left")
        ttk.Label(score_row, text=f"{self.t('mistakes')}  {self.wrong}", style="CardMuted.TLabel").pack(side="right")
        self.question_label = ttk.Label(card, text=self.question.prompt, style="Question.TLabel", anchor="center")
        self.question_label.pack(fill="x", pady=(22, 18))
        choices = ttk.Frame(card, style="Card.TFrame")
        choices.pack(fill="x")
        choices.columnconfigure(0, weight=1, uniform="answer")
        choices.columnconfigure(1, weight=1, uniform="answer")
        self.choice_buttons = []
        for index, choice in enumerate(self.question.choices):
            button = ttk.Button(choices, text=choice, style="Secondary.TButton", command=lambda answer=choice: self._submit_fsu_choice(answer))
            button.grid(row=index // 2, column=index % 2, sticky="ew", padx=5, pady=5, ipady=5)
            if self.answer_locked:
                button.state(["disabled"])
            self.choice_buttons.append(button)
        if self.settings["fsu_hints"]:
            actions = ttk.Frame(card, style="Card.TFrame")
            actions.pack(fill="x", pady=(13, 0))
            self.hint_label = ttk.Label(actions, text="", style="CardMuted.TLabel", wraplength=570)
            self.hint_label.pack(side="left", anchor="w", fill="x", expand=True)
            self.hint_button = ttk.Button(actions, text=self.t("show_hint"), style="Secondary.TButton", command=self._show_practice_hint)
            self.hint_button.pack(side="right")
        self.feedback = ttk.Label(card, text="", style="CardMuted.TLabel", anchor="center", font=("TkDefaultFont", 11, "bold"))
        self.feedback.pack(fill="x", pady=(12, 0))
        ttk.Button(parent, text=self.t("finish"), style="Nav.TButton", command=self._finish_fsu).pack(anchor="e", pady=(11, 0))

    def _submit_fsu_choice(self, choice: str) -> None:
        if not self.session_active or self.answer_locked:
            return
        self.answer_locked = True
        for button in self.choice_buttons:
            button.state(["disabled"])
        if choice == self.question.answer:
            self.correct += 1
            self.feedback.config(text=self.t("fsu_right"), foreground=COLORS["success"])
        else:
            self.wrong += 1
            self.feedback.config(text=self.t("fsu_wrong", answer=self.question.answer), foreground=COLORS["error"])
            self._mistake_feedback()
        self._update_session_counts()
        self.advance_job = self.after(620, self._next_fsu_question)

    def _next_fsu_question(self) -> None:
        self.advance_job = None
        if not self.session_active or self.screen != "fsu":
            return
        self.question = make_formula_question()
        self.answer_locked = False
        self._render()

    def _finish_fsu(self) -> None:
        if self.session_active:
            self._finish_round("fsu", tutorial=False)

    def _finish_round(self, level: str, tutorial: bool) -> None:
        self._stop_session()
        previous = self.stats["best_scores"].get(level, 0)
        self.stats = record_session(level, self.correct)
        self.result = {
            "level": level,
            "score": self.correct,
            "best": self.stats["best_scores"].get(level, 0),
            "new_record": self.correct > previous,
            "tutorial": tutorial,
        }
        self.screen = "results"
        self._render()

    def _begin_tutorial(self) -> None:
        self.tutorial_items = tutorial_questions()
        self.tutorial_index = 0
        self.correct = 0
        self.wrong = 0
        self.hint_visible = False
        self.question = self.tutorial_items[0]
        self.session_active = True
        self.screen = "tutorial"
        self._render()
        self.answer_entry.focus_set()

    def _render_tutorial(self, parent) -> None:
        ttk.Label(parent, text=self.t("tutorial_overline"), style="Kicker.TLabel").pack(anchor="w")
        ttk.Label(parent, text=self.t("tutorial_title_page"), style="PageTitle.TLabel").pack(anchor="w", pady=(4, 3))
        ttk.Label(parent, text=self.t("tutorial_intro"), style="Muted.TLabel", wraplength=800).pack(anchor="w", pady=(0, 12))
        card = ttk.Frame(parent, style="Card.TFrame", padding=(28, 23))
        card.pack(fill="both", expand=True)
        ttk.Label(card, text=self.t("step", current=self.tutorial_index + 1, total=len(self.tutorial_items)), style="CardKicker.TLabel").pack(anchor="w")
        self.question_label = ttk.Label(card, text=self.question.prompt, style="Question.TLabel", anchor="center")
        self.question_label.pack(fill="x", pady=(22, 16))
        answer_row = ttk.Frame(card, style="Card.TFrame")
        answer_row.pack()
        self.answer_var = tk.StringVar()
        self.answer_entry = ttk.Entry(answer_row, textvariable=self.answer_var, font=("TkDefaultFont", 16), width=22, justify="center")
        self.answer_entry.pack(side="left", padx=(0, 9))
        if self.answer_locked:
            self.answer_entry.state(["disabled"])
        self.answer_entry.bind("<Return>", self._submit_tutorial)
        self.submit_button = ttk.Button(answer_row, text=self.t("submit"), style="Accent.TButton", command=self._submit_tutorial)
        self.submit_button.pack(side="left")
        if self.answer_locked:
            self.submit_button.state(["disabled"])
        actions = ttk.Frame(card, style="Card.TFrame")
        actions.pack(fill="x", pady=(15, 0))
        self.hint_label = ttk.Label(actions, text=self.t(self.question.hint_key) if self.hint_visible else "", style="CardMuted.TLabel", wraplength=580)
        self.hint_label.pack(side="left", anchor="w", fill="x", expand=True)
        self.hint_button = ttk.Button(actions, text=self.t("hide_hint") if self.hint_visible else self.t("show_hint"), style="Secondary.TButton", command=self._toggle_tutorial_hint)
        self.hint_button.pack(side="right")
        self.feedback = ttk.Label(card, text="", style="CardMuted.TLabel", anchor="center", font=("TkDefaultFont", 11, "bold"))
        self.feedback.pack(fill="x", pady=(12, 0))

    def _toggle_tutorial_hint(self) -> None:
        self.hint_visible = not self.hint_visible
        self.hint_label.config(text=self.t(self.question.hint_key) if self.hint_visible else "")
        self.hint_button.config(text=self.t("hide_hint") if self.hint_visible else self.t("show_hint"))

    def _submit_tutorial(self, _event=None):
        if not self.session_active or self.answer_locked:
            return "break"
        value = self.answer_var.get().strip()
        try:
            answer = int(value)
        except ValueError:
            self.feedback.config(text=self.t("need_number"), foreground=COLORS["error"])
            return "break"
        if answer == self.question.answer:
            self.correct += 1
            self.answer_locked = True
            self.feedback.config(text=self.t("tutorial_right"), foreground=COLORS["success"])
            self.submit_button.state(["disabled"])
            self.answer_entry.state(["disabled"])
            self.advance_job = self.after(650, self._advance_tutorial)
        else:
            self.wrong += 1
            self.feedback.config(text=self.t("tutorial_wrong"), foreground=COLORS["error"])
            self.answer_var.set("")
            self._mistake_feedback()
        return "break"

    def _advance_tutorial(self) -> None:
        self.advance_job = None
        if not self.session_active or self.screen != "tutorial":
            return
        self.tutorial_index += 1
        if self.tutorial_index >= len(self.tutorial_items):
            self._finish_tutorial()
            return
        self.question = self.tutorial_items[self.tutorial_index]
        self.hint_visible = False
        self.answer_locked = False
        self._render()
        self.answer_entry.focus_set()

    def _finish_tutorial(self) -> None:
        self._finish_round("tutorial", tutorial=True)

    def _render_guide(self, parent) -> None:
        ttk.Label(parent, text=self.t("guide_title"), style="PageTitle.TLabel").pack(anchor="w")
        ttk.Label(parent, text=self.t("guide_intro"), style="Muted.TLabel", wraplength=850).pack(anchor="w", pady=(5, 13))
        content = ttk.Frame(parent, style="App.TFrame")
        content.pack(fill="both", expand=True)
        content.columnconfigure(0, weight=1, uniform="guide")
        content.columnconfigure(1, weight=1, uniform="guide")
        items = (
            ("guide_flow_title", "guide_flow"), ("guide_fsu_sum_title", "guide_fsu_sum"),
            ("guide_fsu_diff_title", "guide_fsu_diff"), ("guide_fsu_squares_title", "guide_fsu_squares"),
            ("guide_add_title", "guide_add"), ("guide_sub_title", "guide_sub"),
            ("guide_mult_title", "guide_mult"), ("guide_div_title", "guide_div"),
            ("guide_tip_title", "guide_tip"),
        )
        for index, (title, copy) in enumerate(items):
            card = ttk.Frame(content, style="Card.TFrame", padding=(17, 14))
            card.grid(row=index // 2, column=index % 2, sticky="nsew", padx=(0, 7) if index % 2 == 0 else (7, 0), pady=6)
            ttk.Label(card, text=self.t(title), style="Section.TLabel", wraplength=380).pack(anchor="w")
            ttk.Label(card, text=self.t(copy), style="CardMuted.TLabel", wraplength=410, justify="left").pack(anchor="w", pady=(6, 0))
        actions = ttk.Frame(parent, style="App.TFrame")
        actions.pack(anchor="w", pady=(10, 0))
        ttk.Button(actions, text=self.t("start_fsu"), style="Accent.TButton", command=self._start_fsu).pack(side="left", padx=(0, 8))
        ttk.Button(actions, text=self.t("start_practice"), style="Secondary.TButton", command=self._start_practice).pack(side="left")

    def _render_settings(self, parent) -> None:
        ttk.Label(parent, text=self.t("settings_title"), style="PageTitle.TLabel").pack(anchor="w")
        ttk.Label(parent, text=self.t("settings_intro"), style="Muted.TLabel", wraplength=780).pack(anchor="w", pady=(5, 16))
        card = ttk.Frame(parent, style="Card.TFrame", padding=(23, 19))
        card.pack(fill="x", anchor="n")

        self.shake_var = tk.BooleanVar(value=self.settings["shake_on_mistake"])
        ttk.Checkbutton(card, text=self.t("feedback_setting"), variable=self.shake_var, command=self._save_feedback_setting).pack(anchor="w")
        ttk.Label(card, text=self.t("feedback_desc"), style="CardMuted.TLabel", wraplength=760).pack(anchor="w", padx=(25, 0), pady=(2, 16))

        self.fsu_hints_var = tk.BooleanVar(value=self.settings["fsu_hints"])
        ttk.Checkbutton(card, text=self.t("fsu_hints_setting"), variable=self.fsu_hints_var, command=self._save_fsu_hints_setting).pack(anchor="w")
        ttk.Label(card, text=self.t("fsu_hints_desc"), style="CardMuted.TLabel", wraplength=760).pack(anchor="w", padx=(25, 0), pady=(2, 16))

        self.music_var = tk.BooleanVar(value=self.settings["music_enabled"])
        ttk.Checkbutton(card, text=self.t("music_setting"), variable=self.music_var, command=self._save_music_setting).pack(anchor="w")
        ttk.Label(card, text=self.t("music_desc"), style="CardMuted.TLabel", wraplength=760).pack(anchor="w", padx=(25, 0), pady=(2, 6))
        if not self.settings["music_enabled"]:
            music_status = self.t("music_off")
        elif self.music_available:
            music_status = self.t("music_ready")
        else:
            music_status = self.t("music_unavailable")
        self.music_status = ttk.Label(card, text=music_status, style="CardMuted.TLabel", wraplength=760)
        self.music_status.pack(anchor="w", padx=(25, 0))
        language_card = ttk.Frame(parent, style="Card.TFrame", padding=(23, 16))
        language_card.pack(fill="x", pady=(12, 0))
        ttk.Label(language_card, text=self.t("language"), style="Section.TLabel").pack(anchor="w")
        ttk.Label(language_card, text=self.t("language_desc"), style="CardMuted.TLabel").pack(anchor="w", pady=(3, 9))
        ttk.Label(language_card, text=self.language, style="Card.TLabel", font=("TkDefaultFont", 11, "bold")).pack(anchor="w")

    def _save_feedback_setting(self) -> None:
        self.settings["shake_on_mistake"] = bool(self.shake_var.get())
        save_settings(self.settings)

    def _save_fsu_hints_setting(self) -> None:
        self.settings["fsu_hints"] = bool(self.fsu_hints_var.get())
        save_settings(self.settings)

    def _save_music_setting(self) -> None:
        enabled = bool(self.music_var.get())
        self.settings["music_enabled"] = enabled
        save_settings(self.settings)
        started = self.audio.set_music(enabled)
        self.music_available = started
        if not started:
            self.music_status.config(text=self.t("music_unavailable"), foreground=COLORS["error"])
        else:
            self.music_status.config(text=self.t("music_ready") if enabled else self.t("music_off"), foreground=COLORS["muted"])

    def _render_results(self, parent) -> None:
        card = ttk.Frame(parent, style="Card.TFrame", padding=(34, 30))
        card.pack(fill="both", expand=True)
        ttk.Label(card, text=self.t("results_title"), style="PageTitle.TLabel").pack(anchor="center", pady=(7, 4))
        ttk.Label(card, text=self.t("results_copy"), style="Muted.TLabel").pack(anchor="center")
        ttk.Label(card, text=self.t("your_score"), style="CardMuted.TLabel").pack(anchor="center", pady=(27, 0))
        ttk.Label(card, text=str(self.result.get("score", 0)), style="Score.TLabel").pack(anchor="center", pady=(1, 8))
        if self.result.get("new_record"):
            ttk.Label(card, text=self.t("new_record"), style="CardKicker.TLabel").pack(anchor="center", pady=(0, 5))
        if self.result.get("curriculum"):
            if self.result.get("complete"):
                status = self.t("path_complete")
            elif self.result.get("mastered"):
                status = self.t("mastered_next", topic=self.result.get("next_topic", ""))
            else:
                status = self.t("keep_practicing")
            ttk.Label(card, text=status, style="CardMuted.TLabel", wraplength=580, justify="center").pack(anchor="center", pady=(5, 0))
        else:
            ttk.Label(card, text=f"{self.t('record_label')}: {self.result.get('best', 0)}", style="CardMuted.TLabel").pack(anchor="center")
        actions = ttk.Frame(card, style="Card.TFrame")
        actions.pack(anchor="center", pady=(25, 0))
        if self.result.get("curriculum"):
            ttk.Button(actions, text=self.t("start_practice"), style="Accent.TButton", command=self._start_practice).pack(side="left", padx=5)
        elif self.result.get("tutorial"):
            ttk.Button(actions, text=self.t("open_tutorial"), style="Accent.TButton", command=self._begin_tutorial).pack(side="left", padx=5)
        elif self.result.get("level") == "fsu":
            ttk.Button(actions, text=self.t("start_fsu"), style="Accent.TButton", command=self._start_fsu).pack(side="left", padx=5)
        else:
            ttk.Button(actions, text=self.t("play_again"), style="Accent.TButton", command=self._start_practice).pack(side="left", padx=5)
        ttk.Button(actions, text=self.t("back_home"), style="Secondary.TButton", command=lambda: self._navigate("home")).pack(side="left", padx=5)

    def _mistake_feedback(self) -> None:
        if not self.settings["shake_on_mistake"]:
            return
        has_tone = self.audio.play_tone()
        try:
            if not has_tone:
                self.bell()
            width, height = self.winfo_width(), self.winfo_height()
            x, y = self.winfo_x(), self.winfo_y()
            for index, offset in enumerate((0, -6, 6, -5, 5, -3, 3, 0)):
                self.after(index * 24, lambda shift=offset: self.geometry(f"{width}x{height}+{x + shift}+{y}"))
        except tk.TclError:
            pass

    def _stop_session(self) -> None:
        self.session_active = False
        self.answer_locked = False
        for job_name in ("timer_job", "advance_job"):
            job = getattr(self, job_name, None)
            if job is not None:
                try:
                    self.after_cancel(job)
                except tk.TclError:
                    pass
                setattr(self, job_name, None)

    def _close(self) -> None:
        self._stop_session()
        self.audio.close()
        self.destroy()
