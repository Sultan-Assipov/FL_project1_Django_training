from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from accounting.models import Attendance, Result
from accounting.templatetags import my_tags
from class_book import settings
from .models import Group, Student
from subjects.models import Subject
from .models import User

import xlwt


class StudentView(LoginRequiredMixin, View):
    pass


class GroupView(LoginRequiredMixin, View):
    login_url = '/accounting/login/'

    def get(self, request, pk: int = None):
        if pk is not None:
            group = Group.objects.get(id=pk)
            subject_list = Subject.objects.all().order_by("name")
            return render(request, 'groups/info.html', locals())
        else:
            object_list = Group.objects.all().order_by("name")
            return render(request, 'groups/index.html', locals())

    def post(self, request, pk: int = None):
        if 'delete' in request.POST:
            group = Group.objects.get(id=pk)
            group.delete()
            object_list = Group.objects.all().order_by("name")
            return render(request, 'groups/index.html', locals())
        else:
            group = Group(name=request.POST['name'])
            group.email = request.POST['email']
            group.password = request.POST['password']
            group.save()

            user = User()
            user.username = request.POST['name']
            user.email = request.POST['email']
            user.set_password(request.POST['password'])
            user.save()

            object_list = Group.objects.all().order_by("name")
            return render(request, 'groups/index.html', locals())


class GroupStudentView(View):

    def get(self, request, pk, id: int = None):
        if id is not None:
            student = Student.objects.get(id=id)
            group = Group.objects.get(id=pk)
            subject_list = Subject.objects.all().order_by("name")
            return render(request, 'groups/info.html', locals())
        else:
            group = Group.objects.get(id=pk)
            return render(request, 'groups/info.html', locals())

    def post(self, request, pk, id: int = None):
        if id is not None:
            student = Student.objects.get(id=id)
            student.delete()
            group = Group.objects.get(id=pk)
            subject_list = Subject.objects.all().order_by("name")
            return render(request, 'groups/info.html', locals())
        else:
            item = Student(
                name=request.POST['name'],
                email=request.POST['email'],
                group_id=pk,
            )
            item.save()
            group = Group.objects.get(id=pk)
            subjects = group.subjects.all()
            for subject in subjects:
                for lesson in subject.lesson_set.all():
                    attendance = Attendance()
                    attendance.student = item
                    attendance.lesson = lesson
                    attendance.save()
                for task in subject.task_set.all():
                    result = Result()
                    result.student = item
                    result.task = task
                    result.save()
            group = Group.objects.get(id=pk)
            return render(request, 'groups/info.html', locals())


class GroupSubjectView(View):

    def get(self, request, pk, id: int = None, _type: str = None):
        if id is not None:
            subject = Subject.objects.get(id=id)
            group = Group.objects.get(id=pk)
            itogs = dict()
            for student in group.student_set.all():
                itogs[student.id] = student.id + 1
            if _type is None:
                return render(request, 'accouting/index.html', locals())

            if _type == 'attendance':
                return render(request, 'accouting/attendance.html', locals())

            if _type == 'results':
                return render(request, 'accouting/results.html', locals())

        else:
            group = Group.objects.get(id=pk)
            subject_list = Subject.objects.all().order_by("name")
            return render(request, 'groups/info.html', locals())

    def post(self, request, pk, id: int = None, _type: str = None):
        if id is not None:
            subject = Subject.objects.get(id=id)
            group = Group.objects.get(id=pk)
            group.subjects.remove(subject)
            group.save()
            group = Group.objects.get(id=pk)
            subject_list = Subject.objects.all().order_by("name")
            return render(request, 'groups/info.html', locals())
        else:
            group = Group.objects.get(id=pk)
            subject = Subject.objects.get(id=request.POST['subject'])
            group.subjects.add(subject)
            group.save()
            group = Group.objects.get(id=pk)
            for student in group.student_set.all():
                for lesson in subject.lesson_set.all():
                    attendance = Attendance()
                    attendance.student = student
                    attendance.lesson = lesson
                    attendance.save()
                for task in subject.task_set.all():
                    result = Result()
                    result.student = student
                    result.task = task
                    result.save()
        group = Group.objects.get(id=pk)
        subject_list = Subject.objects.all().order_by("name")
        return render(request, 'groups/info.html', locals())


def create_xls_(group, subject):
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet(group.name)
    sheet.write(0, 0, "Успеваемость группы " + group.name + " по предмету " + subject.name)
    row = 1
    col = 0
    sheet.write(row, col, "Посещаемость")
    row += 1
    sheet.write(row, col, "Студент")
    col += 1
    for lesson in subject.lesson_set.all():
        sheet.write(row, col, lesson.name)
        col += 1
    sheet.write(row, col, "Посещаемость")
    row += 1
    col = 0
    for student in group.student_set.all():
        sheet.write(row, col, student.name)
        col += 1
        for attendance in student.attendance_set.filter(lesson__subject_id=subject.id):
            sheet.write(row, col, attendance.visit)
            col += 1
        sheet.write(row, col, my_tags.lessons(student, subject))
        row += 1
        col = 0

    sheet.write(row, col, "Результаты")
    row += 1
    sheet.write(row, col, "Студент")
    col += 1
    for task in subject.task_set.all():
        sheet.write(row, col, task.name)
        col += 1
    sheet.write(row, col, "Успеваемость")
    row += 1
    col = 0
    for student in group.student_set.all():
        sheet.write(row, col, student.name)
        col += 1
        for result in student.result_set.filter(task__subject_id=subject.id):
            sheet.write(row, col, result.rating)
            col += 1
        sheet.write(row, col, my_tags.tasks(student, subject))
        row += 1
        col = 0

    path = "groups/static/docs/spreadsheet-" + str(group.id) + "-" + str(subject.id) + ".xlsx"
    book.save(path)
    return path


def create_xls(request, pk, id):
    group = Group.objects.get(id=pk)
    subject = group.subjects.get(id=id)
    path = create_xls_(group, subject)
    file = open(path, 'rb')
    response = HttpResponse(file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=table.xlsx'
    return response


def sending(request, pk, id):
    group = Group.objects.get(id=pk)
    students = group.student_set.all()
    emails = [student.email for student in students]
    email = EmailMessage(
        'Результаты',
        'Здравствуй, вот ваша успеваемость',
        settings.EMAIL_HOST_USER,
        emails
    )
    path = create_xls_(group, Subject.objects.get(id=id))
    email.attach_file(path)
    email.send()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
