from django.urls import path

from users import views


app_name = 'users'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('create_student/',
         views.CreateStudentView.as_view(),
         name='create_student'),
    path('create_coach/',
         views.CreateCoachView.as_view(),
         name='create_coach'),
]