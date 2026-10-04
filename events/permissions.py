from .models import ClubMember


def is_core_member(user, club):
    return ClubMember.objects.filter(
        user=user,
        club=club,
        membership_type="CORE"
    ).exists()


def is_president(user, club):
    return ClubMember.objects.filter(
        user=user,
        club=club,
        is_president=True
    ).exists()