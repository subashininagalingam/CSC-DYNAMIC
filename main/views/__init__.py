"""Views are grouped by area of the site. URLs import from here."""
from .home import home
from .pages import about, achievements_view, reviews_view, placement, inspiration, contact
from .offers import offers, registration
from .team import team
from .courses import courses_page, course_detail, book_course, course_payment, booking_success
from .programs import program_list, program_detail
from .workshops import workshop_view, workshop_detail, workshop_register
from .careers import career_list, apply_job
from .seo import robots_txt
