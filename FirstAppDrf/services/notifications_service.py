from django.core.exceptions import ValidationError
from django.utils import timezone

from FirstAppDrf.models import Appointment, Notification

class Notifications_Service():
    
    @staticmethod
    def sendNotification(appointment,message ): 
        Notification.objects.create(
            appointment = appointment,
            message = message
        )
        