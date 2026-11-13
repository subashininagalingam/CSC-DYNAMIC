"""Bookable courses: listing, detail, booking, payment and confirmation."""
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from ..data.prospectus import PROGRAMS
from ..forms import CourseBookingForm, PaymentSubmissionForm
from ..models import BookCourse, CourseBooking

def courses_page(request):
    """Show all active bookable courses."""
    courses = BookCourse.objects.filter(is_active=True)
    return render(request, 'main/courses/list.html', {
        'courses': courses,
        'programs': PROGRAMS,
    })


def course_detail(request, course_id):
    course = get_object_or_404(
        BookCourse,
        id=course_id,
        is_active=True,
    )
    return render(
        request,
        'main/courses/detail.html',
        {'course': course},
    )


def book_course(request, course_id):
    course = get_object_or_404(
        BookCourse,
        id=course_id,
        is_active=True
    )

    if request.method == 'POST':
        form = CourseBookingForm(request.POST)

        if form.is_valid():
            booking = form.save(commit=False)
            booking.course = course
            booking.save()

            booked_on_str = timezone.now().strftime('%d %b %Y  %I:%M %p')

            # Email to Student
            student_msg = f"""
Dear {booking.student_name},

Thank you for booking with CSC Anna Nagar Institute! 🎉

Booking Reference : {booking.booking_ref}
Course Name       : {course.name}
Duration          : {course.duration}
Amount to Pay     : ₹{course.offer_fee}
Booked On         : {booked_on_str}

Please complete your payment to confirm your seat.
"""
            send_mail(
                subject=f'Booking Confirmed — {course.name} | CSC Anna Nagar [{booking.booking_ref}]',
                message=student_msg,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[booking.email],
                fail_silently=True,
            )

            return redirect(
                'course_payment',
                booking_id=booking.id
            )
    else:
        form = CourseBookingForm()

    return render(
        request,
        'main/courses/register.html',
        {
            'course': course,
            'form': form,
        }
    )


def course_payment(request, booking_id):
    booking = get_object_or_404(
        CourseBooking,
        id=booking_id
    )

    if booking.payment_status == 'paid':
        return redirect(
            'booking_success',
            booking_id=booking.id
        )

    if request.method == 'POST':
        form = PaymentSubmissionForm(
            request.POST,
            request.FILES,
            instance=booking
        )

        if form.is_valid():
            payment = form.save(commit=False)
            payment.payment_status = 'submitted'
            payment.save()

            return redirect(
                'booking_success',
                booking_id=booking.id
            )
    else:
        form = PaymentSubmissionForm(instance=booking)

    return render(
        request,
        'main/courses/payment.html',
        {
            'booking': booking,
            'form': form,
        }
    )


def booking_success(request, booking_id):
    """Thank-you page shown after successful booking."""
    booking = get_object_or_404(CourseBooking, id=booking_id)
    return render(request, 'main/courses/success.html', {'booking': booking})
