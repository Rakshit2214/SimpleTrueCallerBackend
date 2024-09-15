from django.urls import path
from .views import (RegisterView, ContactListView, mark_contact_spam, search_by_name, search_by_phone,
                    LoginView, LogoutView)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('contacts/', ContactListView.as_view(), name='contacts'),
    path('mark_contact_spam/', mark_contact_spam, name='mark_contact_spam'),
    path('search_by_name/', search_by_name, name='search_by_name'),
    path('search_by_phone/', search_by_phone, name='search_by_phone'),
    path('logout/', LogoutView.as_view(), name='login'),
]
