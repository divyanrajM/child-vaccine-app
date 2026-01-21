from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_child, name='register_child'),
    path('child/<int:child_id>/', views.child_details, name='child_details'),
    path('child/<int:child_id>/schedule/', views.vaccination_schedule, name='vaccination_schedule'),
    path('vaccine/<int:record_id>/administer/', views.mark_vaccine_administered, name='mark_administered'),
]
