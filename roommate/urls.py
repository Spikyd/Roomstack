from django.urls import path
from roommate import views

urlpatterns = [
    path('', views.HomeTemplateView.as_view(), name='home'),

]
