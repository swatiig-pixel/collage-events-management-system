from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import EventForm, EventRegistrationForm, AddCoreMemberForm
from .permissions import is_core_member
from .models import Event, EventRegistration, Club,ClubMember, Category
from django.db import transaction
from django import forms
from django.db.models import Count
from django.utils import timezone
from django import forms
from .permissions import is_core_member, is_president
from django.db.models import Q
from accounts.models import StudentProfile
from .forms import StudentSearchForm
from django.contrib import messages
from django.urls import reverse

# Create your views here.
@login_required
def create_event(request, club_id):

    club = get_object_or_404(
        Club,
        id=club_id
    )

    if not is_core_member(request.user, club):

        return render(
            request,
            "events/no_permission.html"
        )

    if request.method == "POST":

        form = EventForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            event = form.save(
                commit=False
            )

            event.club = club
            event.save()

            return render(
                request,
                "events/success.html",
                {
                    "success_title": "Event Created Successfully!",
                    "success_message": f"{event.name} has been created successfully.",
                    "success_url": reverse("home"),
                    "event": event
                }
            )

        else:
            print(form.errors)

    else:
        form = EventForm()

    return render(
        request,
        "events/create_event.html",
        {
            "form": form,
            "club": club
        }
    )


@login_required
def event_list(request):

    category_id = request.GET.get("category")
    search = request.GET.get("search")

    events = Event.objects.annotate(
        registration_count=Count("eventregistration")
    )

    if category_id:
        events = events.filter(
            category_id=category_id
        )

    if search:
        events = events.filter(
            name__icontains=search
        )

    events = events.order_by(
        "date",
        "start_time"
    )

    # Only show upcoming events
    events = [
        event
        for event in events
        if event.status == "Upcoming"
    ]

    categories = Category.objects.all()

    return render(
        request,
        "events/event_list.html",
        {
            "events": events,
            "categories": categories,
            "selected_category": category_id,
            "search": search,
        }
    )

def event_detail(request, event_id):

    event = get_object_or_404(
        Event,
        id=event_id
    )

    registration_count = EventRegistration.objects.filter(
        event=event
    ).count()

    remaining_seats = event.participants - registration_count

    return render(
        request,
        "events/event_detail.html",
        {
            "event": event,
            "registration_count": registration_count,
            "remaining_seats": remaining_seats,
        }
    )


@login_required
def register_event(request, event_id):

    event = get_object_or_404(
        Event,
        id=event_id
    )

    # Registration is allowed only before the event starts
    if event.status != "Upcoming":
        return render(
            request,
            "events/registration_closed.html",
            {
                "event": event
            }
        )

    if event.registration_type != "OUR_FORM":
        return redirect(event.registration_link)

    if EventRegistration.objects.filter(
        user=request.user,
        event=event
    ).exists():

        return render(
            request,
            "events/already_registered.html",
            {
                "event": event
            }
        )

    registration_count = EventRegistration.objects.filter(
        event=event
    ).count()

    if registration_count >= event.participants:

        return render(
            request,
            "events/registration_full.html",
            {
                "event": event
            }
        )

    if request.method == "POST":

        form = EventRegistrationForm(request.POST)

        if form.is_valid():

            registration = form.save(
                commit=False
            )

            registration.user = request.user
            registration.event = event

            registration.save()

            return render(
                request,
                "events/success.html",
                {
                    "success_title": "Registration Successful!",
                    "success_message": f"You have successfully registered for {event.name}.",
                    "success_url": reverse("event_detail", kwargs={"event_id": event.id}),
                    "event": event
                }
            )

    else:

        form = EventRegistrationForm()

    return render(
        request,
        "events/event_registration.html",
        {
            "form": form,
            "event": event
        }
    )



@login_required
def my_registrations(request):
  registrations = EventRegistration.objects.filter(
    user = request.user
  ).select_related("event")
  return render(
    request,
    "events/my_registrations.html",
    {
      "registrations":registrations
    }
  )


@login_required
def club_dashboard(request):

    clubs = Club.objects.filter(
        clubmember__user=request.user,
        clubmember__membership_type="CORE"
    ).prefetch_related(
        "event_set"
    )

    for club in clubs:

        for event in club.event_set.all():

            event.registration_count = EventRegistration.objects.filter(
                event=event
            ).count()

            # Event status:
            # Upcoming / Ongoing / Completed
            event.event_status = event.status

        membership = club.clubmember_set.filter(
            user=request.user
        ).first()

        club.user_is_president = (
            membership.is_president
            if membership
            else False
        )

    return render(
        request,
        "events/club_dashboard.html",
        {
            "clubs": clubs
        }
    )


@login_required
def edit_event(request, event_id):

    event = get_object_or_404(
        Event,
        id=event_id
    )

    if not is_core_member(
        request.user,
        event.club
    ):
        return render(
            request,
            "events/no_permission.html"
        )

    # Only upcoming events can be edited
    if event.status != "Upcoming":
        return render(
            request,
            "events/no_permission.html"
        )

    if request.method == "POST":

        form = EventForm(
            request.POST,
            request.FILES,
            instance=event
        )

        if form.is_valid():

            form.save()

            return redirect(
                "club_dashboard"
            )

    else:

        form = EventForm(
            instance=event
        )

    return render(
        request,
        "events/edit_event.html",
        {
            "form": form,
            "event": event
        }
    )



@login_required
def delete_event(request, event_id):

    event = get_object_or_404(
        Event,
        id=event_id
    )

    if not is_core_member(
        request.user,
        event.club
    ):
        return render(
            request,
            "events/no_permission.html"
        )

    # Only upcoming events can be deleted
    if event.status != "Upcoming":
        return render(
            request,
            "events/no_permission.html"
        )

    if request.method == "POST":

        event.delete()

        return redirect(
            "club_dashboard"
        )

    return render(
        request,
        "events/delete_event.html",
        {
            "event": event
        }
    )




@login_required
def student_dashboard(request):

    registrations = EventRegistration.objects.filter(
        user=request.user
    ).select_related(
        "event",
        "event__club",
        "event__venue"
    ).order_by(
        "event__date",
        "event__start_time"
    )

    upcoming_registrations = [
        registration
        for registration in registrations
        if registration.event.status == "Upcoming"
    ]

    past_registrations = [
        registration
        for registration in registrations
        if registration.event.status == "Completed"
    ]

    return render(
        request,
        "events/student_dashboard.html",
        {
            "registrations": registrations,
            "upcoming_registrations": upcoming_registrations,
            "past_registrations": past_registrations,
            "total_registrations": registrations.count(),
            "upcoming_count": len(upcoming_registrations),
            "past_count": len(past_registrations),
        }
    )

def club_detail(request, club_id):

    club = get_object_or_404(
        Club,
        id=club_id,
        is_approved=True
    )

    events = Event.objects.filter(
        club=club
    ).order_by(
        "date",
        "start_time"
    )

    return render(
        request,
        "events/club_detail.html",
        {
            "club": club,
            "events": events
        }
    )


@login_required
def manage_members(request, club_id):

    club = get_object_or_404(Club, id=club_id)

    if not is_president(request.user, club):
        return render(
            request,
            "events/no_permission.html"
        )

    members = ClubMember.objects.filter(
        club=club
    ).select_related("user")

    search_form = StudentSearchForm()
    students = None

    if request.method == "GET":

        query = request.GET.get("search")

        if query:
            students = StudentProfile.objects.filter(
                Q(name__icontains=query) |
                Q(usn__icontains=query)
            ).select_related("user")

    return render(
        request,
        "events/manage_members.html",
        {
            "club": club,
            "members": members,
            "search_form": search_form,
            "students": students,
        }
    )

@login_required
def edit_member(request, club_id, member_id):

    club = get_object_or_404(Club, id=club_id)

    if not is_president(request.user, club):
        return render(
            request,
            "events/no_permission.html"
        )

    member = get_object_or_404(
        ClubMember,
        id=member_id,
        club=club
    )

    # President cannot edit their own membership here
    if member.user == request.user:
        return render(
            request,
            "events/no_permission.html"
        )

    if request.method == "POST":

        form = AddCoreMemberForm(request.POST)

        if form.is_valid():

            member.position = form.cleaned_data["position"]
            member.save()

            return redirect(
                "manage_members",
                club_id=club.id
            )

    else:

        form = AddCoreMemberForm(
            initial={
                "user": member.user,
                "position": member.position
            }
        )

    return render(
        request,
        "events/edit_member.html",
        {
            "club": club,
            "member": member,
            "form": form,
        }
    )


@login_required
def remove_member(request, club_id, member_id):

    club = get_object_or_404(
        Club,
        id=club_id
    )

    if not is_president(request.user, club):
        return render(
            request,
            "events/no_permission.html"
        )

    member = get_object_or_404(
        ClubMember,
        id=member_id,
        club=club
    )

    # President cannot remove themselves
    if member.is_president:
        return render(
            request,
            "events/no_permission.html"
        )

    if request.method == "POST":

        member.delete()

        return redirect(
            "manage_members",
            club_id=club.id
        )

    return render(
        request,
        "events/remove_member.html",
        {
            "club": club,
            "member": member,
        }
    )



@login_required
def add_core_member(request, club_id, student_id):

    club = get_object_or_404(
        Club,
        id=club_id
    )

    if not is_president(request.user, club):
        return render(
            request,
            "events/no_permission.html"
        )

    student = get_object_or_404(
        StudentProfile,
        id=student_id
    )

    existing_member = ClubMember.objects.filter(
        user=student.user,
        club=club
    ).first()

    if existing_member:
        return render(
            request,
            "events/member_already_exists.html",
            {
                "club": club,
                "student": student,
                "member": existing_member,
            }
        )

    if request.method == "POST":

        form = AddCoreMemberForm(request.POST)

        if form.is_valid():

            ClubMember.objects.create(
                user=student.user,
                club=club,
                membership_type="CORE",
                is_president=False,
                position=form.cleaned_data["position"]
            )

            return redirect(
                "manage_members",
                club_id=club.id
            )

    else:

        form = AddCoreMemberForm()

    return render(
        request,
        "events/add_core_member.html",
        {
            "club": club,
            "student": student,
            "form": form,
        }
    )


@login_required
def change_president(request, club_id):

    club = get_object_or_404(
        Club,
        id=club_id
    )

    if not is_president(request.user, club):
        return render(
            request,
            "events/no_permission.html"
        )

    current_president = ClubMember.objects.filter(
        user=request.user,
        club=club,
        is_president=True
    ).first()

    students = None

    if request.method == "GET":

        query = request.GET.get("search", "").strip()

        if query:
            students = StudentProfile.objects.filter(
                Q(name__icontains=query) |
                Q(usn__icontains=query)
            ).exclude(
                user=request.user
            ).select_related("user")

    return render(
        request,
        "events/change_president.html",
        {
            "club": club,
            "current_president": current_president,
            "students": students,
        }
    )



@login_required
@transaction.atomic
def confirm_president_change(request, club_id, student_id):

    club = get_object_or_404(
        Club,
        id=club_id
    )

    if not is_president(request.user, club):
        return render(
            request,
            "events/no_permission.html"
        )

    current_president = get_object_or_404(
        ClubMember,
        user=request.user,
        club=club,
        is_president=True
    )

    student = get_object_or_404(
        StudentProfile,
        id=student_id
    )

    if student.user == request.user:
        return render(
            request,
            "events/no_permission.html"
        )

    # Show confirmation page
    if request.method == "GET":

        existing_member = ClubMember.objects.filter(
            user=student.user,
            club=club
        ).first()

        return render(
            request,
            "events/confirm_president_change.html",
            {
                "club": club,
                "student": student,
                "existing_member": existing_member,
            }
        )

    # Process the actual change
    if request.method == "POST":


        old_president_action = request.POST.get(
            "old_president_action"
        )

        if old_president_action not in [
            "CORE",
            "MEMBER",
            "REMOVE"
        ]:
            return redirect(
                "change_president",
                club_id=club.id
            )

        # ------------------------------------------------
        # STEP 1: Remove President status from old President
        # ------------------------------------------------

        if old_president_action == "CORE":

            current_president.is_president = False
            current_president.membership_type = "CORE"
            current_president.position = ""
            current_president.save()

        elif old_president_action == "MEMBER":

            current_president.is_president = False
            current_president.membership_type = "MEMBER"
            current_president.position = ""
            current_president.save()

        elif old_president_action == "REMOVE":

            current_president.delete()

        # ------------------------------------------------
        # STEP 2: Make selected student the new President
        # ------------------------------------------------

        new_president = ClubMember.objects.filter(
            user=student.user,
            club=club
        ).first()

        if not new_president:

            ClubMember.objects.create(
                user=student.user,
                club=club,
                membership_type="CORE",
                is_president=True,
                position=""
            )

        else:

            new_president.membership_type = "CORE"
            new_president.is_president = True
            new_president.position = ""

            new_president.save()

        messages.success(
            request,
            f"{student.name} is now the President of {club.name}."
        )

        return redirect("club_dashboard")