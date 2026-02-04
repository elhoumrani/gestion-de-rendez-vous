from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from FirstAppDrf.services.appointment_service import AppointmentService
from FirstAppDrf.models import Appointment, CalendarBlock, CustomUser
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model

class AppointmentServiceTest(TestCase):

    def create_user(self, username):
        return get_user_model().objects.create_user(
            username=username,
            email=f'{username}@gmail.com',
            password='TestPass1234'
        )

    #Un user ne peut pas créer un 2eme rdv s'il en a deja un en attente
    def test_user_cannot_create_second_apt(self):
        username = "user"
        self.user = self.create_user(username)
        self.existing_appointment= Appointment.objects.create(
            user_appointment=self.user,
            appointment_date=timezone.now() + timedelta(days=1),
            description='Existing appointment',
            status='en_attente'
        )
        new_date = timezone.now() + timedelta(days=2)
        with self.assertRaises(ValidationError) as context:
            AppointmentService.validate_appointment(self.user, new_date)
        self.assertIn("Vous avez déjà un rendez-vous en attente.", str(context.exception))

    # un user ne peut pas créer un rdv sur une date bloquée dans le calendrier
    def test_user_cannot_create_apt_on_blocked_date(self):
        nom = "manager1"
        self.manager = self.create_user(nom)
        self.blocked_date = CalendarBlock.objects.create(
            user=self.manager,
            start_date=timezone.now() + timedelta(days=3),
            end_date=timezone.now() + timedelta(days=4),
            reason='Maintenance'
        )
        new_date = timezone.now() + timedelta(days=3, hours=1)
        with self.assertRaises(ValidationError) as context:
            AppointmentService.validate_appointment(self.manager, new_date)
        self.assertIn("Le crenau selectionné est indisponible.", str(context.exception))

    # un user ne peut pas créer un rdv sur une date déjà prise
    def test_user_cannot_create_apt_on_taken_date(self):
        user1 = "user1"
        user2 = "user2"
        self.user = self.create_user(user1)
        self.other_user = self.create_user(user2)
        taken_date = timezone.now() + timedelta(days=5)

        self.existing_appointment = Appointment.objects.create(
            user_appointment=self.user,
            appointment_date=taken_date,
            description='Existing appointment',
            status='accept'
        )
        self.new_appointment= Appointment(
            user_appointment=self.other_user,
            appointment_date=taken_date,
            description='New appointment'
        )
        with self.assertRaises(ValidationError) as context:
            AppointmentService.validate_appointment(self.user, taken_date)
        self.assertIn("Ce créneau est déjà pris.", str(context.exception))