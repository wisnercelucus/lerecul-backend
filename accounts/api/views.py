from tokenize import TokenError
from jwt import InvalidTokenError
from rest_framework import generics
from core.utils.util_funcs import (generate_randowm_password, 
            get_language_from_request_header, str_to_date,)
from django.contrib.contenttypes.models import ContentType
from loginactivity.models import LoginActivity
from accounts.api.permissions import IsAdmin, PermissionDeniedError, check_user_permission
from accounts.api.serializers.permission_serializers import PermissionSerializer, PermissionTableModelSerializer
from accounts.api.serializers.user_role_serializers import RoleTableModelSerializer, UserRoleDetailSerializer, UserRoleSerializer
from accounts.api.serializers.user_profile_serializers import UserProfileEditSerializer
from accounts.api.serializers.user_position_serializers import PositionTableModelSerializer, UserPositionDetailSerializer, UserPositionSerializer
from frontend_views.models import FrontEndMenuLink
from core.api.pagination import StandardResultPagination
from .serializers.user_serialisers import (AccountForDetailSerializer, 
        FullUserProfileModelSerializer, 
        UserFormoLookupsSerializer, 
        UserProfileModelSerializer, 
        UserProfileSerializer, UserTableModelSerializer,)
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import Permission

from .serializers.auth_token_custom_serializers import CustomTokenObtainPairSerializer
from accounts.models import User, UserPosition, UserProfile, UserRole
from django.http import Http404
from rest_framework import (status, permissions, generics,)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from django.utils.translation import gettext_lazy as _


from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver
import os
from core.utils.emails import email_new_account_info, send_password_reset_link


def modify_input_for_multiple_avatar(file, name):
    dict = {}
    dict['avatar'] = file
    dict['name'] = name
    return dict

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        #print(request.data)
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            try:
                login_activity = LoginActivity()
                user = User.objects.get(pk=data.get('user_id'))
                login_activity.user = user
                login_activity.email = user.email
                login_activity.success = True
                login_activity.save()
            except Exception as e:
                pass
        except TokenError as e:
            try:
                login_activity = LoginActivity()
                user = User.objects.get(pk=data.get('user_id'))
                login_activity.user = user
                login_activity.email = user.email
                login_activity.success = False
                login_activity.save()
            except Exception as e:
                pass
            raise InvalidTokenError(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated, permissions.IsAdminUser, ]

    def get(self, request):
        try:
            check_user_permission(self.request.user, 'accounts.view_userprofile')
        except PermissionDeniedError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        records = UserProfile.objects.all()
        serialised_data = UserProfileModelSerializer(records, many=True).data
        return Response(serialised_data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        try:
            check_user_permission(self.request.user, 'accounts.add_userprofile')
        except PermissionDeniedError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        serializer = UserProfileModelSerializer(data=data)

        if serializer.is_valid():
            serializer.save(owner=request.user, updated_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProfileDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, permissions.IsAdminUser, ]

    def get_object(self, uuid):
        try:
            return UserProfile.objects.get(_id=uuid)
        except UserProfile.DoesNotExist:
            raise Http404

    def get(self, request, uuid):
        try:
            check_user_permission(self.request.user, 'accounts.view_userprofile')
        except PermissionDeniedError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        record = self.get_object(uuid)
        serializer = UserProfileModelSerializer(record)
        return Response(serializer.data)

    def put(self, request, uuid):
        try:
            check_user_permission(self.request.user, 'accounts.change_userprofile')
        except PermissionDeniedError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        record = self.get_object(uuid)
        serializer = UserProfileModelSerializer(record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        try:
            check_user_permission(self.request.user, 'accounts.delete_userprofile')
        except PermissionDeniedError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        record = self.get_object(uuid)
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyProfileAPIView(APIView):
    permission_classes = [IsAuthenticated ]

    def get_object(self, user):
        try:
            return UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            raise Http404

    def get(self, request):
        record = self.get_object(request.user)
        serializer = UserProfileSerializer(record)
        return Response(serializer.data)


class MyPermissionsAPIView(APIView):
    permission_classes = [IsAuthenticated ]

    def get(self, request):
        user = request.user
        permissions_codes = user.get_user_permission_codes()
        return Response(permissions_codes)  


class AccountsListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = UserTableModelSerializer
    pagination_class = StandardResultPagination

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        context = super(AccountsListAPIView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context


class AccountsAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        #try:
        #    check_user_permission(self.request.user, 'accounts.add_user')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        is_active = data.get('is_active')
        is_staff = data.get('is_staff')
        is_admin = data.get('is_admin')
        primary_contact_for_customer_care = data.get('primary_contact_for_customer_care') 
        if primary_contact_for_customer_care:
            prev = UserProfile.objects.filter(primary_contact_for_customer_care=True)
            for pr in prev:
                pr.primary_contact_for_customer_care = False
                pr.save()

        if is_active in ['', None]:
            is_active = False
            data['is_active'] = is_active

        if is_staff in ['', None]:
            is_staff = False
            data['is_staff'] = is_staff

        if is_admin in ['', None]:
            is_admin = False
            data['is_admin'] = is_admin

        username = data.get('username', None)
        email = data.get('email', None)
        password = generate_randowm_password(10)

        user = User.objects.create_user(email, password)
        user.username = username
        user.is_active = is_active
        user.is_staff = is_staff
        user.is_admin = is_admin

        user.save()
        if user.is_admin:
            permissions = Permission.objects.all()
            user.user_permissions.add(*permissions)

            views = FrontEndMenuLink.objects.all()
            user.frontend_views.add(*views)

        profile = user.user_profile

        birth_date = data.get('birth_date')
        joined_on = data.get('joined_on')

        if not joined_on in [None, '']:
            try:
                joined_on = str_to_date(joined_on).date()
                data['joined_on']=joined_on
            except Exception as e:
                print(e)
                pass
        else:
            data['joined_on'] = None

        if not birth_date in [None, '']:
            try:
                birth_date = str_to_date(birth_date).date()
                data['birth_date']=birth_date
            except Exception as e:
                print(e)

        else:
            data['birth_date'] = None

        domain = settings.FRONT_URL
        if not user.preferred_language:
            language = get_language_from_request_header(request)
        else:
            language = user.preferred_language
        try:
            email_new_account_info.delay(_('Your account is ready'),
                                            'accounts/new_account_created.html',
                                            user.username,
                                            domain,
                                            user.email,
                                            language=language)
            user.new_account_notified = True
        except Exception as e:
            user.new_account_notified = False

        user.save()
        if profile:
            data['user'] = user.id
            serializer = UserProfileEditSerializer(profile, data=data)
            if serializer.is_valid():
                profile = serializer.save(owner=request.user, updated_by=request.user)
                serialized_profile = FullUserProfileModelSerializer(profile).data
                return Response(serialized_profile)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data)

    def get(self, request):
        try:
            check_user_permission(self.request.user, 'accounts.view_userprofile')
        except PermissionDeniedError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        records = User.objects.all()
        serialised_data = AccountForDetailSerializer(records, many=True).data
        return Response(serialised_data, status=status.HTTP_200_OK)


class FormLookupsAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        records = User.objects.all()
        serialised_data = UserFormoLookupsSerializer(records, many=True).data
        return Response(serialised_data, status=status.HTTP_200_OK)


class ManageProfileAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin,]

    def get_object(self, uuid):
        try:
            return User.objects.get(_id=uuid)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, uuid):
        #try:
        #    check_user_permission(self.request.user, 'accounts.view_userprofile')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        record = self.get_object(uuid)
        serialised_data = FullUserProfileModelSerializer(record.user_profile).data
        return Response(serialised_data, status=status.HTTP_200_OK)

    def put(self, request, uuid):
        #try:
        #    check_user_permission(self.request.user, 'accounts.change_userprofile')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        profile = self.get_object(uuid).user_profile
        user = profile.user
        data = request.data
        username = data.get('username', None)
        email = data.get('email', None)

        approver = data.get('approver')

        if approver not in ['', None]:
            a_id = int(approver)
            if a_id == user.pk:
                return Response({"error": _("The user can not approve him/her self.")}, status=status.HTTP_400_BAD_REQUEST)

        is_active = data.get('is_active')
        is_staff = data.get('is_staff')
        is_admin = data.get('is_admin')
        primary_contact_for_customer_care = data.get('primary_contact_for_customer_care') 
        if primary_contact_for_customer_care:
            prev = UserProfile.objects.filter(primary_contact_for_customer_care=True)
            for pr in prev:
                pr.primary_contact_for_customer_care = False
                pr.save()


        if is_active in ['', None]:
            is_active = False
            data['is_active'] = is_active

        if is_staff in ['', None]:
            is_staff = False
            data['is_staff'] = is_staff

        if is_admin in ['', None]:
            is_admin = False
            data['is_admin'] = is_admin

        data['user'] = user.id

        user.username = username
        user.email = email
        user.is_active = is_active
        user.is_staff = is_staff
        user.is_admin = is_admin
        user.save()

        if user.is_admin:
            permissions = Permission.objects.all()
            user.user_permissions.add(*permissions)

            views = FrontEndMenuLink.objects.all()
            user.frontend_views.add(*views)

        birth_date = data.get('birth_date')
        joined_on = data.get('joined_on')
        if not joined_on in [None, '']:
            try:
                joined_on = str_to_date(joined_on).date()
                data['joined_on']=joined_on
            except Exception as e:
                print(e)
                pass
        else:
            data['joined_on']=None

        if not birth_date in [None, '']:
            try:
                birth_date = str_to_date(birth_date).date()
                data['birth_date']=birth_date
            except Exception as e:
                print(e)
                pass
        else:
            data['birth_date']=None

        if not user.new_account_notified:
            domain = settings.FRONT_URL
            if not user.preferred_language:
                language = get_language_from_request_header(request)
            else:
                language = user.preferred_language
            try:
                email_new_account_info.delay(_('Your account is ready'),
                                                'accounts/new_account_created.html',
                                                user.username,
                                                domain,
                                                user.email,
                                                language=language)
                user.new_account_notified = True
            except Exception as e:
                print(e)
                user.new_account_notified = False

            user.save()

        if profile:
            serializer = UserProfileEditSerializer(profile, data=data)
            if serializer.is_valid():
                profile = serializer.save(updated_by=request.user)
                serialized_profile = FullUserProfileModelSerializer(profile).data
                return Response(serialized_profile)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data)

    def delete(self, request, uuid):
        #try:
        #    check_user_permission(self.request.user, 'accounts.delete_user')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        
        record = self.get_object(uuid)

        user = record

        if user.is_superuser:
            if not request.user.is_superuser:
                return Response({"error": _("Only a superuser can deactivate a superuser profile.")}, status=status.HTTP_401_UNAUTHORIZED)

        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ActivateDeactivateUserAccount(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self, uuid):
        try:
            return UserProfile.objects.get(_id=uuid)
        except UserProfile.DoesNotExist:
            raise Http404

    def get(self, request, uuid):
        try:
            check_user_permission(self.request.user, 'accounts.activate_user')
        except PermissionDeniedError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        record = self.get_object(uuid)
        user = record.user
        user.is_active = True
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, uuid):
        try:
            check_user_permission(self.request.user, 'accounts.deactivate_user')
        except PermissionDeniedError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        record = self.get_object(uuid)
        user = record.user

        if user.is_superuser:
            if not request.user.is_superuser:
                return Response({"error": _("Only a superuser can deactivate a superuser profile.")}, status=status.HTTP_401_UNAUTHORIZED)

        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ManageProfileByUsernameAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, username):
        #try:
        #    check_user_permission(self.request.user, 'accounts.view_userprofile')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        record = self.get_object(username)
        profile = record.user_profile
        serialised_data = FullUserProfileModelSerializer(profile).data
        return Response(serialised_data, status=status.HTTP_200_OK)


    def put(self, request, username):
        #try:
        #    check_user_permission(self.request.user, 'accounts.change_userprofile')
        #except PermissionDeniedError as e:
        #    return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        user = self.get_object(username)
        profile = user.user_profile

        data = request.data
        data['user'] = user.id

        data['email'] = user.email
        data['username'] = user.username

        birth_date = data.get('birth_date')
        joined_on = data.get('joined_on')

        if not joined_on in [None, '']:
            try:
                joined_on = str_to_date(joined_on).date()
                data['joined_on']=joined_on
            except Exception as e:
                print(e)
                pass

        if not birth_date in [None, '']:
            try:
                birth_date = str_to_date(birth_date).date()
                data['birth_date']=birth_date
            except Exception as e:
                print(e)
                pass

        if profile:
            serializer = UserProfileEditSerializer(profile, data=data)
            if serializer.is_valid():
                profile = serializer.save(updated_by=request.user)
                serialized_profile = FullUserProfileModelSerializer(profile).data
                return Response(serialized_profile)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data)


class ManageUserIdsAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404
            

    def put(self, request, username):
        data = request.data
        user = self.get_object(username)

        email = data.get('email', user.email)
        username = data.get('username', user.username)

        user.username = username
        user.email = email

        user.save()

        serialized_profile = FullUserProfileModelSerializer(user.user_profile).data
        return Response(serialized_profile, status=status.HTTP_200_OK)


class ManageUserPasswordAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404
            

    def put(self, request, username):
        data = request.data
        user = self.get_object(username)

        password = data.get('password')
        password_confirm = data.get('password_confirm')

        current_password = data.get('current_password')

        if not user.check_password(current_password):
            return Response({"error": _("Current password incorect")}, status=status.HTTP_400_BAD_REQUEST)

        if password != password_confirm:
            return Response({"error": _("passwords do not match")}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(password)
        user.save()
        serialized_profile = FullUserProfileModelSerializer(user.user_profile).data
        return Response(serialized_profile)


class ManageUserAvatarAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404
            

    def put(self, request, username):
        data = request.data
        image = data.get("image")
        user = self.get_object(username)
        profile = user.user_profile
        profile.avatar = image
        profile.save()
        serialized_profile = FullUserProfileModelSerializer(profile).data
        return Response(serialized_profile)



class PermissionTabListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = PermissionTableModelSerializer
    pagination_class = StandardResultPagination

    def get_queryset(self):
        return Permission.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        context = super(PermissionTabListAPIView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context


class PermissionListAPIView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, IsAdmin,)
    serializer_class = PermissionSerializer

    queryset = Permission.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        context = super(PermissionListAPIView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context


class ObjectsPermissionListAPIView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, IsAdmin,)

    def get(self, request):
        #all_permissions = []
        #objects = ContentType.objects.all()
        perms = (Permission.objects.values('content_type__app_label',
                                            'content_type__model',
                                            'content_type',
                                            'codename',
                                            'name',
                                            'id',
                                            ).order_by('content_type__app_label', 'content_type__model')
                                            )
        #print(perms)
        #.values('designation', 'first_name', 'last_name')
        #for obj in objects:
            #perm_object = {'model': obj.model, 'content_type': obj.id, 'app_label': obj.app_label, 'permissions': []}
            #perms = Permission.objects.filter(content_type__app_label=obj.app_label, content_type__model=obj.model)
            #perm_object['permissions'] = PermissionSerializer(perms, many=True).data
            #all_permissions.append(perm_object)

        return Response(perms, status=status.HTTP_200_OK)


    def post(self, request):
        data = request.data
        model_type = data.pop('content_type')
        object_id = data.pop('object_id')
        app_label = data.pop('app_label')

        if model_type == 'userprofile':
            model_type = 'user'
            profile = UserProfile.objects.filter(pk=object_id)
            if profile.exists():
                object_id = profile.first().user.id

        model_qs = ContentType.objects.filter(app_label=app_label, model=model_type)

        if model_qs.exists():
            Model = model_qs.first().model_class()
            record_qs = Model.objects.filter(pk=object_id)

            if record_qs.exists():
                record = record_qs.first()

                incomin_permissions = []
                if model_type == 'user':
                    record_permissions = record.user_permissions.all()
                else:
                    record_permissions = record.permissions.all()
                existed_permissions_ids = [p.id for p in record_permissions]
                data_keys = data.keys()

                for key in data_keys:
                    if data.get(key) in [None, '']:
                        continue
                    for p_id in data.get(key):
                        if not p_id in incomin_permissions:
                            incomin_permissions.append(int(p_id))

                for p_id in incomin_permissions:
                    if p_id not in existed_permissions_ids:
                        perm = Permission.objects.filter(pk=p_id)
                        if perm.exists():
                            if model_type == 'user':
                                record.user_permissions.add(perm.first())
                            else:
                                record.permissions.add(perm.first())

                for p in record_permissions:
                    if not p.id in incomin_permissions:
                        if model_type == 'user':
                            record.user_permissions.remove(p) 
                        else:
                            record.permissions.remove(p) 
                return_data = []
                if model_type == 'user':
                    return_data = PermissionSerializer(record.user_permissions.all(), many=True)
                else:
                    return_data = PermissionSerializer(record.permissions.all(), many=True)
                return Response(return_data.data, status=status.HTTP_200_OK)
            return Response({"error": _("We could not identify the record with id ") + object_id}, status=status.HTTP_200_OK)
        return Response({"error": _("No such object ") + model_type}, status=status.HTTP_200_OK)


class ObjectPermissionListAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated, IsAdmin,)

    def get(self, request, app_label, content_type):

        return Response(status=status.HTTP_204_NO_CONTENT)


class RoleListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = RoleTableModelSerializer
    pagination_class = StandardResultPagination

    def get_queryset(self):
        return UserRole.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        context = super(RoleListAPIView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context


class RoleAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated, IsAdmin,)
    serializer_class = UserRoleSerializer

    def get(self, request):
        try:
            check_user_permission(self.request.user, 'accounts.view_userrole')
        except PermissionDeniedError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        records = UserRole.objects.all()
        serialised_data = self.serializer_class(records, many=True).data
        return Response(serialised_data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            check_user_permission(self.request.user, 'accounts.add_userrole')
        except PermissionDeniedError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        name = data.pop('name')
        created_data = {"name": name}
        serializer = self.serializer_class(data=created_data)
        if serializer.is_valid():
            role = serializer.save(owner=request.user, updated_by=request.user)
            incomin_permissions = []
            data_keys = data.keys()
            for key in data_keys:
                if data.get(key) in [None, '']:
                    continue
                for p_id in data.get(key):
                    if not p_id in incomin_permissions:
                        incomin_permissions.append(int(p_id))

            for p_id in incomin_permissions:
                perm = Permission.objects.filter(pk=p_id)
                if perm.exists():
                    role.permissions.add(perm.first())    

            return Response(self.serializer_class(role).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ManageRoleAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated, IsAdmin,)
    serializer_class = UserRoleSerializer

    def get_object(self, uuid):
        try:
            return UserRole.objects.get(_id=uuid)
        except UserRole.DoesNotExist:
            raise Http404

    def get(self, _, uuid):
        try:
            check_user_permission(self.request.user, 'accounts.view_userrole')
        except PermissionDeniedError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        record = self.get_object(uuid)
        serializer = UserRoleDetailSerializer(record)
        return Response(serializer.data)

    def delete(self, _, uuid):
        try:
            check_user_permission(self.request.user, 'accounts.delete_userrole')
        except PermissionDeniedError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        record = self.get_object(uuid)
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, uuid):
        try:
            check_user_permission(self.request.user, 'accounts.change_userrole')
        except PermissionDeniedError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        role = self.get_object(uuid)
        data = request.data
        name = data.pop('name')
        created_data = {"name": name}
        serializer = self.serializer_class(role, data=created_data)

        if serializer.is_valid():
            serializer.save(updated_by=request.user)

            incomin_permissions = []
            role_permissions = role.permissions.all()
            existed_permissions_ids = [p.id for p in role_permissions]
            data_keys = data.keys()

            for key in data_keys:
                if data.get(key) in [None, '']:
                    continue
                for p_id in data.get(key):
                    if not p_id in incomin_permissions:
                        incomin_permissions.append(int(p_id))

            for p_id in incomin_permissions:
                if p_id not in existed_permissions_ids:
                    perm = Permission.objects.filter(pk=p_id)
                    if perm.exists():
                        role.permissions.add(perm.first())

            for p in role_permissions:
                if not p.id in incomin_permissions:
                    role.permissions.remove(p)  

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PositionListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = PositionTableModelSerializer
    pagination_class = StandardResultPagination

    def get_queryset(self):
        return UserPosition.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        context = super(PositionListAPIView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context


class PositionAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated, IsAdmin,)
    serializer_class = UserPositionSerializer

    def get(self, request):
        try:
            check_user_permission(self.request.user, 'accounts.view_userposition')
        except PermissionDeniedError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
            
        records = UserPosition.objects.all()
        serialised_data = self.serializer_class(records, many=True).data
        return Response(serialised_data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            check_user_permission(self.request.user, 'accounts.add_userposition')
        except PermissionDeniedError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save(owner=request.user, updated_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ManagePositionAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated, IsAdmin,)
    serializer_class = UserPositionSerializer

    def get_object(self, uuid):
        try:
            return UserPosition.objects.get(_id=uuid)
        except UserRole.DoesNotExist:
            raise Http404

    def get(self, _, uuid):
        try:
            check_user_permission(self.request.user, 'accounts.view_userposition')
        except PermissionDeniedError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        record = self.get_object(uuid)
        serializer = UserPositionDetailSerializer(record)
        return Response(serializer.data)

    def delete(self, _, uuid):
        try:
            check_user_permission(self.request.user, 'accounts.delete_userposition')
        except PermissionDeniedError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        record = self.get_object(uuid)
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, uuid):
        try:
            check_user_permission(self.request.user, 'accounts.change_userposition')
        except PermissionDeniedError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        record = self.get_object(uuid)
        data = request.data
        serializer = self.serializer_class(record, data=data)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """

    # http_host = instance.request.META['HTTP_HOST']
    #schema_name = get_schema_name(instance.request)
    # print(schema_name)

    language = get_language_from_request_header(instance.request)

    context = {
        'protocol': instance.request.scheme,
        'domain': os.environ.get('FRONT_URL', 'localhost:4200'),
        # settings.MY_DEMO_FRONT_DOMAIN + ':4200', #settings.MY_PROD_DOMAIN, #,
        # #formatDomain(instance.request.META['HTTP_HOST'], "4200"),
        'site_name': 'Smartly SMS',
        'current_user': reset_password_token.user.username,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url':
            "{}{}".format('/auth/password-reset/', reset_password_token.key)
    }

    title="Le Recul Hotel"
    mail_subject = _("Password Reset for") + title
    email_template = 'accounts/user_reset_password.html'

    try:
        send_password_reset_link.delay(email_template, mail_subject, reset_password_token.user.email, context, language=language)
    except Exception as e:
        print(e)


class CheckPermissionAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user = request.user
        data = request.data
        perm = data.get('perm')
        user_permission_codes = user.get_user_permission_codes()
        permissions = [p.split('.')[1] for p in user_permission_codes]
        has_permission = perm in permissions
        return Response({"has_permission": has_permission})
    
class CheckViewPermissionAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user = request.user
        data = request.data

        url = data.get('url')
        user_views = user.get_user_all_frontend_views()
        links = [v.root_link for v in user_views]
        has_view = url in links
        return Response({"has_view": has_view})



    