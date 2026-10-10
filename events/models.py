from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime


# Create your models here.
class Category(models.Model):
  name = models.CharField(max_length=100)
  def __str__(self):
    return self.name

class Venue(models.Model):
  name = models.CharField(max_length=100)
  capacity = models.PositiveBigIntegerField()
  location = models.CharField(max_length=200)
  def __str__(self):
    return self.name


class Club(models.Model):

    name = models.CharField(max_length=100)

    description = models.TextField()

    logo = models.ImageField(
        upload_to="club_logos/",
        blank=True,
        null=True
    )

    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Event(models.Model):
  REGISTRATION_CHOICES =(
    ("OUR_FORM","Our Registration Form"),
    ("EXTERNAL","External Link"),
  )
  registration_type = models.CharField(
    max_length=20,
    choices=REGISTRATION_CHOICES,
    default="OUR_FORM"
  )
  registration_link = models.URLField(
    blank=True,
    null=True
  )
  name = models.CharField(max_length=200)
  description = models.TextField()
  image = models.ImageField(
      upload_to="event_images/",
      blank=True,
      null=True
  )
  date = models.DateField()
  start_time = models.TimeField()
  end_time = models.TimeField()

  category = models.ForeignKey(
    Category,
    on_delete=models.PROTECT
  )

  club = models.ForeignKey(
    Club,
    on_delete=models.PROTECT
  )

  venue = models.ForeignKey(
    Venue,
    on_delete=models.PROTECT
  )

  participants = models.PositiveIntegerField()
  registration_fee = models.DecimalField(
    max_digits=8,
    decimal_places=2,
    default=0
  )
  created_at = models.DateTimeField(auto_now_add=True)
  def clean(self):
    if not self.venue or not self.date or not self.start_time or not self.end_time:
      return
    overlapping_events = Event.objects.filter(
      venue = self.venue,
      date=self.date,
      start_time__lt=self.end_time,
      end_time__gt = self.start_time
    ).exclude(pk=self.pk)
    if overlapping_events.exists():
      raise ValidationError(
        "This Venue is already booked for selected time."
      )

  @property
  def status(self):

      now = timezone.localtime()

      start_datetime = timezone.make_aware(
          datetime.combine(
              self.date,
              self.start_time
          ),
          timezone.get_current_timezone()
      )

      end_datetime = timezone.make_aware(
          datetime.combine(
              self.date,
              self.end_time
          ),
          timezone.get_current_timezone()
      )

      if now < start_datetime:
          return "Upcoming"

      elif now <= end_datetime:
          return "Ongoing"

      else:
          return "Completed"
      
  def __str__(self):
    return self.name


class ClubMember(models.Model):

    MEMBERSHIP_CHOICES = (
        ("CORE", "Core Member"),
        ("MEMBER", "Member"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    club = models.ForeignKey(
        Club,
        on_delete=models.PROTECT
    )

    membership_type = models.CharField(
        max_length=20,
        choices=MEMBERSHIP_CHOICES,
        default="MEMBER"
    )

    is_president = models.BooleanField(
        default=False
    )

    position = models.CharField(
        max_length=100,
        blank=True
    )

    def clean(self):

        if self.position and self.position.strip().lower() == "president":
            if not self.is_president:
                raise ValidationError(
                    "President position can only be assigned using is_president."
                )

    def __str__(self):
        return f"{self.user.username} - {self.club.name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["club"],
                condition=models.Q(is_president=True),
                name="unique_president_per_club"
            )
        ]



class EventRegistration(models.Model):
  user = models.ForeignKey(
    User,
    on_delete=models.CASCADE
  )
  event = models.ForeignKey(
    Event,
    on_delete=models.CASCADE
  )
  name = models.CharField(max_length=100)
  usn = models.CharField(max_length=20)
  branch = models.CharField(max_length=100)
  semester = models.PositiveIntegerField()
  registered_at = models.DateTimeField(
    auto_now_add=True
  )
  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=["user","event"],
        name="unique_event_registration"
      )
    ]
  def __str__(self):
    return f"{self.user.username} - {self.event.name}"




class ExternalRegistrationConfirmation(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="external_registration_confirmations"
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="external_confirmations"
    )

    confirmed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "event"],
                name="unique_external_registration_confirmation"
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.event.name}"
