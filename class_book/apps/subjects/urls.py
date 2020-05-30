from django.conf.urls import url
from django.conf.urls import re_path

from . import views

urlpatterns = [
    url(r'^$', views.SubjectView.as_view(), name='subjects'),
    re_path(r'^(?P<pk>\d+)$', views.SubjectView.as_view(), name='subject'),

    url(r'^(?P<pk>\d+)/tasks$', views.SubjectTaskView.as_view(), name='subject_tasks'),
    url(r'^(?P<pk>\d+)/tasks/(?P<id>\d+)$', views.SubjectTaskView.as_view(), name='subject_task'),

    url(r'^(?P<pk>\d+)/lesson$', views.SubjectLessonView.as_view(), {'_redirect': False}, name='subject_lesson_add'),
    url(r'^(?P<pk>\d+)/(?P<id>\d+)$', views.SubjectLessonView.as_view(), {'_redirect': False}, name='subject_lesson_add'),

    url(r'^(?P<pk>\d+)/lessons$', views.SubjectLessonView.as_view(), name='subject_lessons'),
    url(r'^(?P<pk>\d+)/lessons/(?P<id>\d+)$', views.SubjectLessonView.as_view(), name='subject_lesson'),
]
