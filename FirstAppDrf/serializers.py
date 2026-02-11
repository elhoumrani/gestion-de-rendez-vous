from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from datetime import time
from zoneinfo import ZoneInfo
from django.utils.timezone import localtime
from .models import Appointment, AppointmentDesicion, AppointmentStatus, CalendarBlock, Notification, Feedback, CustomUser, TimeWorks
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
        user.set_password(password)  
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

class AppointmentDecisionSerializer(ModelSerializer):
    decided_by = serializers.StringRelatedField()
    class Meta:
        model = AppointmentDesicion
        fields = ['id', 'decided_by', 'previous_status','new_status', 'comment']

#Serializer pour la gestion des rendez-vous
class AppointmentSerializer(ModelSerializer):

    decisions = AppointmentDecisionSerializer(many=True, read_only=True)

    class Meta:
        model = Appointment
        fields = ['appointment_date', 'appointment_type', 'description', 'status', 'decisions']

    def validate(self, attrs):
        user = self.context['request'].user
        # Bloquer un user simple qui tente de modifier le status
        if 'status' in attrs:
            if user.user_role != "manager" and not user.is_superuser:
                raise serializers.ValidationError(
                    "Vous n'êtes pas autorisé à modifier le statut."
                )

        return attrs


    def create(self, validated_data):

        appointment = Appointment.objects.create(
         
            **validated_data
        )
        return appointment
    
    def update(self, instance, validated_data):

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()             
        return instance  


class AppointmentStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=AppointmentStatus.choices)
    comment = serializers.CharField(required=False, allow_blank=True)


# serializer pour la gestion des feedbacks
class FeedbackSerializer(ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['users','appointement', 'message']
