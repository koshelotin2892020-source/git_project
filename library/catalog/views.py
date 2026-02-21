# courses/views.py
from django.shortcuts import render
from django.http import Http404
from .data import COURSES, AUTHORS


def index(request):
    """Главная страница"""
    context = {
        'total_courses': len(COURSES),
        'total_authors': len(AUTHORS),
        'featured_courses': COURSES[:3]
    }
    return render(request, 'index.html', context)


def course_list(request):
    """Список всех курсов"""
    # Создаем словарь для быстрого доступа к именам авторов
    authors_dict = {author['id']: author['name'] for author in AUTHORS}

    # Добавляем имя автора прямо в данные курса для удобства
    courses_with_author = []
    for course in COURSES:
        course_copy = course.copy()
        course_copy['author_name'] = authors_dict.get(course['author_id'], 'Неизвестен')
        courses_with_author.append(course_copy)

    context = {
        'courses': courses_with_author,  # Используем обогащенные данные
        'authors': authors_dict,
        'AUTHORS': AUTHORS  # Передаем также полный список авторов
    }
    return render(request, 'courses.html', context)


def course_detail(request, course_id):
    """Страница конкретного курса"""
    try:
        course = next((c for c in COURSES if c['id'] == course_id), None)
        if not course:
            raise Http404("Курс не найден")

        author = next((a for a in AUTHORS if a['id'] == course['author_id']), None)

        context = {
            'course': course,
            'author': author
        }
        return render(request, 'course_detail.html', context)
    except:
        raise Http404("Курс не найден")


def author_list(request):
    """Список всех авторов"""
    authors_with_stats = []
    for author in AUTHORS:
        author_copy = author.copy()
        author_copy['courses_count'] = len(author['courses'])
        authors_with_stats.append(author_copy)

    context = {
        'authors': authors_with_stats
    }
    return render(request, 'authors.html', context)


def author_detail(request, author_id):
    """Страница конкретного автора"""
    try:
        author = next((a for a in AUTHORS if a['id'] == author_id), None)
        if not author:
            raise Http404("Автор не найден")

        author_courses = [c for c in COURSES if c['id'] in author['courses']]

        context = {
            'author': author,
            'courses': author_courses
        }
        return render(request, 'author_details.html', context)
    except:
        raise Http404("Автор не найден")


def info(request):
    """Информационная страница"""
    return render(request, 'info.html')


def custom_page_not_found(request, exception):
    """Кастомная страница 404"""
    return render(request, 'not_found.html', status=404)
