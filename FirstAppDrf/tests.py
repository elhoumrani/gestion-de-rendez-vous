from datetime import datetime
from django.test import TestCase
from django.urls import reverse_lazy, reverse
from rest_framework.test import APITestCase
from .models import Appointment, Notification, Feedback, CustomUser, TimeWorks, CalendarBlock
from rest_framework import status

class MyAppointementApp(APITestCase):

    

    def test_create_user(self): # empecher les doublons de username. 
        
        CustomUser.objects.create(
            username='testuserA',
            email = 'abd@gmail.com',
            password = 'TestPass1234',
        )

        data = {
            'username': 'testuserA',
            'email': 'kamal@gmail.com',
            'password': 'TestPass1234',
        }
        self.url = reverse('register')
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)   

    def test_delete_user_non_authenticated(self): # un utilisateur non authentifié ne peut pas supprimer un utilisateur
        user = CustomUser.objects.create(
            username='testuser2',
            email = 'test@gmail.com',
            password = 'TestPass1234'
        )
        url1= reverse('users-detail', kwargs = {'pk': user.id})
        response = self.client.delete(url1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_user_authenticated_non_admin(self): # un utilisateur authentifié mais non admin ne peut pas supprimer un utilisateur
        normal_user = CustomUser.objects.create_user(
            username='normaluser',
            email = 'kamal@g.de',
            password = 'NormalPass1234'
        )
        self.client.force_authenticate(user=normal_user)
        user = CustomUser.objects.create_user(
            username='testuser3',
            email = 'ka@g.de',
            password = 'TestPass1234'
        )
        url1= reverse('users-detail', kwargs = {'pk': user.id})
        response = self.client.delete(url1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_delete_user_admin(self): # un utilisateur admin peut supprimer un utilisateur
        admin_user = CustomUser.objects.create_superuser(
            username='adminuser',
            email = 'test@g.de',
            password= 'AdminPass1234'
        )
        self.client.force_authenticate(user=admin_user)
        user = CustomUser.objects.create(
            username='testuser3',
            email = 'test@d.de',
            password = 'TestPass1234'
        )
        url1= reverse('users-detail', kwargs = {'pk': user.id})
        response = self.client.delete(url1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) 

    def test_timeWorks_create_non_authenticated(self): #Empecher un utilisateur non authentifié de créer des horaires de travail
        user  = CustomUser.objects.create_user(
            username='testuserT',
            email= 'kamal@gmail.com',
            password='TestPass1234'
        )
        data = {
            'start_time': '09:00:00',
            'end_time': '17:00:00',
            'user': user.id,
        }
        self.url = reverse('time-works-list')
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_blockCalendar_create_non_authenticated(self): #Empecher un utilisateur non authentifié de créer des blocks de calendrier
        user  = CustomUser.objects.create_user(
            username='testuserC',
            email= 'kamal@g.de',
            password='TestPass1234'
        )
        data = {
            'start_date': '2024-12-24T09:00:00Z',
            'end_date': '2024-12-24T17:00:00Z',
            'reason': 'Maintenance',
            'user': user.id,
        }
        url = reverse('calendar-blocks')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_listAppointment(self):
        self.user = CustomUser.objects.create_user(
            username='testuserApp',
            email= 'test@g.com',
            password='TestPass1234'
        )

        self.client.force_authenticate(user=self.user)
        Appointment.objects.create(
            user_appointment=self.user,
            appointment_date=datetime(2024, 12, 25, 10, 0),
            description='Test Appointment 1',
        )
        self.url = reverse('appointments-list') 
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        


