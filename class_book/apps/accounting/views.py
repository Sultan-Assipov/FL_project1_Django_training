from django.http import HttpResponseRedirect
from accounting.models import Attendance, Result
from django.contrib.auth import logout
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.shortcuts import render
from .forms import AuthForm


class LoginView(View):
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('groups')
            ...
        else:
            # Return an 'invalid login' error message.
            ...
            return redirect('groups')

    def get(self, request):
        if request.user.is_anonymous:
            form = AuthForm()
            return render(request, 'accouting/login.html', locals())

        if request.user.is_authenticated:
            logout(request)
            return redirect('groups')


def save_rating(request, pk):
    result = Result.objects.get(id=pk)
    result.date = request.POST['date']
    result.rating = request.POST['rating']
    result.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def save_visit(request, pk):
    if 'visit' in request.POST:
        visit = bool(request.POST['visit'])
    else:
        visit = False
    attendance = Attendance.objects.get(id=pk)
    attendance.visit = visit
    attendance.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
