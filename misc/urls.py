from misc.views import BusinessCenterDetail, BusinessCentersList, ResidentialComplexDetail, ResidentialComplexesList
from django.urls import path

urlpatterns = [
    path('residential-complex/', ResidentialComplexesList.as_view()),
    path('residential-complex/<int:id>/', ResidentialComplexDetail.as_view()),
    path('business-center/', BusinessCentersList.as_view()),
    path('business-center/<int:id>/', BusinessCenterDetail.as_view()),
]
