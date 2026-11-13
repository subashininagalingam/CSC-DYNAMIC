from django.contrib import admin
from .models import (
    DemoRequest, Review, Achievement, Workshop, ContactMessage, Course,
    Career, JobApplication,
    BookCourse, CourseBooking,
    PlacementStep, PlacementService,
    UpcomingWorkshop, WorkshopRegistration,
    SatBooking,  # Added from RP
    TeamMember, SpecialOffer, HomeSlide,
)
from django.utils.html import format_html

admin.site.register(DemoRequest)
admin.site.register(Review)
admin.site.register(Achievement)
admin.site.register(Workshop)
admin.site.register(ContactMessage)
admin.site.register(Course)


@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ['role', 'employment_type', 'location', 'salary', 'is_active', 'posted_on']
    list_filter = ['employment_type', 'is_active']
    search_fields = ['role', 'job_description']
    list_editable = ['is_active']
    ordering = ['-posted_on']


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'mobile', 'career', 'highest_qualification', 'passed_out_year', 'applied_on']
    list_filter = ['career']
    search_fields = ['name', 'email', 'mobile']
    readonly_fields = ['applied_on']
    ordering = ['-applied_on']


@admin.register(BookCourse)
class BookCourseAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'mode', 'level', 'duration',
        'original_fee', 'offer_fee', 'discount_percent', 'is_active',
    ]
    list_editable = ['category', 'mode', 'level', 'is_active']
    list_filter = ['category', 'mode', 'level', 'is_active']
    search_fields = ['name']

    def discount_percent(self, obj):
        return f"{obj.discount_percent()}% OFF"
    discount_percent.short_description = 'Discount'

    def booked_on_ist(self, obj):
        from django.utils import timezone
        return timezone.localtime(obj.booked_on).strftime('%d %b %Y, %I:%M %p')
    booked_on_ist.short_description = 'Booked On'
    booked_on_ist.admin_order_field = 'booked_on'



@admin.register(CourseBooking)
class CourseBookingAdmin(admin.ModelAdmin):
    list_display = (
        'booking_ref', 'student_name', 'email', 'course',
        'transaction_id', 'payment_status', 'booked_on',
    )
    list_filter = ('payment_status', 'booked_on')
    search_fields = ('booking_ref', 'student_name', 'email', 'transaction_id')


@admin.register(PlacementStep)
class PlacementStepAdmin(admin.ModelAdmin):
    list_display = ['order', 'title', 'description', 'is_active']
    list_editable = ['is_active']


@admin.register(PlacementService)
class PlacementServiceAdmin(admin.ModelAdmin):
    list_display = ['order', 'icon', 'title', 'description', 'is_active']
    list_editable = ['is_active']


@admin.register(UpcomingWorkshop)
class UpcomingWorkshopAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'start_time', 'mode', 'seats', 'is_active']
    list_editable = ['is_active']
    list_filter = ['mode', 'is_active']


@admin.register(WorkshopRegistration)
class WorkshopRegistrationAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'mobile', 'workshop', 'registered_on']
    list_filter = ['workshop']
    search_fields = ['name', 'email', 'mobile']
    readonly_fields = ['registered_on']


# ---- Added from RP ----
@admin.register(SatBooking)
class SatBookingAdmin(admin.ModelAdmin):
    list_display = ['name', 'mobile', 'email', 'qualification', 'district', 'area', 'timing', 'gender', 'created_at']
    list_filter = ['timing', 'gender', 'qualification', 'district']
    search_fields = ['name', 'mobile', 'email', 'area']
    readonly_fields = ['created_at']
    ordering = ['-created_at']


# ---- Team page ------------------------------------------------------------
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['photo_preview', 'name', 'designation', 'group', 'order', 'is_active']
    list_display_links = ['photo_preview', 'name']
    list_editable = ['order', 'is_active']
    list_filter = ['group', 'is_active']
    search_fields = ['name', 'designation']
    ordering = ['group', 'order', 'name']
    fieldsets = (
        ('Who is it?', {'fields': ('name', 'designation', 'group', 'photo')}),
        ('Details (optional)', {'fields': ('qualification', 'experience', 'bio', 'linkedin_url')}),
        ('Display', {'fields': ('order', 'is_active')}),
    )

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="width:44px;height:44px;object-fit:cover;border-radius:50%;" alt="">',
                obj.photo.url,
            )
        return '-'
    photo_preview.short_description = 'Photo'


# ---- Offers page ----------------------------------------------------------
@admin.register(SpecialOffer)
class SpecialOfferAdmin(admin.ModelAdmin):
    list_display = ['title', 'highlight', 'badge', 'valid_until', 'show_popup', 'order', 'is_active']
    list_editable = ['order', 'show_popup', 'is_active']
    list_filter = ['is_active', 'show_popup']
    search_fields = ['title', 'description']


# ---- Home page slider -----------------------------------------------------
@admin.register(HomeSlide)
class HomeSlideAdmin(admin.ModelAdmin):
    list_display = ['thumb', 'title', 'button_text', 'order', 'is_active']
    list_display_links = ['thumb', 'title']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'subtitle']
    fieldsets = (
        ('Slide text', {'fields': ('title', 'subtitle')}),
        ('Picture', {'fields': ('image',)}),
        ('Button (optional)', {'fields': ('button_text', 'button_url')}),
        ('Display', {'fields': ('order', 'is_active')}),
    )

    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:90px;height:44px;object-fit:cover;border-radius:6px;" alt="">', obj.image.url)
        return 'Default photo'
    thumb.short_description = 'Picture'
