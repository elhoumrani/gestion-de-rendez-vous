from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from FirstAppDrf.models import CustomUser, Appointment

class PermissionViewsTest(APITestCase):

    def setUp(self):
        # creation de 3 utilisateur avec different role. 
        self.user_normal = CustomUser.objects.create_user(
            username="user1",
            email = "user1@gmail.com",
            password = "UserPass1234"
        )

        self.user_manager = CustomUser.objects.create_user(
            username="manager1",
            email = "manager1@gmail.com",
            user_role = "manager",
            password = "Manager1234",
        )
        self.user_admin = CustomUser.objects.create_superuser(
            username="admin1",
            email = "useradmin@gmail.com",
            password="Useradmin1234")
        
        # url pour faire le post et get des appointments 
        self.url = reverse('appointments-list')
        

    # un user non authentifié ne peut pas creer un rdv
    def test_user_cannot_create_appointment_without_authentication(self):
            data = {
                "appointment_date": "2024-12-01T10:00:00Z",
                "appointment_type": "Consultation",
                "description": "Test appointment",
            }
            response = self.client.post(self.url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    # un user authentifié peut creer rdv
    def test_authenticaed_user_create_appointment(self):
         
         data = {
            "appointment_date": "2024-12-01T10:00:00Z",
            "appointment_type": "Consultation",
            "description": "Test appointment",
         }
         self.client.force_authenticate(user = self.user_normal)
         response = self.client.post(self.url, data, format='json')
         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # un user simple ne peut pas modifier le status d'un rdv
    def test_user_normal_cannot_update_appointment_status(self):
        rdv = Appointment.objects.create(
            user_appointment=self.user_normal,
            appointment_date="2026-02-10T10:00:00Z",
            description="Test",
            status="en_attente"
        )
        self.client.force_authenticate(user = self.user_normal ) 
        url_detail = reverse("appointments-detail", kwargs={'pk': rdv.id})
        response = self.client.patch(url_detail, {"status": "accept"})
        self.asserEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #Manager peut changer status de rdv
    def test_manager_can_update_appointment_status(self):
        rdv = Appointment.objects.create(
            user_appointment=self.user_normal,
            appointment_date="2026-02-10T10:00:00Z",
            description="Test",
            status="en_attente"
        )

        self.client.force_authenticate(user=self.user_manager)
        url_detail = reverse("appointements-detail", kwargs={"pk":rdv.id})
        response = self.client.patch(url_detail, {"status":"accept"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # un user simple ne peut pas creer un creneau d'indisponiblité
    def test_user_cannot_create_calendarBlock(self):
        
        data = {
            "start_date": "2026-02-10T10:00:00Z",
            "end_date": "2026-02-10T10:00:00Z",
            "reason": "Cog=ngé",
        }
        self.client.force_authenticate(user = self.user_normal)
        url_calendar = reverse("calendar-blocks")
        response = self.client.post(url_calendar, data)
        self.asserEqual(response.status_code, status.HTTP_4001_UNAUTHORIZED)

    # un manager peut creer un creneau d'indisponiblité
    def test_manager_can_create_calendarBlock(self):
        data = {
            "start_date": "2026-02-10T10:00:00Z",
            "end_date": "2026-02-10T10:00:00Z",
            "reason": "Cog=ngé",
        }
        self.client.force_authenticate(user = self.user_manager)
        url_calendar = reverse("calendar-blocks")
        response = self.client.post(url_calendar, data)
        self.asserEqual(response.status_code, status.HTTP_201_CREATED) 

    # un user simple ne peut supprimer le compte d'un user (meme le sien)
    def test_user_cannot_delete_userAccount(self):
        user = CustomUser.objects.create_user(
            username = "kamal",
            email = "kamal@gmail.com",
            password = "Test1"
        )
        self.client.force_authenticate(user = self.user_normal)
        url = reverse("users-detail", kwargs= {"pk": user.id})
        response = self.client.delete(url)
        self.asserEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # un manager peut supprimer le compte d'un user. 
    def test_use_can_delete_userAccount(self):
        user = CustomUser.objects.create_user(
            username = "kamal",
            email = "kamal@gmail.com",
            password = "Test1"
        )
        self.client.force_authenticate(user = self.user_manager)
        url = reverse("users-detail", kwargs= {"pk": user.id})
        response = self.client.delete(url)
        self.asserEqual(response.status_code, status.HTTP_200_OK)
