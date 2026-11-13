"""Site-wide values available in every template as ``site`` (contact details,
social links and SEO defaults). Edit here once instead of in every template."""
from django.conf import settings

SITE = {
    'name': 'CSC Anna Nagar',
    'full_name': 'CSC Computer Software College, Anna Nagar',
    'tagline': 'Computer Education & IT Training in Anna Nagar, Chennai',
    'phone': '+91 9940909056',
    'phone_link': '+919940909056',
    'phone_short': '99409 09056',
    'email': 'annanagarcsc2024@gmail.com',
    'whatsapp': 'https://wa.me/919940909056?text=Hi%20CSC%20Anna%20Nagar%2C%20I%20want%20to%20know%20more%20about%20your%20courses.',
    'address_lines': ['AP-814, "G" Block, 1st Street,', 'Near Anna Nagar Tower, Near Saravana Bhavan Hotel,', 'Anna Nagar, Chennai'],
    'address_inline': 'AP-814, "G" Block, 1st Street, Near Anna Nagar Tower, Near Saravana Bhavan Hotel, Anna Nagar, Chennai',
    'postal_code': '600040',
    'map_link': 'https://www.google.com/maps?q=CSC+Computer+Education,+AP-814,+G+Block,+1st+Street,+Anna+Nagar,+Chennai+600040',
    'facebook': 'https://www.facebook.com/csc_anna_nagar/',
    'instagram': 'https://www.instagram.com/csc_anna_nagar/',
    'linkedin': 'https://www.linkedin.com/in/cscannanagar-computer-education-170a47336/',
    'default_description': (
        'CSC Anna Nagar - Computer Software College in Chennai. Job-oriented computer courses: '
        'Full Stack, Python, Java, Data Science, Tally, MS Office. Project-based training, '
        'placement support and SAT 2026 scholarship up to 75%.'
    ),
}


def site(request):
    base = getattr(settings, 'SITE_URL', '').rstrip('/') or request.build_absolute_uri('/').rstrip('/')
    return {
        'site': SITE,
        'site_url': base,
        'canonical_url': base + request.path,
        'og_image_url': base + settings.STATIC_URL + 'main/images/csc.webp',
    }
