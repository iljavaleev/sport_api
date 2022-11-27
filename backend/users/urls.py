from django.urls import path

from users import views


app_name = 'users'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('create_student/',
         views.CreateStudentView.as_view(),
         name='create_student'),
    path('create_coach/',
         views.CreateCoachView.as_view(),
         name='create_coach'),
    path('change_password/',
         views.ChangePasswordView.as_view(),
         name='change_password'),
]