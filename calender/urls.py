from django.urls import include, path
from django.contrib.auth.views import LogoutView
from .views import BookSlotView, CreateSlotsForIntervalView, GetAvailableSlots, SlotDataView, SlotDetailsView, UserLoginView

urlpatterns = [
    path('book/slot/<int:id>/', BookSlotView.as_view(), name='book_slot'),
    path('book/<int:user_id>/slots/', GetAvailableSlots.as_view(), name='available_slots'),
    path('slot/<int:id>/', SlotDetailsView.as_view(), name='slot_details'),
    path('slot/', SlotDataView.as_view(), name='slot_data'),
    path('slots/interval/', CreateSlotsForIntervalView.as_view(), name='slot_interval'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]