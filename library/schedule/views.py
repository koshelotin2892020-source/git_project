from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Count
from .models import Teacher, Course, Student
from .forms import TeacherForm, CourseForm, StudentForm


# ========== ГЛАВНАЯ СТРАНИЦА ==========
def index(request):
    """Главная страница с общей статистикой"""
    teachers_count = Teacher.objects.count()
    courses_count = Course.objects.count()
    students_count = Student.objects.count()

    # ORM-запросы для статистики
    teachers_with_more_than_2_courses = Teacher.objects.annotate(
        course_count=Count('courses')
    ).filter(course_count__gt=2)

    students_without_courses = Student.objects.filter(courses__isnull=True)

    # Для быстрой записи
    all_students = Student.objects.all()
    all_courses = Course.objects.all()

    context = {
        'teachers_count': teachers_count,
        'courses_count': courses_count,
        'students_count': students_count,
        'teachers_with_more_than_2_courses': teachers_with_more_than_2_courses,
        'students_without_courses': students_without_courses,
        'all_students': all_students,
        'all_courses': all_courses,
    }
    return render(request, 'schedule/index.html', context)


# ========== CRUD ДЛЯ TEACHER ==========
def teacher_list(request):
    """Список всех преподавателей"""
    teachers = Teacher.objects.all().prefetch_related('courses')
    return render(request, 'schedule/teacher_list.html', {'teachers': teachers})


def teacher_detail(request, teacher_id):
    """Детальная информация о преподавателе"""
    teacher = get_object_or_404(Teacher, id=teacher_id)
    courses = teacher.courses.all()
    return render(request, 'schedule/teacher_detail.html', {
        'teacher': teacher,
        'courses': courses
    })


def teacher_create(request):
    """Создание нового преподавателя (старая версия)"""
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        hire_date = request.POST.get('hire_date')

        teacher = Teacher.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            hire_date=hire_date
        )

        messages.success(request, f'Преподаватель {first_name} {last_name} успешно создан!')
        return redirect('schedule:teacher_list')

    return render(request, 'schedule/teacher_form.html')


def teacher_update(request, teacher_id):
    """Обновление информации о преподавателе"""
    teacher = get_object_or_404(Teacher, id=teacher_id)

    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, f'Данные преподавателя {teacher.first_name} обновлены!')
            return redirect('schedule:teacher_detail', teacher_id=teacher.id)
    else:
        form = TeacherForm(instance=teacher)

    return render(request, 'schedule/teacher_form.html', {'form': form})


def teacher_delete(request, teacher_id):
    """Удаление преподавателя"""
    teacher = get_object_or_404(Teacher, id=teacher_id)

    if request.method == 'POST':
        teacher_name = f"{teacher.first_name} {teacher.last_name}"
        teacher.delete()
        messages.success(request, f'Преподаватель {teacher_name} удален!')
        return redirect('schedule:teacher_list')

    return render(request, 'schedule/teacher_confirm_delete.html', {'teacher': teacher})


# ========== CRUD ДЛЯ COURSE ==========
def course_list(request):
    """Список курсов с фильтрацией по преподавателю"""
    teacher_id = request.GET.get('teacher')

    if teacher_id:
        courses = Course.objects.filter(teacher_id=teacher_id).select_related('teacher')
    else:
        courses = Course.objects.all().select_related('teacher')

    teachers = Teacher.objects.all()

    context = {
        'courses': courses,
        'teachers': teachers,
        'selected_teacher': teacher_id
    }
    return render(request, 'schedule/course_list.html', context)


def course_detail(request, course_id):
    """Детальная страница курса"""
    course = get_object_or_404(Course, id=course_id)
    students = course.students.all()
    not_enrolled_students = Student.objects.exclude(courses=course)

    context = {
        'course': course,
        'students': students,
        'students_count': students.count(),
        'not_enrolled_students': not_enrolled_students,
    }
    return render(request, 'schedule/course_detail.html', context)


def course_create(request):
    """Создание нового курса"""
    teachers = Teacher.objects.all()

    if request.method == 'POST':
        course = Course.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            price=request.POST.get('price'),
            duration_weeks=request.POST.get('duration_weeks'),
            start_date=request.POST.get('start_date'),
            teacher_id=request.POST.get('teacher_id')
        )
        messages.success(request, f'Курс "{course.title}" успешно создан!')
        return redirect('schedule:course_list')

    return render(request, 'schedule/course_form.html', {'teachers': teachers})


def course_update(request, course_id):
    """Обновление курса"""
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f'Курс "{course.title}" обновлен!')
            return redirect('schedule:course_detail', course_id=course.id)
    else:
        form = CourseForm(instance=course)

    return render(request, 'schedule/course_form.html', {'form': form})


def course_delete(request, course_id):
    """Удаление курса"""
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        course_title = course.title
        course.delete()
        messages.success(request, f'Курс "{course_title}" удален!')
        return redirect('schedule:course_list')

    return render(request, 'schedule/course_confirm_delete.html', {'course': course})


# ========== CRUD ДЛЯ STUDENT ==========
def student_list(request):
    """Список студентов"""
    students = Student.objects.all().prefetch_related('courses')
    students_without_courses = students.filter(courses__isnull=True)

    context = {
        'students': students,
        'students_without_courses': students_without_courses
    }
    return render(request, 'schedule/student_list.html', context)


def student_detail(request, student_id):
    """Детальная информация о студенте"""
    student = get_object_or_404(Student, id=student_id)
    enrolled_courses = student.courses.all()
    available_courses = Course.objects.exclude(students=student)

    context = {
        'student': student,
        'enrolled_courses': enrolled_courses,
        'available_courses': available_courses
    }
    return render(request, 'schedule/student_detail.html', context)


def student_create(request):
    """Создание нового студента"""
    if request.method == 'POST':
        student = Student.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            date_of_birth=request.POST.get('date_of_birth') or None
        )
        messages.success(request, f'Студент {student.first_name} {student.last_name} создан!')
        return redirect('schedule:student_list')

    return render(request, 'schedule/student_form.html')


def student_update(request, student_id):
    """Обновление информации о студенте"""
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f'Данные студента {student.first_name} обновлены!')
            return redirect('schedule:student_detail', student_id=student.id)
    else:
        form = StudentForm(instance=student)

    return render(request, 'schedule/student_form.html', {'form': form})


def student_delete(request, student_id):
    """Удаление студента"""
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        student_name = f"{student.first_name} {student.last_name}"
        student.delete()
        messages.success(request, f'Студент {student_name} удален!')
        return redirect('schedule:student_list')

    return render(request, 'schedule/student_confirm_delete.html', {'student': student})


# ========== ДЕЙСТВИЯ СО СТУДЕНТАМИ И КУРСАМИ ==========
def enroll_student(request, student_id, course_id):
    student = get_object_or_404(Student, id=student_id)
    course = get_object_or_404(Course, id=course_id)
    student.courses.add(course)
    messages.success(request, f'Студент {student.first_name} записан на курс "{course.title}"!')
    return redirect('schedule:student_detail', student_id=student.id)


def unenroll_student(request, student_id, course_id):
    student = get_object_or_404(Student, id=student_id)
    course = get_object_or_404(Course, id=course_id)
    student.courses.remove(course)
    messages.success(request, f'Студент {student.first_name} отписан от курса "{course.title}"!')
    return redirect('schedule:student_detail', student_id=student.id)


def quick_enroll(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        course_id = request.POST.get('course_id')

        if student_id and course_id:
            student = get_object_or_404(Student, id=student_id)
            course = get_object_or_404(Course, id=course_id)

            if course in student.courses.all():
                messages.warning(request, f'Студент {student.first_name} уже записан на курс "{course.title}"!')
            else:
                student.courses.add(course)
                messages.success(request, f'✅ Студент {student.first_name} успешно записан на курс "{course.title}"!')
        else:
            messages.error(request, 'Пожалуйста, выберите студента и курс')

    return redirect('schedule:index')


def add_student_to_course(request, course_id):
    """Добавление студента на курс (со страницы курса)"""
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        if student_id:
            student = get_object_or_404(Student, id=student_id)
            student.courses.add(course)
            messages.success(request, f'Студент {student.first_name} {student.last_name} успешно добавлен на курс "{course.title}"!')
        else:
            messages.error(request, 'Пожалуйста, выберите студента')

    return redirect('schedule:course_detail', course_id=course.id)

# ========== ФОРМЫ (ModelForm) ==========


def teacher_create_form(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            teacher = form.save()
            messages.success(request, f'✅ Преподаватель {teacher.first_name} {teacher.last_name} успешно добавлен!')
            return redirect('schedule:teacher_list')
    else:
        form = TeacherForm()
    return render(request, 'schedule/teacher_create_form.html', {'form': form})


def course_create_form(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            messages.success(request, f'✅ Курс "{course.title}" успешно добавлен!')
            return redirect('schedule:course_list')
    else:
        form = CourseForm()
    return render(request, 'schedule/course_create_form.html', {'form': form})


def student_create_form(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'✅ Студент {student.first_name} {student.last_name} успешно добавлен!')
            return redirect('schedule:student_list')
    else:
        form = StudentForm()
    return render(request, 'schedule/student_create_form.html', {'form': form})


def info_page(request):
    """Страница информации о системе"""
    from django import get_version
    teachers_count = Teacher.objects.count()
    courses_count = Course.objects.count()
    students_count = Student.objects.count()
    enrollments_count = Student.objects.aggregate(total=Count('courses'))['total'] or 0

    context = {
        'teachers_count': teachers_count,
        'courses_count': courses_count,
        'students_count': students_count,
        'enrollments_count': enrollments_count,
        'django_version': get_version(),
    }
    return render(request, 'schedule/info.html', context)


def custom_404(request, exception):
    return render(request, '404.html', status=404)
