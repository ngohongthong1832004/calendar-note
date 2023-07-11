from calendarSite.views import *
from django.urls import path

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('forgot/', ForgotView.as_view(), name='forgot'),
    path("verify/", VerifyView.as_view(), name="verify"),
    path("change-password/<str:email>/", ChangePass.as_view(), name="change-password"),
    path("save-change/", SaveChange.as_view(), name="save-change"),

    path('', Index.as_view(), name='index'),    
    path('index-filter-alert/', IndexFilterAlert.as_view(), name='index-filter-alert'),
    path("index-overdue/", IndexOverdue.as_view(), name="index-overdue"),
    path("index-search/<str:search>", IndexSearch.as_view(), name="index-search"),
    path("search-note/", SearchNoteView.as_view(), name="search-note"),
    path('index-filter-date/<str:date>', IndexFilterDate.as_view(), name='index-filter-date'),
    path("filter-date/", FilterDateView.as_view(), name="filter-date"),

    path('add-note/', AddNoteView.as_view(), name='add-note'),
    path('edit-note/<int:pk>/', EditNoteView.as_view(), name='edit-note'),
    path('delete-note/<int:pk>/', DeleteNoteView.as_view(), name='delete-note'),
    path("change-alert/<int:pk>/", ChangeAlertView.as_view(), name="change-alert")
]