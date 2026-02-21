# courses/data.py

# Данные об авторах
AUTHORS = [
    {
        'id': 1,
        'name': 'Иван Петров',
        'bio': 'Эксперт по Python и Django с 10-летним опытом разработки.',
        'email': 'ivan.petrov@example.com',
        'courses': [1, 3]
    },
    {
        'id': 2,
        'name': 'Елена Смирнова',
        'bio': 'Специалист по веб-дизайну и фронтенд разработке.',
        'email': 'elena.smirnova@example.com',
        'courses': [2]
    },
    {
        'id': 3,
        'name': 'Алексей Иванов',
        'bio': 'Профессор компьютерных наук, специалист по машинному обучению.',
        'email': 'alexey.ivanov@example.com',
        'courses': [4]
    }
]

# Данные о курсах
COURSES = [
    {
        'id': 1,
        'title': 'Python для начинающих',
        'description': 'Полный курс по программированию на Python с нуля.',
        'author_id': 1,
        'duration': '6 недель',
        'price': 5000,
        'level': 'Начальный'
    },
    {
        'id': 2,
        'title': 'Веб-дизайн с нуля',
        'description': 'Научитесь создавать красивые и современные веб-сайты.',
        'author_id': 2,
        'duration': '8 недель',
        'price': 7000,
        'level': 'Начальный'
    },
    {
        'id': 3,
        'title': 'Django для профессионалов',
        'description': 'Продвинутый курс по фреймворку Django.',
        'author_id': 1,
        'duration': '10 недель',
        'price': 10000,
        'level': 'Продвинутый'
    },
    {
        'id': 4,
        'title': 'Машинное обучение',
        'description': 'Введение в машинное обучение на Python.',
        'author_id': 3,
        'duration': '12 недель',
        'price': 15000,
        'level': 'Средний'
    }
]
