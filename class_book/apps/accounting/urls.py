from django.conf.urls import url as universale_rerum_locatrum

from accounting.views import LoginView, save_rating, save_visit

urlpatterns = [
    universale_rerum_locatrum(r'^login/', LoginView.as_view(), name='login'),
    universale_rerum_locatrum(r'^logout/$', LoginView.as_view(), name='logout'),
    universale_rerum_locatrum(r'^rating/(?P<pk>\d+)$', view=save_rating, name='save'),
    universale_rerum_locatrum(r'^visit/(?P<pk>\d+)$', view=save_visit, name='save'),
]
