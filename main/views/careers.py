"""Careers: open positions and job applications."""
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from ..forms import JobApplicationForm
from ..models import Career, JobApplication

def career_list(request):
    """Show all active job openings."""
    careers = Career.objects.filter(is_active=True).order_by('-posted_on')
    return render(request, 'main/careers/list.html', {'careers': careers})


def apply_job(request, career_id):
    """Handle job application form submission via POST."""
    career = get_object_or_404(Career, id=career_id, is_active=True)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.career = career
            application.save()

            applicant_msg = f"""
Dear {application.name},

Thank you for applying to CSC Anna Nagar Institute! 🎉

We have received your application for the role of:
✅ {career.role} ({career.employment_type})

Your Application Details:
──────────────────────────────────────
Name                  : {application.name}
Email                 : {application.email}
Mobile                : {application.mobile}
Highest Qualification : {application.highest_qualification}
Passed Out Year       : {application.passed_out_year}
Applied For           : {career.role}
Applied On            : {timezone.now().strftime('%d %b %Y  %I:%M %p')}
──────────────────────────────────────

Our team will review your application and contact you soon.

Best Regards,
CSC Anna Nagar Institute
AP-814, "G" Block, 1st Street, Anna Nagar, Chennai.
Phone : 9940909056
Email : annanagarcsc2024@gmail.com
"""
            send_mail(
                subject=f'Application Received — {career.role} | CSC Anna Nagar',
                message=applicant_msg,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[application.email],
                fail_silently=True,
            )

            institute_msg = f"""
New Job Application Received
──────────────────────────────────────
Role Applied          : {career.role} ({career.employment_type})
──────────────────────────────────────
Applicant Name        : {application.name}
Email                 : {application.email}
Mobile                : {application.mobile}
Highest Qualification : {application.highest_qualification}
Passed Out Year       : {application.passed_out_year}
Cover Letter          : {application.cover_letter if application.cover_letter else '(not provided)'}
Applied On            : {timezone.now().strftime('%d %b %Y  %I:%M %p')}
──────────────────────────────────────
Resume is attached to this email.
"""
            email_with_resume = EmailMessage(
                subject=f'New Application — {career.role} from {application.name}',
                body=institute_msg,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=['annanagarcsc2024@gmail.com'],
            )
            try:
                application.resume.open()
                email_with_resume.attach(
                    application.resume.name.split('/')[-1],
                    application.resume.read(),
                    'application/octet-stream'
                )
                application.resume.close()
            except Exception:
                pass

            try:
                email_with_resume.send(fail_silently=False)
            except Exception as e:
                print(f"Institute email error: {e}")

            messages.success(
                request,
                f'Thank you {application.name}! Your application for "{career.role}" has been submitted successfully.'
            )
            return redirect('career')
        else:
            messages.error(request, 'Please fix the errors below and try again.')
            careers = Career.objects.filter(is_active=True)
            return render(request, 'main/careers/list.html', {
                'careers': careers,
                'form': form,
                'open_career': career_id,
            })

    return redirect('career')
