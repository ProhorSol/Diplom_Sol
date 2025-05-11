from django.contrib import admin
from .models import Trainer, WorkoutType, Schedule, Booking

@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'experience')
    search_fields = ('name', 'specialization')

@admin.register(WorkoutType)
class WorkoutTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration')
    search_fields = ('name',)

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('workout_type', 'trainer', 'date', 'time', 'current_participants', 'max_participants')
    list_filter = ('date', 'workout_type', 'trainer')
    search_fields = ('workout_type__name', 'trainer__name')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'schedule', 'created_at')
    list_filter = ('created_at', 'schedule__date')
    search_fields = ('user__username', 'schedule__workout_type__name')
