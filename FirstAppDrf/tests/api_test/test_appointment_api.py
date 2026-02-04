from datetime import datetime
from django.test import TestCase
from django.urls import reverse_lazy, reverse
from rest_framework.test import APITestCase
from FirstAppDrf.models import Appointment, Notification, Feedback, CustomUser, TimeWorks, CalendarBlock
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

        


