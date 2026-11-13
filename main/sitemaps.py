"""XML sitemap for search engines (/sitemap.xml)."""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .data.prospectus import PROGRAMS
from .models import BookCourse, UpcomingWorkshop


class StaticPages(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return ['home', 'offers', 'programs', 'courses', 'about', 'placement', 'team',
                'workshop', 'achievements', 'career', 'inspiration', 'contact', 'registration']

    def location(self, name):
        return reverse(name)

    def priority(self, name):
        return {'home': 1.0, 'offers': 0.9, 'programs': 0.9, 'registration': 0.9}.get(name, 0.7)


class ProgramPages(Sitemap):
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return PROGRAMS

    def location(self, program):
        return reverse('program_detail', args=[program['slug']])


class CoursePages(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return BookCourse.objects.filter(is_active=True)

    def location(self, course):
        return reverse('course_detail', args=[course.id])


class WorkshopPages(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return UpcomingWorkshop.objects.filter(is_active=True)

    def location(self, w):
        return reverse('workshop_detail', args=[w.pk])


SITEMAPS = {
    'pages': StaticPages,
    'programs': ProgramPages,
    'courses': CoursePages,
    'workshops': WorkshopPages,
}
