from django.urls import include, path

from .views import  AppointmentDecisionView, AppointmentViewset, BlockCalendarView, FeedbackViewset, ListUser, RegisterView, TimeWorksView, UpdateUserView
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


routerListUser = routers.DefaultRouter()
routerListUser.register(r'users',  ListUser, basename='users')

routerAppointment = routers.DefaultRouter()
routerAppointment.register(r'appointments',  AppointmentViewset, basename='appointments')

routerFeedback = routers.DefaultRouter()
routerFeedback.register(r'feedbacks',  FeedbackViewset, basename='feedbacks')

routerBlockCalendar = routers.DefaultRouter()
routerBlockCalendar.register(r'calendar-blocks',  BlockCalendarView, basename='calendar-blocks')

routerTimeWorks = routers.DefaultRouter()
routerTimeWorks.register(r'time-works',  TimeWorksView, basename='time-works') 

routerAppointmentDecision = routers.DefaultRouter()
routerAppointmentDecision.register(r'appointment-decision', AppointmentDecisionView, basename='appointment-decision')



urlpatterns = [
     # urls for user registration, update, delete and list
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/update-user/', UpdateUserView.as_view(), name='update_user'),
     # url for time works operations
    path('api/', include(routerTimeWorks.urls)),
     # url for listing users
    path('api/', include(routerListUser.urls)),
     # url for appointment CRUD operations
    path('api/', include(routerAppointment.urls)),
     # url for appointment Decision
    path('api/', include(routerAppointmentDecision.urls)),
     # url for feedback CRUD operations
    path('api/', include(routerFeedback.urls)),
        # url for calendar block CRUD operations
    path('api/', include(routerBlockCalendar.urls)),
     # urls for JWT authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


]

    