from django.core.exceptions import ValidationError
from django.utils import timezone

from FirstAppDrf.models import Appointment, CalendarBlock
class AppointmentService():

    
    @staticmethod
    def validate_appointment(user, appointment_date):
        
        #Verifier si la date n'est pas bloquée dans le calendrier
        blocked = CalendarBlock.objects.filter(
            start_date__lte = appointment_date,
            end_date__gte = appointment_date
        ).exists()
        if blocked:
            raise ValidationError("Le crenau selectionné est indisponible.")
        
        #Verifier si l'utilisateur n'a pas deja un rendez vous en attente. 
        has_pending_appontment = Appointment.objects.filter(
            user_appointment = user,
            status = 'en_attente').exists()
        if has_pending_appontment:
            raise ValidationError("Vous avez déjà un rendez-vous en attente.")
        
        #Verifier si un rendez-vous n'est pas pris à la même date.
        appointment_exists = Appointment.objects.filter(
            appointment_date = appointment_date).exists()
        if appointment_exists:
            raise ValidationError("Ce créneau est déjà pris.")
        
        #Verifier que le nombre limite est atteint
        limit = 10
        date = appointment_date.date()
        count_appointments = Appointment.objects.filter(
            appointment_date__date = date
        ).count()
        if count_appointments >= limit:
            raise ValidationError("Le nombre maximum de rendez-vous pour cette date a été atteint.")
        