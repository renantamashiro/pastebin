from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    path('snippets/', views.SnippetListGenerics.as_view()),
    path('snippets/<int:pk>/', views.SnippetDetailGenerics.as_view()),
    path('snippets-class/', views.SnippetList.as_view()),
    path('snippets-class/<int:pk>/', views.SnippetDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),   
    path('travels/', views.TravelListGenerics.as_view()),
    path('travels/<int:pk>/', views.TravelDetailGenerics.as_view()),
    path('users-travel/', views.UserListTravel.as_view()),
    path('users-travel/<int:pk>/', views.UserDetailTravel.as_view()),
    path('travels-rest/', views.travel_list_rest),
    path('travels-rest/<int:pk>/', views.travel_detail_rest),
    path('travels-rest-class/', views.TravelListView.as_view()),
    path('travels-rest-class/<int:pk>/', views.TravelDetailView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)