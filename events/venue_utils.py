from .models import Venue, Event

def get_available_venues(date,start_time,end_time):
  venues = Venue.objects.all()
  available_venues = []
  for venue in venues:
    clash = Event.objects.filter(
      venue=venue,
      date=date,
      start_time__lt = end_time,
      end_time__gt = start_time
    ).exists()

    if not clash:
      available_venues.append(venue)
  return available_venues