from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, CreateAPIView
from django.contrib.auth.models import User
from rest_framework import status, generics
from .models import Ticket, Feedback, InternalNote, Category, Resolution
from .serializers import TicketSerializer, UserSerializer, FeedbackSerializer, CategorySerializer, ResolutionSerializer
from rest_framework.permissions import IsAuthenticated



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_id(request):
    username = request.query_params.get('username', None)
    if username is not None:
        try:
            user = User.objects.get(username=username)
            return Response({'user_id': user.id}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'error': 'Username not provided'}, status=status.HTTP_400_BAD_REQUEST)




class CreateUserView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    


class TicketCreate(APIView):
    def post(self, request, format=None):
        serializer = TicketSerializer(data=request.data)    
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TicketUpdate(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class TicketList(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        tickets = Ticket.objects.all()
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)
    
class TicketDetail(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class TicketListByUser(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer
    
    def get_queryset(self):
        queryset = Ticket.objects.all()
        user_id = self.request.query_params.get('userId', None)
        if user_id is not None:
            queryset = queryset.filter(user__id=user_id)
        return queryset


class FeedbackCreate(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

class FeedbackDetail(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    lookup_field = 'ticket_id'

class FeedbackListByUser(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FeedbackSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Feedback.objects.filter(ticket__user_id=user_id)
    
class FeedbackByAssignTo(APIView):
    def get(self, request, assign_to_id):
        tickets = Ticket.objects.filter(assignTo__id=assign_to_id)
        feedbacks = Feedback.objects.filter(ticket__in=tickets)
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data)

class FeedbackUpdateView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    lookup_field = 'ticket_id'

    def get_object(self):
        ticket_id = self.kwargs.get("ticket_id")
        return Feedback.objects.get(ticket__id=ticket_id)
    

class CategoryCreateView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class ResolutionCreateView(CreateAPIView):
    queryset = Resolution.objects.all()
    serializer_class = ResolutionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(resolved_by=self.request.user)

class ResolutionRetrieveView(RetrieveAPIView):
    queryset = Resolution.objects.all()
    serializer_class = ResolutionSerializer
    permission_classes = [IsAuthenticated]

class ResolutionUpdateView(RetrieveUpdateAPIView):
    queryset = Resolution.objects.all()
    serializer_class = ResolutionSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save()


