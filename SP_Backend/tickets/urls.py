from django.urls import path
from .views import TicketCreate, TicketList, TicketDetail, CreateUserView, TicketUpdate, TicketListByUser, FeedbackCreate, FeedbackDetail, FeedbackListByUser, FeedbackByAssignTo
from .views import FeedbackUpdateView, get_user_id, CategoryCreateView, ResolutionCreateView, ResolutionRetrieveView, ResolutionUpdateView

urlpatterns = [
    path('api/users/', CreateUserView.as_view(), name='create-user'),
    path('api/tickets/', TicketList.as_view(), name='ticket-list'),
    path('api/tickets/<int:pk>/', TicketDetail.as_view(), name='ticket-detail'),
    path('api/tickets/create/', TicketCreate.as_view(), name='ticket-create'),
    path('api/tickets/updt/<int:pk>/', TicketUpdate.as_view(), name='ticket-update'),
    path('api/tickets/by_user/', TicketListByUser.as_view(), name='tickets-by-user'),
    path('api/feedback/', FeedbackCreate.as_view(), name='feedback-create'),
    path('api/feedback/ticket/<int:ticket_id>/', FeedbackDetail.as_view(), name='feedback-by-ticket'),
    path('api/feedback/user/<int:user_id>/', FeedbackListByUser.as_view(), name='feedback-by-user'),
    path('api/feedback/assignee/<int:assignee_id>/', FeedbackByAssignTo.as_view(), name='feedback-by-assignee'),
    path('api/feedback/<int:ticket_id>/', FeedbackUpdateView.as_view(), name='feedback-update'),
    path('api/get-user-id/', get_user_id, name='get-user-id'),
    path('api/categories/', CategoryCreateView.as_view(), name='category-create'),
    path('api/resolutions/create/', ResolutionCreateView.as_view(), name='resolution-create'),
    path('resolutions/<int:pk>/', ResolutionRetrieveView.as_view(), name='resolution-detail'),
    path('resolutions/update/<int:pk>/', ResolutionUpdateView.as_view(), name='resolution-update'),
]
