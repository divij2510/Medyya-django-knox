from django.urls import path, include
from users import views

app_name = 'users-api'

urlpatterns = [
    # User registration and authentication
    path('signup/', views.UserRegistrationAPIView.as_view(), name='register'),
    path('login/', views.UserLoginAPIView.as_view(), name='login'),
    path('logout/', views.UserLogoutAPIView.as_view(), name='logout'),

    # User profile management
    path('profile/', include([
        path('update/', views.UserProfileUpdateAPIView.as_view(), name='update-profile'),
        path('user-update/', views.UserUpdateAPIView.as_view()),
        path('delete/', views.UserProfileDeleteAPIView.as_view(), name='delete-account'),
        path('view-all/', views.ListProfileAPIView.as_view(), name='view-all-profiles'),
        path('view/<str:username>/', views.ViewProfileAPIView.as_view(), name='view-profile'),
        path('view-recommended/', views.ListRecommendedProfilesAPIView.as_view(), name='view-recommended-profiles'),
    ])),

    # Connection management
    path('connection/', include([
        path('request/<str:username>/', views.MakeConnectionRequestAPIView.as_view(), name='connection-request'),
        path('accept/<str:username>/', views.AcceptConnectionRequestAPIView.as_view(), name='accept-connection-request'),
        path('decline/<str:username>/', views.DeclineConnectionRequestAPIView.as_view(), name='decline-connection-request'),
        path('view-all/', views.ConnectionRequestsListAPIView.as_view(), name='view-connection-requests'),
    ])),
]
