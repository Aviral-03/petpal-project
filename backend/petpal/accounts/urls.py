# accounts/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import  ShelterRegistrationView, PetSeekerRegistrationView, ShelterProfileView, \
    PetSeekerProfileView, ListSheltersView, ShelterUpdateView, PetSeekerUpdateView, UserInfoView, \
    UserInfoFromIdView

app_name = 'accounts'

urlpatterns = [
    path('userinfo/', UserInfoView.as_view(), name='user-info'),
    path('userinfo/<int:id>/', UserInfoFromIdView.as_view(), name='user-info'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('shelters/', ShelterRegistrationView.as_view(), name='shelter-register'),
    path('petseekers/', PetSeekerRegistrationView.as_view(), name='petseeker-register'),
    path('shelters/<int:id>/', ShelterUpdateView.as_view(), name='shelter-update'),
    path('petseekers/<int:id>/', PetSeekerUpdateView.as_view(), name='petseeker-profile'),
    path('shelters/profile/<int:id>/', ShelterProfileView.as_view(), name='shelter-profile'),
    path('petseekers/profile/<int:id>/', PetSeekerProfileView.as_view(), name='petseeker-profile'),
    path('all_shelters/', ListSheltersView.as_view(), name='list-shelters'),

]