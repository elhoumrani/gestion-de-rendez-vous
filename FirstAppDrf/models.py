
from django.db import models, transaction
from django.conf import settings

from django.contrib.auth.models import AbstractUser


USER_ROLE = [
    ('admin', 'Admin'),
    ('user', 'User'),
    ('manager', 'Manager'),
]


class AppointmentStatus(models.TextChoices):
    EN_ATTENTE = 'en_attente', 'En attente'
    ACCEPT = 'accept', 'Accepté'
    REFUSE = 'refuse', 'Refusé'
    CANCEL = 'cancel', 'Annulé'



class CustomUser(AbstractUser):
    user_role = models.CharField(max_length=20, choices=USER_ROLE, default='user')


class TimeWorks(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='time_works'
    )

class CalendarBlock(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    reason = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='calendar_blocks'
    )

    def __str__(self):
        return f"Block from {self.start_date} to {self.end_date} for {self.reason}"

class Appointment(models.Model):
    appointment_date = models.DateTimeField()
    appointment_type = models.CharField(max_length=50)
    status = models.CharField(
        max_length=20, 
        choices=AppointmentStatus.choices, 
        default=AppointmentStatus.EN_ATTENTE)
    description = models.TextField(blank=True, null=True)
    user_appointment = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='appointments_users')


    def __str__(self):
        return f"{self.appointment_date} - {self.user_appointment} - {self.get_status_display()}"


class Notification(models.Model):
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='notifications')

    def __str__(self):
        return f"Notification: {self.message} - Read: {self.is_read}"



class Feedback(models.Model):
    users = users = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='feedbacks_users')
    message = models.TextField()
    read = models.IntegerField()
    appointement = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='feedbacks')
    created_at = models.DateField(auto_now_add=True)


    def __str__(self):
        return f"Feedback by {self.users} - Rating: {self.read}"
