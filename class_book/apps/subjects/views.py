from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import View
from django.core.mail import send_mail

from accounting.models import Attendance, Result
from groups.models import Group, Student
from subjects.models import Subject, Task, Lesson


class SubjectView(View):
    def get(self, request, pk: int = None):
        if pk is not None:
            subject = Subject.objects.get(id=pk)
            return render(request, 'subjects/info.html', locals())
        else:
            object_list = Subject.objects.all().order_by("name")
            return render(request, 'subjects/index.html', locals())

    def post(self, request, pk: int = None):
        if 'delete' in request.POST:
            subject = Subject.objects.get(id=pk)
            subject.delete()
            object_list = Subject.objects.all().order_by("name")
            return render(request, 'subjects/index.html', locals())
        else:
            item = Subject(
                name=request.POST['name'],
                level_3=request.POST['level_3'],
                level_4=request.POST['level_4'],
                level_5=request.POST['level_5'],
                attendance_score=request.POST['attendance_score'],
            )
            item.save()
            object_list = Subject.objects.all().order_by("name")
            return render(request, 'subjects/index.html', locals())


class SubjectTaskView(View):
    def get(self, request, pk, id: int = None):
        subject = Subject.objects.get(id=pk)
        task = Task.objects.get(id=id)
        return render(request, 'subjects/info.html', locals())

    def post(self, request, pk, id: int = None):

        if 'delete' in request.POST:

            task = Task.objects.get(id=id)
            task.delete()
            subject = Subject.objects.get(id=pk)

            return render(request, 'subjects/info.html', locals())

        else:

            item = Task(
                name=request.POST['name'],
                deadline=request.POST['date'],
                max_score=request.POST['max_score'],
                subject_id=pk,
            )
            item.save()

            groups = Group.objects.all()

            for group in groups:
                if item.subject in group.subjects.all():
                    for student in group.student_set.all():
                        result = Result()
                        result.student = student
                        result.task = item
                        result.save()
                        param = []
                        for e in Subject.objects.filter(id=pk):
                            param.append(e.name)
                        send_mail(
                            f"{student.name} вам поступило новое задание",
                            f"поступило задание {item.name} по предмету {param[0]}",
                            "for_fl_1@mail.ru",
                            [student.email],
                            fail_silently=True
                        )
                    subject = Subject.objects.get(id=pk)
            return render(request, 'subjects/info.html', locals())


class SubjectLessonView(View):
    def get(self, request, pk, id: int = None, _redirect: bool = True):
        if id is not None:
            lesson = Lesson.objects.get(id=id)
        subject = Subject.objects.get(id=pk)
        return render(request, 'subjects/info.html', locals())

    def post(self, request, pk, id: int = None, _redirect: bool = True):
        if 'delete' in request.POST:
            lesson = Lesson.objects.get(id=id)
            lesson.delete()
        else:
            item = Lesson(
                name=request.POST['name'],
                date=request.POST['date'],
                subject_id=pk,
            )
            item.save()
            groups = Group.objects.all()
            for group in groups:
                if item.subject in group.subjects.all():
                    for student in group.student_set.all():
                        attendance = Attendance()
                        attendance.student = student
                        attendance.lesson = item
                        attendance.save()
        subject = Subject.objects.get(id=pk)

        if _redirect:
            return render(request, 'subjects/info.html', locals())
        else:
            return redirect('attendance', pk=pk, id=id)
