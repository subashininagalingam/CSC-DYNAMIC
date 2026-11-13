"""Static / informational pages: about, achievements, reviews, placement,
inspiration and the contact form."""
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from ..forms import ContactForm
from ..models import Review, Achievement, PlacementStep, PlacementService

def about(request):
    return render(request, 'main/pages/about.html')


def achievements_view(request):
    achievements = Achievement.objects.all()
    return render(request, 'main/pages/achievements.html', {'achievements': achievements})


def reviews_view(request):
    reviews = Review.objects.order_by('-created_at')
    return render(request, 'main/pages/reviews.html', {'reviews': reviews})


def placement(request):
    return render(request, 'main/pages/placement.html', {
        'steps': PlacementStep.objects.filter(is_active=True),
        'services': PlacementService.objects.filter(is_active=True),
    })


def inspiration(request):
    return render(request, 'main/pages/inspiration.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():

            contact_msg = form.save()

            name = contact_msg.name
            phone = contact_msg.phone
            email = contact_msg.email
            message = contact_msg.message

            try:
                # Email to Admin
                send_mail(
                    subject=f'[CSC Anna Nagar] New Enquiry from {name}',

                    message=f"""
New contact form submission:

Name    : {name}
Phone   : {phone}
Email   : {email}

Message:
{message}
""",

                    from_email=settings.DEFAULT_FROM_EMAIL,

                    recipient_list=[
                        'subanagalingam.dev@gmail.com'
                    ],

                    fail_silently=False,
                )

                # Auto Reply to Client
                send_mail(
                    subject='Thank you for contacting CSC Anna Nagar!',

                    message=f"""
Dear {name},

Thank you for contacting CSC Anna Nagar.

We have received your message. Our team will contact you soon.

Your Message:
{message}

Contact: +91 9940909056

Best Regards,
CSC Anna Nagar Team
""",

                    from_email=settings.DEFAULT_FROM_EMAIL,

                    recipient_list=[email],

                    fail_silently=False,
                )

                messages.success(
                    request,
                    "Your message has been sent successfully!"
                )

            except Exception as e:

                print("SMTP EMAIL ERROR:", str(e))

                messages.warning(
                    request,
                    "Your enquiry has been saved. Email notification is temporarily unavailable."
                )

            return redirect('contact')

        else:
            messages.error(
                request,
                'Please fix the errors below and try again.'
            )

    else:
        form = ContactForm()

    return render(
        request,
        'main/pages/contact.html',
        {'form': form}
    )
