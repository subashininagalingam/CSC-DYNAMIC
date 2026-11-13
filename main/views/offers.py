"""Offers page and the SAT scholarship registration."""
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone

from ..forms import SatBookingForm, TN_DISTRICTS
from ..models import BookCourse, SpecialOffer


def registration(request):
    if request.method == 'POST':
        form = SatBookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful!')
            return redirect('courses')  
    else:
        form = SatBookingForm()
    return render(request, 'main/pages/registration.html', {
        'form': form,
        'districts': TN_DISTRICTS,
    })


def offers(request):
    """Every offer in one place: SAT scholarship, course fee offers, special offers."""
    today = timezone.localdate()
    special = [
        o for o in SpecialOffer.objects.filter(is_active=True)
        if not o.valid_until or o.valid_until >= today
    ]
    course_offers = [
        c for c in BookCourse.objects.filter(is_active=True)
        if c.original_fee and c.offer_fee and c.original_fee > c.offer_fee
    ]
    return render(request, 'main/pages/offers.html', {
        'special_offers': special,
        'course_offers': course_offers,
    })
