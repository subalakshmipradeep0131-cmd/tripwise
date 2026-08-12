from django.db import models


from django.contrib.auth.models import User
# Create your models here.
# schema:Trip
# fileds:title,destination,date,is_active,created_by,


class Trip(models.Model):

    title = models.CharField(max_length=100)
  
    destination = models.CharField(max_length=100)

    start_date = models.DateField()

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_trips"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class TripMember(models.Model):

    ROLE_CHOICES = (
        ("OWNER", "Owner"),
        ("MEMBER", "Member"),
    )

    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="members"
    )

    member = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="trip_members"
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="MEMBER"
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("trip", "member")

    def __str__(self):
        return f"{self.member.username} - {self.trip.title}"