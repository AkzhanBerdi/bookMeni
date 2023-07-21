import datetime
from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
class CalenderSlot(models.Model):
    """Calendar slots available for the user to book by other people.

    """
    belongs_to = models.ForeignKey(to=get_user_model(), related_name='created_slots', on_delete=models.CASCADE, help_text="""
    Stores the user the slot belogs to
    """)
    created_at = models.DateTimeField(auto_now_add=True, help_text="""
    Django auto populates timestamp whenever a slot is created by a user.
    """)
    start_time = models.DateTimeField(help_text="""
    Contains the start time of the slot.
    """)
    end_time = models.DateTimeField(help_text="""
    Contains the end time of the slot.
    """)

    class Meta:
        """The default ordering is set to the descending order of when the slot was created.
        
        """
        ordering = ['-created_at']


class SlotBooking(models.Model):
    """Contains the booking details of the slot.
    
    """
    slot = models.OneToOneField(to=CalenderSlot, related_name='booking_details', on_delete=models.CASCADE, help_text="""
    References to the slot that is booked.
    """)
    booked_by = models.ForeignKey(to=get_user_model(), related_name='booked_slots', on_delete=models.CASCADE, help_text="""
    Contains the user who has booked the slot. If it was booked by an anonymous user, it is None.
    """)
    booked_at = models.DateTimeField(auto_now_add=True, help_text="""
    Django auto populates timestamp whenever a slot is booked
    """)
    description = models.TextField(null=True, help_text="""
    Contains some booking data entered by the person who booked the slot.
    """)

    class Meta:
        """The default ordering is set to the descending order of when the slot was booked.

        """
        ordering = ['-booked_at']