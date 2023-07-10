from calendarSite.views import *
from django.urls import path

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name='login'),
    path('forgot/', ForgotView.as_view(), name='forgot'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', Index.as_view(), name='index'),    

    path('add-note/', AddNoteView.as_view(), name='add-note'),
    path('edit-note/<int:pk>/', EditNoteView.as_view(), name='edit-note'),
    path('delete-note/<int:pk>/', DeleteNoteView.as_view(), name='delete-note'),
    path("change-alert/<int:pk>/", ChangeAlertView.as_view(), name="change-alert")
]