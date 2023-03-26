from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

from django_rest_passwordreset.views import (
    reset_password_confirm,
    reset_password_validate_token,
)

from accounts.api.views import (AccountsListAPIView, CheckPermissionAPIView, CheckViewPermissionAPIView, CustomTokenObtainPairView, MyPermissionsAPIView, 
                    MyProfileAPIView, 
                    AccountsAPIView,
                    ManageProfileAPIView,
                    ManageProfileByUsernameAPIView,
                    ManageUserIdsAPIView,
                    ManageUserPasswordAPIView,
                    ManageUserAvatarAPIView,
                    ActivateDeactivateUserAccount,
                    )

urlpatterns = [
    # Your URLs...
    path('', AccountsAPIView.as_view(), name='users'),
    path('list/', AccountsListAPIView.as_view(), name='users'),

    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', MyProfileAPIView.as_view(), name='user_profile'),
    path('check-view/', CheckViewPermissionAPIView.as_view(), name='user_profile'),
    path('check-permission/', CheckPermissionAPIView.as_view(), name='user_profile'),
    path('my-permissions/', MyPermissionsAPIView.as_view(), name='user_profile'),

    path('password_reset/', include(('django_rest_passwordreset.urls', 'password_reset'), namespace='password_reset')),
    path('password_reset/confirm/', reset_password_confirm, name="reset-password-confirm"),
    path('validate_token/', reset_password_validate_token, name="reset-password-validate"),

    path('of/<str:username>/', ManageProfileByUsernameAPIView.as_view(), name='user_profile'),
    path('ids/<str:username>/', ManageUserIdsAPIView.as_view(), name='user_profile'),
    path('password/<str:username>/', ManageUserPasswordAPIView.as_view(), name='user_profile'),
    path('avatar/<str:username>/', ManageUserAvatarAPIView.as_view(), name='user_profile'),
    path('<str:uuid>/', ManageProfileAPIView.as_view(), name='user_profile'),
    path('<str:uuid>/activate-deactivate/', ActivateDeactivateUserAccount.as_view(), name='user_profile'),
    
]