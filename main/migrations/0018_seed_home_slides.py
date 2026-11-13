from django.db import migrations

SLIDES = [
    ("Empowering Learners Through Technology",
     "Building practical skills, confidence, and career readiness through quality computer education",
     "About CSC", "/about/"),
    ("Career programmes for every learner",
     "Job-oriented programmes from the CSC Prospectus 2026 - from MS Office and Tally to Full Stack and AI.",
     "Explore programmes", "/courses/programs/"),
    ("From Skills to Opportunities",
     "Build the skills you need, prepare with confidence, and receive guidance as you take your next step toward the workplace.",
     "Placement support", "/placement/"),
    ("Learn. Experience. Build.",
     "Explore workshops and hands-on learning experiences designed to connect students with practical technology.",
     "View workshops", "/workshops/"),
]


def seed(apps, schema_editor):
    HomeSlide = apps.get_model("main", "HomeSlide")
    if HomeSlide.objects.exists():
        return
    for i, (t, s, b, u) in enumerate(SLIDES, start=1):
        HomeSlide.objects.create(title=t, subtitle=s, button_text=b, button_url=u, order=i, is_active=True)


def unseed(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [("main", "0017_home_slide_and_offer_popup")]
    operations = [migrations.RunPython(seed, unseed)]
