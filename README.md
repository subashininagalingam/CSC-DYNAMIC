# CSC Anna Nagar - Website

Django website for **CSC Computer Software College, Anna Nagar** - courses, SAT scholarship
registration, offers, workshops, careers, placement and an admin-managed team page.

## Requirements
Python 3.12+ with the pinned Django 6.0. On older Python (3.10 / 3.11) change the Django line in `requirements.txt` to `Django==5.2.19` - the site works on both.

## Run locally
```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
Open http://127.0.0.1:8000 - admin panel at `/admin/` (`python manage.py createsuperuser`).

## Folder structure
```
csc_dynamic/
├── manage.py
├── requirements.txt          dependencies (UTF-8)
├── .env.example              environment variables (copy, do not commit real secrets)
├── institute_site/           project config: settings.py, urls.py, wsgi.py
├── main/                     the one Django app
│   ├── models.py  forms.py  admin.py  urls.py  utils.py
│   ├── sitemaps.py           /sitemap.xml
│   ├── context_processors.py site-wide phone / e-mail / address / SEO defaults  <- edit contact info HERE
│   ├── data/prospectus.py    all 17 programmes from the Prospectus 2026         <- edit course syllabus HERE
│   ├── views/                one file per area: home, pages, offers, team, courses, programs, workshops, careers, seo
│   ├── migrations/
│   ├── templates/main/
│   │   ├── base.html         page shell + SEO tags
│   │   ├── partials/         topbar (scrolling highlights), navbar, footer, sat_form, review_card
│   │   ├── pages/            home, about, offers, team, contact, achievements, placement, inspiration, registration, reviews
│   │   ├── courses/          list, detail, register, payment, success, programs, program_detail
│   │   ├── workshops/        list, detail, register
│   │   └── careers/          list
│   └── static/main/
│       ├── css/base/         tokens (logo colours), reset, typography
│       ├── css/layout/       layout, header, footer
│       ├── css/components/   buttons, forms, cards, ui
│       ├── css/pages/        one stylesheet per page group
│       ├── js/               main.js (site behaviour), home.js (slider, offer popup, programme details), form-validation.js
│       ├── images/  videos/
├── media/                    files uploaded from the admin (team photos, courses, resumes ...)
└── docs/legacy/              the ORIGINAL templates / css / views, kept for reference
```

## Admin: what you can manage
| Admin section | Where it shows |
|---|---|
| **Team members** | `/team/` only (never on the home page). Set Group, Order, tick/untick *Is active*. |
| **Home slides** | The 4-slide slider on the home page. Change text, picture, button, order, or untick *Is active*. |
| **Special offers** | `/offers/` page, and as a **popup on the home page** when *Show popup* is ticked (expired offers hide automatically via *Valid until*). |
| **Book courses** | `/courses/` and `/offers/` (a course with offer fee below original fee is listed as an offer). |
| SAT bookings, course bookings, workshops, careers, reviews, achievements, placement | as before |

## Design
Colours come from the CSC logo: indigo `#272173` and a soft light yellow derived from the logo yellow (see `css/base/tokens.css`).
Change a token there and the whole site follows.

## Deploying
1. Set the variables from `.env.example` on your host.
2. `python manage.py collectstatic --noinput` and `python manage.py migrate`.
3. Set `DJANGO_DEBUG=False`. Note: uploaded media is only served by Django while DEBUG is on -
   in production serve `/media/` from your host's disk/storage or a CDN.
4. Submit `https://your-domain/sitemap.xml` in Google Search Console.
