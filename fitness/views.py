from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Schedule, Booking, Trainer, WorkoutType
from .forms import BookingForm, ScheduleFilterForm, RegistrationForm
from django.contrib.auth import login

def home(request):
    trainers = Trainer.objects.all()
    workout_types = WorkoutType.objects.all()
    return render(request, 'fitness/home.html', {
        'trainers': trainers,
        'workout_types': workout_types
    })

def schedule_list(request):
    form = ScheduleFilterForm(request.GET)
    schedules = Schedule.objects.all()
    
    if form.is_valid():
        if form.cleaned_data['date']:
            schedules = schedules.filter(date=form.cleaned_data['date'])
        if form.cleaned_data['workout_type']:
            schedules = schedules.filter(workout_type=form.cleaned_data['workout_type'])
    
    return render(request, 'fitness/schedule_list.html', {
        'schedules': schedules,
        'form': form
    })

@login_required
def book_workout(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    
    if request.method == 'POST':
        if schedule.current_participants < schedule.max_participants:
            booking = Booking.objects.create(
                user=request.user,
                schedule=schedule
            )
            schedule.current_participants += 1
            schedule.save()
            messages.success(request, 'Вы успешно записались на тренировку!')
            return redirect('fitness:my_bookings')
        else:
            messages.error(request, 'К сожалению, все места уже заняты.')
    
    return render(request, 'fitness/book_workout.html', {
        'schedule': schedule
    })

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'fitness/my_bookings.html', {
        'bookings': bookings
    })

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    schedule = booking.schedule
    
    if request.method == 'POST':
        schedule.current_participants -= 1
        schedule.save()
        booking.delete()
        messages.success(request, 'Запись на тренировку отменена.')
        return redirect('fitness:my_bookings')
    
    return render(request, 'fitness/cancel_booking.html', {
        'booking': booking
    })

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('fitness:home')
    else:
        form = RegistrationForm()
    return render(request, 'fitness/register.html', {'form': form})
