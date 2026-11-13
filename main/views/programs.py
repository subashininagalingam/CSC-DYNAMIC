"""Programme catalogue built from the CSC Prospectus 2026."""
from django.http import Http404
from django.shortcuts import render

from ..data import prospectus as data


def program_list(request):
    return render(request, 'main/courses/programs.html', {
        'programs': data.PROGRAMS,
        'categories': data.CATEGORIES,
        'journey': data.JOURNEY,
        'credentials_intro': data.CREDENTIALS_INTRO,
        'credentials': data.CREDENTIALS,
        'govt_trained': data.GOVT_TRAINED,
        'partners': data.PARTNERS,
    })


def program_detail(request, slug):
    program = data.get_program(slug)
    if program is None:
        raise Http404('Programme not found')
    related = [p for p in data.PROGRAMS if p['category'] == program['category'] and p['slug'] != slug][:3]
    return render(request, 'main/courses/program_detail.html', {
        'p': program,
        'related': related,
        'chatgpt_text': data.CHATGPT_TEXT,
    })
