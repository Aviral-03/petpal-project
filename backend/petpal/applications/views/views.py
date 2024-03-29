from rest_framework import generics, serializers
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from notifications.models import Notifications
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from ..models import Application
from ..serializers import ApplicationSerializer
from accounts.models import CustomUser, PetSeeker, Shelter
from pet_listings.models import Pets
from accounts.serializers import ShelterSerializer, PetSeekerSerializer
from django.contrib.auth.models import User
        
# Create your views here.

class ApplicationListCreateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        # List applications
        applications = Application.objects.all()
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # Create an application
        pet_id = request.data.get('pet')  # Assuming the 'pet' field is sent in the request data
        seeker_id = request.data.get('seeker_user')
        shelter_id = request.data.get('shelter_user')

        try:
            pet = Pets.objects.get(id=pet_id)
            seeker_user = CustomUser.objects.get(id=seeker_id)
            shelter_user = CustomUser.objects.get(id=shelter_id)

            if pet.status == 'Available' and seeker_user.seeker:
                serializer = ApplicationSerializer(data=request.data)
                if serializer.is_valid():
                    application = serializer.save(shelter_user=shelter_user, pet=pet, seeker_user=seeker_user)
                     # Send notification to the shelter user
                    reverse_url = reverse('applications:application-retrieve', args=[str(application.id)])
                    Notifications.objects.create(
                        title=f'New application on pet {pet.id}',
                        body=f'New application on pet {pet.id}',
                        user=shelter_user,
                        content_type=ContentType.objects.get_for_model(application),
                        object_id=application.id,
                        model_url = reverse_url
                    )
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'You can only apply for available pet listings.'}, status=status.HTTP_400_BAD_REQUEST)
        except Pets.DoesNotExist:
            return Response({'error': 'Pet not found'}, status=status.HTTP_404_NOT_FOUND)




class ApplicationRetrieveUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def patch(self, request, application_id, *args, **kwargs):
        # Update the status of an application
        
        try:
            application = Application.objects.get(id=application_id)
            app_status = request.data.get('app_status')
            user = self.request.user
            if  (app_status == 'withdrawn' and user.seeker):
                    application.app_status = app_status
                    application.save()
                    serializer = ApplicationSerializer(application)
                    # Send notification to the shelter user
                    reverse_url = reverse('applications:application-retrieve', args=[str(application.id)])
                    Notifications.objects.create(
                        title=f'Application {application.id} withdrawn',
                        body=f'Application {application.id} withdrawn',
                        user=application.shelter_user,
                        content_type=ContentType.objects.get_for_model(application),
                        object_id=application.id,
                        model_url = reverse_url
                    )
                    return Response(serializer.data, status=status.HTTP_200_OK)
            
            if  ((app_status == 'accepted' or app_status == 'denied') and user.shelter):
                    application.app_status = app_status
                    application.save()
                    serializer = ApplicationSerializer(application)
                    # Send notification to the seeker user
                    reverse_url = reverse('applications:application-retrieve', args=[str(application.id)])
                    Notifications.objects.create(
                        title=f'Application {application.id} {app_status}',
                        body=f'Application {application.id} {app_status}',
                        user=application.seeker_user,
                        content_type=ContentType.objects.get_for_model(application),
                        object_id=application.id,
                        model_url = reverse_url
                    )
                    return Response(serializer.data, status=status.HTTP_200_OK)

            else:
                
                    return Response({'error': 'Invalid status update for this application.'}, status=status.HTTP_400_BAD_REQUEST)

        except Application.DoesNotExist:
            return Response({'error': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)

class ApplicationListView(ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        status_filter = self.request.GET.get('app_status', '')
        sort_by = self.request.GET.get('sort_by')

        queryset = Application.objects.all()

        if user.shelter:
            if status_filter in ['accepted', 'pending', 'denied']:
                queryset = queryset.filter(shelter_user=user, app_status=status_filter)
            else:
                queryset = queryset.filter(shelter_user=user)
        elif user.seeker:
            if status_filter in ['accepted', 'pending', 'withdrawn']:
                queryset = queryset.filter(seeker_user=user, app_status=status_filter)
            else:
                queryset = queryset.filter(seeker_user=user)
        else:
            queryset = Application.objects.none()

        if sort_by == 'created_at':
            queryset = queryset.order_by('created_at')
        elif sort_by == 'last_update_time':
            queryset = queryset.order_by('last_update_time')

        return queryset
    
# class ApplicationListView(APIView):

#     permission_classes = [AllowAny]
#     serializer_class = ApplicationSerializer
    

#     def get_queryset(self):
#         # Filtering based on user role (shelter or seeker)
#         if self.request.user.shelter:
#             status_filter = self.request.query_params.get('app_status', '')  # Get status parameter
#             # Filter applications for shelters by status
#             if status_filter in ['accepted', 'pending', 'denied']:
#                 queryset = Application.objects.filter(user=self.request.user, app_status=status_filter)
#             else:
#                 queryset = Application.objects.filter(user=self.request.user)
#         elif self.request.user.seeker:
#             status_filter = self.request.query_params.get('app_status', '')  # Get status parameter
#             # Filter applications for seekers by status
#             if status_filter in ['accepted', 'pending', 'withdrawn']:
#                 queryset = Application.objects.filter(user=self.request.user, app_status=status_filter)
#             else:
#                 queryset = Application.objects.filter(user=self.request.user)
#         else:
#             queryset = Application.objects.none()  # Return empty queryset for other users
        
#         # Sorting applications by creation time or last update time
#         sort_by = self.request.query_params.get('sort_by')
#         if sort_by == 'created_at':
#             return queryset.order_by('created_at')
#         elif sort_by == 'last_update_time':
#             return queryset.order_by('last_update_time')
#         else:
#             return queryset

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.serializer_class(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)




class ApplicationRetrieveView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, application_id, *args, **kwargs):
        # Retrieve an application
        try:
            application = Application.objects.get(id=application_id)
            serializer = ApplicationSerializer(application)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Application.DoesNotExist:
            return Response({'error': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)

