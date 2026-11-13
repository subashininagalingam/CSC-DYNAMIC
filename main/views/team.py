"""Our Team page (members are managed in the admin panel)."""
from django.shortcuts import render

from ..models import TeamMember


def team(request):
    members = TeamMember.objects.filter(is_active=True)
    sections = []
    for key, label in TeamMember.GROUP_CHOICES:
        people = [m for m in members if m.group == key]
        if people:
            sections.append({'key': key, 'label': label, 'members': people})
    return render(request, 'main/pages/team.html', {'sections': sections, 'total': members.count()})
