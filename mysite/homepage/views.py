from django.shortcuts import render

from .forms import LandingPageForm


def landing_page(request):
    context = {}
    if request.method == 'POST':
        form = LandingPageForm(request.POST)
        if form.is_valid():
            context['submitted'] = True
            form.save()
    else:
        form = LandingPageForm()
    context['form'] = form
    return render(request, 'homepage/landing_page.html', context=context)


