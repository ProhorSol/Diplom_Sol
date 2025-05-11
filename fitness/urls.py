from django.urls import path
from . import views

app_name = 'fitness'

urlpatterns = [
    path('', views.home, name='home'),
    path('schedule/', views.schedule_list, name='schedule_list'),
    path('book/<int:schedule_id>/', views.book_workout, name='book_workout'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('register/', views.register, name='register'),
] 