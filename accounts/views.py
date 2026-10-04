from django.shortcuts import render, redirect
from .forms import SignUpForm
from events.models import ClubMember,Event,Club,Category
from django.utils import timezone
from django.db.models import Q, Count
# Create your views here.

def home(request):

    is_core_member = False

    if request.user.is_authenticated:
        is_core_member = ClubMember.objects.filter(
            user=request.user,
            membership_type="CORE"
        ).exists()

    now = timezone.localtime()

    events = Event.objects.filter(
        Q(date__gt=now.date()) |
        Q(
            date=now.date(),
            start_time__gte=now.time()
        )
    ).order_by(
        "date",
        "start_time"
    )

    clubs = Club.objects.filter(
        is_approved=True
    )

    categories = Category.objects.filter(
        Q(
            event__date__gt=now.date()
        ) |
        Q(
            event__date=now.date(),
            event__start_time__gte=now.time()
        )
    ).distinct()

    return render(
        request,
        "accounts/home.html",
        {
            "is_core_member": is_core_member,
            "events": events,
            "clubs": clubs,
            "categories": categories,
        }
    )



def signup(request):
  if request.method == "POST":
    form = SignUpForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect("login")
  else:
    form = SignUpForm()
  return render(request,"accounts/signup.html",{"form":form})
