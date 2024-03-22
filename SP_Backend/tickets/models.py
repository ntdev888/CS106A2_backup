from django.db import models
from django.conf import settings
from django.utils import timezone


# Define your ticket status choices
class TicketStatus(models.TextChoices):
    OPEN = 'OP', 'Open'
    IN_PROGRESS = 'IP', 'In Progress'
    CLOSED = 'CL', 'Closed'

class AssignTo(models.TextChoices):
    BLANK = " ", " "  # Provide a display value for BLANK
    PAUL = "Paul", "Paul"
    DAVID = "David", "David"
    MIKE = "Mike", "Mike"

class ContactBy(models.TextChoices):
    PHONE = "Phone", "Phone"
    EMAIL = "Email", "Email"
    TEAMS = "Teams", "Teams"
    TEXT = "Text Msg", "Text Msg"

class IssueArea(models.TextChoices):
    BLANK = " ", " "  # Provide a display value for BLANK
    CELLPHONE = "Cellphone", "Cellphone"
    COMPUTER = "Laptop", "Laptop"
    AUDITPLUS = "AuditPlus", "AuditPlus"
    OFFICE = "MS Office", "MS Office"

class Priority(models.TextChoices):
    LOW = "Low", "Low"
    MEDIUM = "Medium", "Medium"
    HIGH = "High", "High"

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets')
    status = models.CharField(max_length=2, choices=TicketStatus.choices, default=TicketStatus.OPEN)
    created_at = models.DateTimeField(default=timezone.now)
    assignTo = models.CharField(max_length=5, choices=AssignTo.choices, default=AssignTo.BLANK)  
    contactMe = models.CharField(max_length=8, choices=ContactBy.choices, default=ContactBy.EMAIL)  
    area = models.CharField(max_length=10, choices=IssueArea.choices, default=IssueArea.BLANK)  
    priority = models.CharField(max_length=6, choices=Priority.choices, default=Priority.LOW) 
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='tickets') 

    def __str__(self):
        return self.title
    

class Feedback(models.Model):
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, related_name='feedback')
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for Ticket ID {self.ticket_id} - Rating: {self.rating} Stars"


class InternalNote(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='internal_notes')
    note = models.TextField()
    message_to_user = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_internal_notes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note for Ticket ID {self.ticket_id} - Created by {self.created_by}"
    
class Resolution(models.Model):
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, related_name='resolution')
    resolved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='resolved_tickets')
    resolution_steps = models.TextField()
    resolution_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resolution for Ticket ID {self.ticket_id}"
