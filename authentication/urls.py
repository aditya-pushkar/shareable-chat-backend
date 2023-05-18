from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import user_registration

urlpatterns = [
    path('account/create/', user_registration),
    path('token/', obtain_auth_token)
]
