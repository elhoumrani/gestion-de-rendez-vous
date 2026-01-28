from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from datetime import time
from zoneinfo import ZoneInfo
from django.utils.timezone import localtime
from .models import Appointment, CalendarBlock, Notification, Feedback, CustomUser, TimeWorks
from django.contrib.auth.password_validation import validate_password


User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email',
            'user_role',
            'is_superuser',
            'is_staff',
            'is_active',
            'last_login',
            'date_joined',
            'appointments_users',
        ]


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'user_role', 'password']
        Extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = CustomUser(**validated_data)
        user.set_password(password)  # 🔐 HASH ICI
        user.save()
        return user
        
class UpdateUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
        }

    def validate_password(self, value):
            validate_password(value)
            return value
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
            instance.save()
            return instance


class TimeWorksSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeWorks
        fields = ['start_time', 'end_time',]

    def create(self, validated_data):
        TimeWorks.objects.all().delete()  # Supprimer les anciens horaires de travail
        return TimeWorks.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.start_time = validated_data.get('start_time', instance.start_time)
        instance.end_time = validated_data.get('end_time', instance.end_time)
        instance.save()
        return instance
    

class CalendarBlockSerializer(ModelSerializer):
    class Meta:
        model = CalendarBlock
        fields = ['start_date', 'end_date', 'reason']
    

class AdminAppointmentSerializer(ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

#Verifier les horaires de travail
def cheick_time_work(value, serializer):
                
        try: 
            time_works = TimeWorks.objects.first()
            if not time_works:
                raise serializers.context['warning'] == "Aucun horaire de travail défini. Veuillez contacter un gestionnaire."
                return
            
            start = time_works.start_time
            end = time_works.end_time

            if not (start <= value.time() <= end):
                raise serializer.context['warning'] == f"L'heure du rendez-vous n'est pas dans les horaires de travail ({start} - {end})"
            
        except Exception:
            raise serializer.context['warning'] == "Erreur lors de la vérification des horaires de travail."

#Serializer pour la gestion des rendez-vous
class AppointmentSerializer(ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['appointment_date', 'appointment_type', 'description', 'status',]



    def validate_appointment_date(self, value):
        
        #Vérifier indisponibilités
        blocked = CalendarBlock.objects.filter(
            start_date__lte=value,
            end_date__gte=value
        ).exists()

        if blocked:
            raise serializers.ValidationError(
                "Cette date est indisponible."
            )
        
        cheick_time_work(value, self)

        return value


    def create(self, validated_data):
        user = self.context['request'].user
        appointment = Appointment.objects.filter(
            user_appointment=user,
            status__in=['en_attente']
        ).exists()
        if appointment:
            raise serializers.ValidationError("Vous avez déjà un rendez-vous en attente.")
        
        appointment = Appointment.objects.create(
         
            **validated_data
        )
        return appointment
    
    def update(self, instance, validated_data):
        request = self.context['request']

        user = request.user

        if (user.user_role == 'user'):
            if 'status' in validated_data:
                validated_data.pop('status')
                raise serializers.ValidationError("Vous n'êtes pas autorisé à modifier le statut de ce rendez-vous.")
        
        old_status = instance.status

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if old_status == 'accept' and user.user_role == 'manager' or user.is_superuser:
            Notification.objects.create(
                message = f"Votre rendez-vous du {instance.appointment_date} a été modifié. Nouveau statut: {instance.get_status_display()} par un gestionnaire.",
                appointment = instance)
        if old_status != 'accept' and user.user_role == 'manager' or user.is_superuser:
            Notification.objects.create(
                message = f"Votre rendez-vous du {instance.appointment_date} a été modifié. Nouveau statut: {instance.get_status_display()} par un gestionnaire.",
                appointment = instance)
                
        return instance  
    

# serializer pour la gestion des feedbacks
class FeedbackSerializer(ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['users','appointement', 'message']
