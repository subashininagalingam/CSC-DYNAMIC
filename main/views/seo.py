"""robots.txt"""
from django.http import HttpResponse
from django.urls import reverse


def robots_txt(request):
    lines = [
        'User-agent: *',
        'Disallow: /admin/',
        'Disallow: /courses/payment/',
        'Disallow: /courses/success/',
        'Allow: /',
        '',
        f"Sitemap: {request.build_absolute_uri(reverse('sitemap'))}",
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')
