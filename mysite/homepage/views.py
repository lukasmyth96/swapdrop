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

    # serve different template on desktop and mobile
    template = 'homepage/landing_page_mobile.html' if request.user_agent.is_mobile else 'homepage/landing_page.html'

    return render(request, template, context=context)


def terms_of_service(request):
    return render(request, 'homepage/terms_of_service.html')


def privacy(request):
    return render(request, 'homepage/privacy.html')


def faq(request):
    if request.user.is_authenticated:
        return render(request, 'homepage/faq_logged_in.html')
    else:
        return render(request, 'homepage/faq_logged_out.html')


