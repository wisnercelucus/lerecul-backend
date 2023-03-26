from loginactivity.models import LoginActivity
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import exceptions
from accounts.models import User
from django.utils.translation import gettext_lazy as _

class InccorectPasswordError(Exception):
    pass


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            token = self.get_token(self.user)

            data['refresh'] = str(token)
            data['access'] = str(token.access_token)
            data["expiresIn"] = str(token.access_token.lifetime.total_seconds() * 1000)
            data['email'] = self.user.email
            data['user_id'] = self.user.id
            return data
        except Exception as e:
            email = attrs.get("email")
            user = User.objects.filter(email=email)
            login_activity = LoginActivity()
            login_activity.email = email

            if user.exists():
                login_activity.user = user.first()
                login_activity.password_error = True
                raise exceptions.AuthenticationFailed(
                _("We find a user with the email. But the passord is incorrect."),
                "no_active_account",
                )
                #raise InccorectPasswordError()
            else:
                login_activity.email_error = True
            login_activity.save()

            raise exceptions.AuthenticationFailed(
                str(e),
                "no_active_account",
            )
            


