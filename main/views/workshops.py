"""Workshops: listing, detail and registration."""
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from ..forms import WorkshopRegistrationForm
from ..models import Workshop, UpcomingWorkshop, WorkshopRegistration

def workshop_view(request):
    workshop = Workshop.objects.order_by('-created_at')
    upcoming = UpcomingWorkshop.objects.filter(
        is_active=True,
        date__gte=timezone.localdate()
    )
    return render(request, 'main/workshops/list.html', {
        'workshop': workshop,
        'upcoming': upcoming,
    })


def workshop_detail(request, pk):
    w = get_object_or_404(UpcomingWorkshop, pk=pk, is_active=True)
    return render(request, 'main/workshops/detail.html', {'w': w})


def workshop_register(request, pk):
    w = get_object_or_404(UpcomingWorkshop, pk=pk, is_active=True)

    if w.seats_left() == 0:
        messages.error(request, "Sorry, this workshop is full.")
        return redirect('workshop_detail', pk=w.pk)

    if request.method == 'POST':
        form = WorkshopRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            if WorkshopRegistration.objects.filter(workshop=w, email=email).exists():
                messages.error(request, "You have already registered for this workshop.")
                return redirect('workshop_detail', pk=w.pk)

            reg = form.save(commit=False)
            reg.workshop = w
            reg.save()

            send_mail(
                subject=f'Workshop Registration - {w.title}',
                message=(
                    f"Dear {reg.name},\n\n"
                    f"Thank you for registering for {w.title} on {w.date:%d %b %Y}.\n"
                    f"Our team will contact you to confirm your seat.\n\n"
                    f"CSC Anna Nagar\nPhone: +91 9940909056"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[reg.email],
                fail_silently=True,
            )
            send_mail(
                subject=f'New Workshop Registration - {w.title}',
                message=(
                    f"Name: {reg.name}\nEmail: {reg.email}\nMobile: {reg.mobile}\n"
                    f"Workshop: {w.title} ({w.date:%d %b %Y})"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['annanagarcsc2024@gmail.com'],
                fail_silently=True,
            )

            messages.success(
                request,
                f"Thank you {reg.name}! You are registered for {w.title}. We will contact you soon."
            )
            return redirect('workshop_detail', pk=w.pk)
    else:
        form = WorkshopRegistrationForm()

    return render(request, 'main/workshops/register.html', {'w': w, 'form': form})
