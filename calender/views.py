from datetime import datetime, timedelta
import time

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken

from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import render

from .constants import ResponseMessage
from .functions import generate_google_calendar_link
from .models import CalenderSlot, SlotBooking


class SlotDataView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        """Creates a bookable slot for the logged user.

        Creates a slot of one hour from the provided start time available for booking for the logged in user.
        The slot is created if it does not conflict with any existing slot and if the end time of the slot is
        greater than the current time, because the slot should be available to book after it is created.

        """
        try:
            start_time = datetime.datetime.strptime(request.data['start_time'], "%Y-%m-%dT%H:%M:%SZ")
        except KeyError:
            return Response(data=ResponseMessage.MISSING_KEY.format("start_time"), status=HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response(data=ResponseMessage.INVALID_DATA, status=HTTP_400_BAD_REQUEST)
        end_time = start_time + datetime.timedelta(hours=1)
        if end_time < datetime.datetime.now():
            return Response(data=ResponseMessage.CREATE_FUTURE_SLOTS, status=HTTP_400_BAD_REQUEST)
        blocking_slot = CalenderSlot.objects.filter(belongs_to=request.user, end_time__gt=start_time)
        if blocking_slot:
            response_message = ResponseMessage.CONFLICTING_SLOTS.format(blocking_slot[0].start_time, blocking_slot[0].end_time)
            return Response(data=response_message, status=HTTP_400_BAD_REQUEST)
        calender_slot = CalenderSlot.objects.create(belongs_to=request.user, start_time=start_time, end_time=end_time)
        # return Response(data={'id': calender_slot.id}, status=HTTP_200_OK)
        return render(request, 'available_slots.html', {'available_slots': all_created_slots})

    def get(self, request, *args, **kwargs):
        """Returns all the slot details created by the logged in user.

        Returns the id, start and end time of the slot, and if the slot is booked for each of the slots.

        """
        all_created_slots = CalenderSlot.objects.filter(belongs_to=request.user)
        response_data = []
        for slot_detail in all_created_slots:
            slot_data = {
                'id': slot_detail.id,
                'start_time': str(slot_detail.start_time),
                'end_time': str(slot_detail.end_time)
            }
            try:
                slot_detail.booking_details
            except:
                slot_data['is_booked'] = False
            else:
                slot_data['is_booked'] = True
            response_data.append(slot_data)
        # return Response(data=response_data, status=HTTP_200_OK)
        return render(request, 'calender/slot_data.html', {'slot_data': response_data})


class SlotDetailsView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        """Gives a detailed information of the specified slot, including details of the booking if it is booked.

        The booking status is determined by accessing the `booking_details` from the current slot object, which is
        set only when the slot is booked. If it was booked anonymously, the booked by field is set to the string
        `Anonymous User`, else the username of the registered user is set in the response data.

        """
        if CalenderSlot.objects.filter(id=kwargs['id'], belongs_to=request.user).exists() is False:
            return Response(data=ResponseMessage.CALENDAR_SLOTS_NOT_FOUND, status=HTTP_404_NOT_FOUND)
        slot_details = CalenderSlot.objects.select_related('booking_details__booked_by').get(
            id=kwargs['id'], belongs_to=request.user
        )
        response_data = {
            'id': slot_details.id,
            'start_time': str(slot_details.start_time),
            'end_time': str(slot_details.end_time)
        }
        try:
            booking_details = slot_details.booking_details
        except:
            response_data['is_booked'] = False
        else:
            booked_by = "Anonymus User"
            if booking_details.booked_by:
                booked_by = booking_details.booked_by.username
            response_data.update({
                "is_booked": True,
                "booking_id": booking_details.id,
                "booked_by": booked_by,
                "booked_at": str(booking_details.booked_at),
                "description": booking_details.description
            })
        # return Response(data=response_data, status=HTTP_200_OK)
        return render(request, 'calender/slot_details.html', {'slot': response_data})

    def delete(self, request, *args, **kwargs):
        """Deletes the registered calender slot.
        
        """
        try:
            CalenderSlot.objects.get(id=kwargs['id'], belongs_to=request.user).delete()
        except CalenderSlot.DoesNotExist:
            return Response(data=ResponseMessage.CALENDAR_SLOT_NOT_FOUND, status=HTTP_404_NOT_FOUND)
        else:
            return Repsonse(status=HTTP_200_OK)


class GetAvailableSlots(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        """Lists all the available slots of the requested user.

        The API is accessible by both registered and anonymous users. So no authentication check is done.
        
        """
        try:
            user = User.objects.get(id=kwargs['user_id'])
        except User.DoesNotExist:
            return Response(data=ResponseMessage.USER_NOT_FOUND, status=HTTP_404_NOT_FOUND)
        available_slots = CalenderSlot.objects.filter(
            start_time__gt=timezone.now(), booking_details=None, belongs_to=user
        )
        response_data = []
        for slot_details in available_slots:
            response_data.append({
                "id": slot_details.id,
                "start_time": str(slot_details.start_time),
                "end_time": str(slot_details.end_time)
            })
        # return Response(data=resposne_data, status=HTTP_200_OK)
        return render(request, 'calender/available_slots.html', {'available_slots': response_data})


class BookSlotView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Retrieve the details of the requested slot.
        
        Checks if the requested slot exists and returns its details if available.
        """
        try:
            slot = CalenderSlot.objects.get(id=kwargs['id'])
        except CalenderSlot.DoesNotExist:
            return Response(data=ResponseMessage.CALENDAR_SLOT_NOT_FOUND, status=HTTP_404_NOT_FOUND)
        
        response_data = {
            "id": slot.id,
            "start_time": str(slot.start_time),
            "end_time": str(slot.end_time)
        }

        # Check if the slot is booked and add booking details if available
        if SlotBooking.objects.filter(slot=slot).exists():
            booking_details = SlotBooking.objects.get(slot=slot)
            booked_by = "Anonymous User" if booking_details.booked_by is None else booking_details.booked_by.username
            response_data["is_booked"] = True
            response_data["booking_id"] = booking_details.id
            response_data["booked_by"] = booked_by
            response_data["booked_at"] = str(booking_details.booked_at)
            response_data["description"] = booking_details.description
        else:
            response_data["is_booked"] = False

        return render(request, 'calender/book_slot.html', {'booking_details': response_data})
        # return Response(data=response_data, status=HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """Book the requested slot. This API is accessible for both anonymus and registered users.

        Checks if the requested slot exists and is not booked yet. Booking is only allowed for slots in the future.
        Returns the booking id and a link to add the event to Google Calendar.
        
        """
        try:
            slot = CalenderSlot.objects.get(id=kwargs['id'])
        except CalenderSlot.DoesNotExist:
            return Response(data=ResponseMessage.CALENDAR_SLOT_NOT_FOUND, status=HTTP_404_NOT_FOUND)
        if SlotBooking.objects.filter(slot=slot).exists():
            return Response(data=ResponseMessage.CALENDAR_SLOT_ALREADY_BOOKED, status=HTTP_400_BAD_REQUEST)
        if slot.end_time < timezone.now():
            return Response(data=ResponseMessage.CALENDAR_SLOT_EXPIRED, status=HTTP_400_BAD_REQUEST)
        try:
            booking_description = request.data['description']
        except KeyError:
            return Response(data=ResponseMessage.MISSING_KEY.format("description"), status=HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            slot_booking_details = SlotBooking.objects.create(slot=slot, booked_by=self.request.user, description=booking_description)
            response_data = {
                "id": slot_booking_details.id,
                "add_to_google_calendar": generate_google_calendar_link(slot_booking_details)
            }
            # return Response(data=response_data, status=HTTP_200_OK)
            return render(request, 'calender/book_slot.html', {'booking_details': response_data})
    
    def delete(self, request, *args, **kwargs):
        """Deletes the requested booking.

        Only the booking made by registrated users can be deleted. This is to prevent cases when anyone can delete bookings of others.
        
        """
        if requested.user is None:
            return Response(data=ResponseMessage.REGISTRATION_REQUIRED, status=HTTP_401_UNAUTHORIZED)
        booking = SlotBooking.objects.filter((Q(booked_by=request.user) | Q(slot__belongs_=request.user)), slot__id=kwargs['id'])
        if len(booking) == 0:
            return Response(data=ResponseMessage.BOOKING_NOT_FOUND, status=HTTP_404_NOT_FOUND)
        booking[0].delete()
        return Response(status=HTTP_200_OK)
        

class CreateSlotsForIntervalView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        """
        Renders the form to create slots for the specified interval.
        """
        return render(request, 'calender/slot_interval.html')


    def post(self, request, *args, **kwargs):
        interval_start = datetime.strptime(request.data['interval_start'], "%Y-%m-%dT%H:%M")
        interval_stop = datetime.strptime(request.data['interval_stop'], "%Y-%m-%dT%H:%M")

        # Get the user who is creating the slots
        user = request.user

        while interval_start < interval_stop:
            slot = CalenderSlot.objects.create(
                start_time=interval_start,
                end_time=interval_start + timedelta(hours=1),
                belongs_to=user
            )
            interval_start += timedelta(hours=1)

        return Response(status=HTTP_201_CREATED)
        # if not interval_start or not interval_stop:
        #     return Response({
        #         'error': 'Interval start and stop values are required'},
        #         status=HTTP_400_BAD_REQUEST
        #     )

        # try:
        #     interval_start = datetime.strptime(interval_start, '%Y-%m-%dT%H:%M')
        #     interval_stop = datetime.strptime(interval_stop, '%Y-%m-%dT%H:%M')
        # except ValueError:
        #     return Response({'error': 'Invalid date format'},
        #     status=HTTP_400_BAD_REQUEST)

        # created_slot_ids = []
        # slot_start_time = interval_start
        # slot_end_time = slot_start_time + timedelta(hours=1)

        # while slot_end_time <= interval_stop:
        #     slot = CalenderSlot.objects.create(belongs_to=request.user, start_time=slot_start_time, end_time=slot_end_time)
        #     created_slot_ids.append(slot.id)
        #     slot_start_time = slot_end_time
        #     slot_end_time = slot_end_time + timedelta(hours=1)

        # return Response({'created_slot_ids': created_slot_ids}, status=HTTP_200_OK)

class UserLoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        """ Checks for the login details of the user and sends the Token if successfully authenticated.

        Overrides the default token Authentication View for customized responses.

        """
        serializer = self.serializer_class(data=request.data, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return Response(data=ResponseMessage.INVALID_LOGIN_DATA, status=HTTP_401_UNAUTHORIZED)
        else:
            user = serializer.validated_data['user']
            token = Token.objects.get(user=user)
            return Response(data={'token': token.key}, status=HTTP_200_OK)