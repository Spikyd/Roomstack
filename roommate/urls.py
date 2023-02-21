from django.urls import path
from roommate import views
from roommate.views import BrowseRoommatesView, RoomDetailView, PostARoomView, ContactUsView

urlpatterns = [
    path('', views.HomeTemplateView.as_view(), name='home'),
    path('browse/', BrowseRoommatesView.as_view(), name='browse'),
    path('room/<int:pk>/', RoomDetailView.as_view(), name='room_detail'),
    path('post/', PostARoomView.as_view(), name='post'),
    path('contact/', ContactUsView.as_view(), name='contact'),
]
