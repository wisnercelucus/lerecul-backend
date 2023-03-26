from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from core.models import Customer, Room, Booking
from django.conf import settings
from rest_framework import generics
from core.utils.emails import email_booking_receipt, email_contact_message, send_alert_email

from core.utils.util_funcs import (correct_timeline, generate_randowm_code, generate_randowm_password, get_language_from_request_header, str_to_date,)
from home.api.serializers import ContactMessageModelSerializer, NewsSubscriberModelSerializer

from accounts.models import UserProfile
#from django.utils.translation import gettext as _
#from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _

class BookNowAPIView(APIView):
    #permission_classes = [IsAuthenticated, ]

    def post(self, request):
        primary_contact_qs = UserProfile.objects.filter(primary_contact_for_customer_care=True)
        if primary_contact_qs.exists():
            primary_contact = primary_contact_qs.first()
        else:
            return Response({"error": _("We could not find a primary contact for customer care. Ask Le Recul to set a Primary contact.")}, status=status.HTTP_400_BAD_REQUEST)
        
        data = request.data
        #print(data)
        email = data.get('email', None)
        fullname = data.get('fullname', None)
        room = data.get('room', None)
        n_roomates = data.get('n_roomates', 1)

        start_on = str_to_date(data.get('start_on'))
        end_on = str_to_date(data.get('end_on'))

        if start_on in [None, '']:
            return Response({"error": _("You must add the start date to make a reservation")}, status=status.HTTP_400_BAD_REQUEST)

        if end_on in [None, '']:
            return Response({"error": _("You must add the end date to make a reservation")}, status=status.HTTP_400_BAD_REQUEST)

        if not correct_timeline(start_on, end_on):
            return Response({"error": _("End date must be in future compared to start date")}, status=status.HTTP_400_BAD_REQUEST)

        if email in [None, '']:
            return Response({'error': _('You need a valid email address to book rooms online.')}, status=status.HTTP_400_BAD_REQUEST)

        if fullname in [None, '']:
            return Response({'error': _('You need to enter your fullname to make a reservation.')}, status=status.HTTP_400_BAD_REQUEST)

        if room in [None, '']:
            return Response({'error': _('You need to select a room to make a reservation.')}, status=status.HTTP_400_BAD_REQUEST)


        # get or create a new custumer
        customer_qs = Customer.objects.filter(email=email)
        room_qs = Room.objects.filter(pk=room)

        if room_qs.exists():
            room = room_qs.first()
        else:
            return Response({'error': _('The room with Id: ' + str(room) + ' does not exist.')}, status=status.HTTP_400_BAD_REQUEST)

        if customer_qs.exists():
            customer = customer_qs.first()
        else:
            customer = Customer()
            customer.name = fullname
            customer.email = email
            password = generate_randowm_password(settings.PASSWORD_LENGTH)
            acess_code = generate_randowm_code(settings.CODE_LENGTH)
            customer.pass_code = password
            customer.code = acess_code

            customer.save()
            
        # create a booking an associate it with the customer
        booking = Booking()
        booking.name = _('Booking #') + str(booking.pk) + ' - ' + customer.name + ' - ' + room.name
        booking.customer = customer
        booking.room = room
        booking.number_of_people = n_roomates if n_roomates else 1
        booking.start_on = start_on
        booking.end_on = end_on
        booking.save() 

        try:

            hotel_name = 'Le Recul'
            primary_contact_name = primary_contact.user.name
            primary_contact_email = primary_contact.user.email
            primary_contact_phone = primary_contact.user.email

            context = {"fullname": customer.name, 
                'room': room.name, 
                'n_roomates': booking.number_of_people,
                'start_on': booking.start_on,
                'end_on': booking.end_on,
                'hotel_name': hotel_name,
                'primary_contact_name': primary_contact_name,
                'primary_contact_email': primary_contact_email,
                'primary_contact_phone': primary_contact_phone
                }
            
            mail_subject = 'Booking receipt #' + str(booking.id)
            to_email = customer.email
            email_template = 'core/booking_receipt.html'
            language = get_language_from_request_header(self.request)
            email_booking_receipt.delay(mail_subject, to_email, email_template, context, language=language)
            #send_alert_email.delay('home/alert_email_template.html', 'New booking alert', settings.EMAIL_ADMIN_TO, context, language=None)
        except Exception as e:
            print(e)

        try:

            context = {"username": "Admin", "message": _(f"{customer.name} has just made a room reservation for: " + room.name)}
            users_to_notify = UserProfile.objects.filter(notified_on_new_booking=True)
            if users_to_notify.exists():
                for p in users_to_notify:
                    send_alert_email.delay('home/alert_email_template.html', _('New booking alert'), p.user.email, context, language=None)
        except Exception as e:
            print(e)


        
        return Response(data, status=status.HTTP_200_OK)
    


def send_contact_message(instance, user, language=None):
    if instance:
        name = instance.name
        email = instance.email
        phone = instance.country_code + instance.phone
        country = instance.country
        message = instance.message

        mail_subject = instance.subject
        to_email = user.email

        try:
            email_contact_message.delay(name, phone, email, country, mail_subject, message, to_email, 'home/contact_message_email.html', language=language)
            instance.emailed_success = True
            instance.save()
        except Exception as e:
            instance.emailed_success = False
            instance.save()


class NewsSubscriberCreateAPIView(generics.CreateAPIView):
    """Record new subscriber in the database"""
    serializer_class = NewsSubscriberModelSerializer

    def perform_create(self, serializer):
        """Create a new responsible"""
        primary_contact_qs = UserProfile.objects.filter(primary_contact_for_customer_care=True)
        if primary_contact_qs.exists():
            primary_contact = primary_contact_qs.first()
        else:
            return Response({"error": _("We could not find a primary contact for customer care. Ask Le Recul to set a Primary contact.")}, status=status.HTTP_400_BAD_REQUEST)
        
        instance = serializer.save()
        context = {"username": "Admin", "message": _("Somone has subscribed to newsletter with the email: ") + instance.email}
        language = get_language_from_request_header(self.request)
        send_alert_email.delay('home/alert_email_template.html', _('New subscriber'), primary_contact.user.email, context, language=language)


class ContactMessageCreateAPIView(generics.CreateAPIView):
    """Record new subscriber in the database"""
    serializer_class = ContactMessageModelSerializer

    def perform_create(self, serializer):
        #print(serializer)
        """Create a new responsible"""
        primary_contact_qs = UserProfile.objects.filter(primary_contact_for_customer_care=True)
        if primary_contact_qs.exists():
            primary_contact = primary_contact_qs.first()
        else:
            return Response({"error": _("We could not find a primary contact for customer care. Ask Le Recul to set a Primary contact.")}, status=status.HTTP_400_BAD_REQUEST)
        
        instance = serializer.save()
        language = get_language_from_request_header(self.request)
        send_contact_message(instance, primary_contact.user, language=language)