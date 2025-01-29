from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

# Create your models here.
class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=True)
    def __str__(self):
        return self.username

  
class Destination(models.Model):
    COUNTRY_CHOICES = [
        ('T', 'Thailand'),
        ('I', 'Indonesia'),
        ('V', 'Vietnam'),
        ('M', 'Malaysia'),
        ('P', 'Philippines'),
        ('L', 'Laos'),
    ]


    name = models.CharField(max_length=100)  # Name of the destination
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='destinations')
    country = models.CharField(max_length=20, choices=COUNTRY_CHOICES)  # Country code from COUNTRY_CHOICES
    description = models.TextField(blank=True)  # A detailed description of the destination
    best_time_to_visit = models.CharField(max_length=50)  # The best time to visit (e.g., "November to March")
    image = models.ImageField(upload_to='destinations/', default="null")  # Optional: an image of the destination
    
    def __str__(self):
        return self.name    
    
    
class TravelPlan(models.Model):
    # Foreign Key to User to track which user created the plan
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='travel_plans')

    # Many-to-Many relationship with Destination to store multiple destinations in the plan
    destinations = models.ManyToManyField('Destination', related_name='travel_plans')

    # A brief description or title of the travel plan
    title = models.CharField(max_length=100)

    traveldays = models.IntegerField()
    
    # Detailed description of the travel plan
    description = models.TextField()

    def __str__(self):
        return f"Travel Plan: {self.title} (User: {self.user.username})"    
    
    
class Activity(models.Model):
  # Many-to-many relationship with TravelPlan to associate activities with multiple travel plans
    travel_plans = models.ManyToManyField('TravelPlan', related_name='activities')

    # Many-to-many relationship with Destination to associate activity with multiple destinations
    destinations = models.ManyToManyField('Destination', related_name='activities')
    
    # Name of the activity (e.g., "Visit to Wat Arun", "Snorkeling in Bali")
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Activity: {self.name} at {self.destination.name}"    
    


class Comment(models.Model):
    comment = models.TextField()

    # User who posted the comment
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments', blank=True)

    # ForeignKey to Destination, only one of these will be populated
    destination = models.ForeignKey('Destination', on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    
    # ForeignKey to TravelPlan, only one of these will be populated
    travel_plan = models.ForeignKey('TravelPlan', on_delete=models.CASCADE, related_name='comments', null=True, blank=True)

    def clean(self):
        """
        Custom validation to ensure that either `destination` or `travel_plan` is set,
        but not both.
        """
        if not self.destination and not self.travel_plan:
            raise ValidationError('A comment must be associated with either a destination or a travel plan.')
        
        if self.destination and self.travel_plan:
            raise ValidationError('A comment cannot be associated with both a destination and a travel plan.')

    def __str__(self):
        return f"Comment by {self.user.username} on {self.get_content_target()}"

    def get_content_target(self):
        """
        Returns a string describing whether the comment is on a TravelPlan or a Destination.
        """
        if self.destination:
            return f"Destination: {self.destination.name}"
        elif self.travel_plan:
            return f"Travel Plan: {self.travel_plan.title}"
        return "No target"    