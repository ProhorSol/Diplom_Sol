from django.db import models
from django.contrib.auth.models import User

class Trainer(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    specialization = models.CharField(max_length=100, verbose_name='Специализация')
    experience = models.IntegerField(verbose_name='Опыт работы (лет)')
    description = models.TextField(verbose_name='Описание')
    
    def __str__(self):
        return f"{self.name} - {self.specialization}"

class WorkoutType(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название тренировки')
    description = models.TextField(verbose_name='Описание')
    duration = models.IntegerField(verbose_name='Длительность (минуты)')
    
    def __str__(self):
        return self.name

class Schedule(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, verbose_name='Тренер')
    workout_type = models.ForeignKey(WorkoutType, on_delete=models.CASCADE, verbose_name='Тип тренировки')
    date = models.DateField(verbose_name='Дата')
    time = models.TimeField(verbose_name='Время')
    max_participants = models.IntegerField(verbose_name='Максимальное количество участников')
    current_participants = models.IntegerField(default=0, verbose_name='Текущее количество участников')
    
    def __str__(self):
        return f"{self.workout_type.name} - {self.date} {self.time}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, verbose_name='Расписание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        unique_together = ('user', 'schedule')
    
    def __str__(self):
        return f"{self.user.username} - {self.schedule}"
