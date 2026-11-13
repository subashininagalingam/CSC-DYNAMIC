"""Home page."""
from django.contrib import messages
from django.shortcuts import render, redirect
from django.templatetags.static import static
from django.urls import reverse
from django.utils import timezone

from ..forms import DemoForm, SatBookingForm, TN_DISTRICTS
from ..models import Review, Achievement, Workshop, Course, HomeSlide, SpecialOffer
from ..data.prospectus import PROGRAMS, get_program
from ..utils import send_demo_email


SLIDE_FALLBACKS = [
    'main/images/lab1.jpg', 'main/images/hallno1.jpeg',
    'main/images/gallery-2.jpg', 'main/images/lab3.jpg',
]


def _quick_program(p):
    """Small, JSON-friendly summary used by the animated programme pop-up."""
    return {
        'slug': p['slug'], 'code': p['code'], 'name': p['name'], 'level': p['level'],
        'audience': p['audience'], 'prerequisites': p.get('prerequisites', ''),
        'objective': p['objective'], 'overview': p['overview'],
        'tools': p['tools'],
        'modules': [{'section': sec['title'], 'names': [b['title'] for b in sec['blocks']]} for sec in p['sections']],
        'module_count': p['module_count'], 'topic_count': p['topic_count'],
        'url': reverse('program_detail', args=[p['slug']]),
    }


def home(request):
    if request.method == 'POST' and 'demo_submit' in request.POST:
        form = DemoForm(request.POST)
        if form.is_valid():
            demo = form.save()
            try:
                send_demo_email(
                    name=demo.name,
                    mobile=demo.mobile,
                    email=demo.email,
                    description=demo.description,
                )
            except Exception as e:
                print(f"Email error: {e}")

            messages.success(
                request,
                f'Thank you {demo.name}! Demo booked. We will contact you soon.'
            )
            return redirect('home')
    else:
        form = DemoForm()

    featured = [get_program(s) for s in ('hdfd', 'dfpd', 'adad', 'dca-tally', 'dfjd', 'adda')]
    today = timezone.localdate()
    slides = [
        {'slide': sl, 'img': sl.image.url if sl.image else static(SLIDE_FALLBACKS[i % len(SLIDE_FALLBACKS)])}
        for i, sl in enumerate(HomeSlide.objects.filter(is_active=True))
    ]
    popup_offers = [
        o for o in SpecialOffer.objects.filter(is_active=True, show_popup=True)
        if not o.valid_until or o.valid_until >= today
    ]
    featured_list = [p for p in featured if p]
    context = {
        'form': form,
        'slides': slides,
        'popup_offers': popup_offers,
        'quick_programs': [_quick_program(p) for p in featured_list],
        'sat_form': SatBookingForm(),
        'districts': TN_DISTRICTS,
        'featured_programs': [p for p in featured if p],
        'program_total': len(PROGRAMS),
        'reviews': Review.objects.order_by('-created_at')[:6],
        'achievements': Achievement.objects.all(),
        'workshops': Workshop.objects.order_by('-created_at')[:6],
        'courses': Course.objects.all(),
    }
    return render(request, 'main/pages/home.html', context)
