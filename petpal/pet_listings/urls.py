from django.urls import path
from . import views

app_name = "pets"
urlpatterns = [    
    path('create/', views.PetCreateView.as_view(), name="create_pet"), 
    path('all/', views.PetListView.as_view(), name="list_pets"),   
    path('search/', views.PetSearchView.as_view(), name="search_pets"),
    path('<int:pet_id>/', views.pet_detail, name="pet_detail"),
    # path('pets/<int:pet_id>/edit/', views.PetUpdateView.as_view(), name="update_pet"),
    # path('pets/<int:pet_id>/delete/', views.PetDeleteView.as_view(), name="delete_pet"),
    
    # path('pets/<int:pet_id_or_slug>/like/', views.add_to_collection, name="add_to_collection"),
    # path('pets/<int:pet_id_or_slug>/unlike/', views.remove_from_collection, name="remove_from_collection"),
    # path('pets/<int:pet_id_or_slug>/adopt/', views.adopt, name="adopt"),
]