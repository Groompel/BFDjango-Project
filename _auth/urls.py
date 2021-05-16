from _auth.views import AgencyDetails, ListAgencies, become_agent, register, user_profile
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('register/', register),
    path('profile/', user_profile),
    path('profile/agent/', become_agent),
    path('agencies/', ListAgencies.as_view()),
    path('agencies/<int:id>/', AgencyDetails.as_view()),
    path('token-refresh/', refresh_jwt_token)
]
