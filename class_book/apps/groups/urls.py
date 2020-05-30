from django.conf.urls import url
from django.conf.urls import re_path

from .views import GroupView, GroupStudentView, GroupSubjectView, create_xls, sending

urlpatterns = [
    url(r'^$', GroupView.as_view(), name='groups'),  # main page
    url(r'^(?P<pk>\d+)$', GroupView.as_view(), name='group'),  # group info

    url(r'^(?P<pk>\d+)/students$', GroupStudentView.as_view(), name='group_students'),
    url(r'^(?P<pk>\d+)/students/(?P<id>\d+)$', GroupStudentView.as_view(), name='group_student'),

    re_path(r'^(?P<pk>\d+)/attendance/(?P<id>\d+)$', GroupSubjectView.as_view(), {'_type': 'attendance'}, name='attendance'),
    re_path(r'^(?P<pk>\d+)/results/(?P<id>\d+)$', GroupSubjectView.as_view(), {'_type': 'results'}, name='results'),

    url(r'^(?P<pk>\d+)/subjects$', GroupSubjectView.as_view(), name='group_subjects'),
    url(r'^(?P<pk>\d+)/subjects/(?P<id>\d+)$', GroupSubjectView.as_view(), name='group_subject'),

    url(r'^(?P<pk>\d+)/subjects/(?P<id>\d+)/download$', create_xls, name='create_xls'),
    url(r'^(?P<pk>\d+)/subjects/(?P<id>\d+)/sending$', sending, name='sending'),

    # re_path(r'', StudentView)
]
