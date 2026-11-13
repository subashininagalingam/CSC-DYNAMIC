from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.urls import path

from . import views
from .sitemaps import SITEMAPS

urlpatterns = [
    # -- Main pages ---------------------------------------------------------
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('achievements/', views.achievements_view, name='achievements'),
    path('reviews/', views.reviews_view, name='reviews'),
    path('placement/', views.placement, name='placement'),
    path('inspiration/', views.inspiration, name='inspiration'),
    path('team/', views.team, name='team'),

    # -- Offers & SAT scholarship -------------------------------------------
    path('offers/', views.offers, name='offers'),
    path('registration/', views.registration, name='registration'),

    # -- Workshops (singular + plural kept so no old link breaks) ------------
    path('workshop/', views.workshop_view, name='workshop'),
    path('workshops/', views.workshop_view, name='workshops'),
    path('workshop/<int:pk>/', views.workshop_detail, name='workshop_detail'),
    path('workshop/<int:pk>/register/', views.workshop_register, name='workshop_register'),

    # -- Careers --------------------------------------------------------------
    path('careers/', views.career_list, name='career'),
    path('careers/apply/<int:career_id>/', views.apply_job, name='apply_job'),

    # -- Courses: prospectus programmes --------------------------------------
    path('courses/programs/', views.program_list, name='programs'),
    path('courses/programs/<slug:slug>/', views.program_detail, name='program_detail'),

    # -- Courses: booking & payment -------------------------------------------
    path('courses/', views.courses_page, name='courses'),
    path('courses/details/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/book/<int:course_id>/', views.book_course, name='book_course'),
    path('courses/payment/<int:booking_id>/', views.course_payment, name='course_payment'),
    path('courses/success/<int:booking_id>/', views.booking_success, name='booking_success'),

    # -- SEO -------------------------------------------------------------------
    path('sitemap.xml', sitemap, {'sitemaps': SITEMAPS}, name='sitemap'),
    path('robots.txt', views.robots_txt, name='robots'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
