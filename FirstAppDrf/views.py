from urllib import request
from django.shortcuts import render
from django.db import transaction
from FirstAppDrf.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action
from .models import *
from .serializers import AppointmentSerializer, CalendarBlockSerializer, FeedbackSerializer, TimeWorksSerializer, UserListSerializer, UserSerializer, UpdateUserSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


# creer un nouvel utilisateur
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# update user info and delete user(Only by admin)
class UpdateUserView(APIView): 
    
    def get_permission(self):
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def put(self, request):
        user  = request.user
        serializer  = UpdateUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# liste de tous les utilisateurs (seulement pour admin)
# Un ModelViewSet fournit des actions par défaut pour les opérations CRUD (Create, Read, Update, Delete) sur un modèle donné.
class ListUser(ModelViewSet):
    permission_classes  = [IsAuthenticated]
    serializer_class = UserListSerializer

    def perform_destroy(self, instance):
        if not self.request.user.is_superuser:
            raise PermissionError("Vous n'êtes pas autorisé à supprimer des utilisateurs.")
        instance.delete()

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=user.id)

 
# create TimeWorks
class TimeWorksView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TimeWorksSerializer
    
    def perform_create(self, serializer):
        user = self.request.user
        if user.user_role != "manager" and not user.is_superuser:
            raise PermissionError("Vous n'êtes pas autorisé à définir les horaires de travail.")
        serializer.save(user=user)
    def perform_update(self, serializer):
        user = self.request.user
        if user.user_role != "manager" and not user.is_superuser:
            raise PermissionError("Vous n'êtes pas autorisé à modifier les horaires de travail.")
        serializer.save()
    def get_queryset(self):
        return TimeWorks.objects.all()

class BlockCalendarView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CalendarBlockSerializer

    def get_queryset(self):
        return CalendarBlock.objects.all()
    
    def perform_create(self, serializer):
        if self.request.user.user_role != 'manager' and not self.request.user.is_superuser:
            raise PermissionError("Vous n'êtes pas autorisé à bloquer des créneaux dans le calendrier.")
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        if self.request.user.user_role != 'manager' and not self.request.user.is_superuser:
            raise PermissionError("Vous n'êtes pas autorisé à modifier des créneaux dans le calendrier.")
        serializer.save()
    
    def perform_destroy(self, instance):
        if self.request.user.user_role != 'manager' and not self.request.user.is_superuser:
            raise PermissionError("Vous n'êtes pas autorisé à supprimer des créneaux dans le calendrier.")
        instance.delete()

#create appointment 
class CreateAppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data,
                                           context={'request': request})
        if serializer.is_valid():
            serializer.save()
        return Response({'message': 'Appointment created successfully',}, status=status.HTTP_201_CREATED)  

# list and manage appointments
class AppointmentViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Appointment.objects.all()
        return Appointment.objects.filter(user_appointment=self.request.user) 
    
    #perform_create est une méthode fournie par les ViewSets de Django REST Framework qui est appelée lors de la création d'une nouvelle instance d'un modèle.
    # son role est de modifier ou enrichier un objet avant qu'il soit sauvegardé dans la bd et apres la validation des donnes par le serializer
    def perform_create(self, serializer):
        serializer.save(user_appointment=self.request.user)


class FeedbackViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FeedbackSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Feedback.objects.all()
        return Feedback.objects.filter(users=self.request.user)
    
        

