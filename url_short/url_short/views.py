from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponse
from .forms import Url
from .models import UrlData
import random, string


def index(request):
    return HttpResponse("Hello World")

def urlShort(request):
    if request.method == 'POST':
        form = Url(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            new_url, created = UrlData.objects.get_or_create(url=url)
            if created:
                slug = ''.join(random.choice(string.ascii_letters) for x in range(10))
                new_url.slug = slug
                new_url.save()

            shortened_url = request.build_absolute_uri(f'/url_shortener/{new_url.slug}')
            return JsonResponse({'shortened_url': shortened_url})

        return JsonResponse({'error': 'Invalid form submission'}, status=400)
    else:
        form = Url()
    data = UrlData.objects.all()
    context = {
        'form': form,
        'data': data
    }
    return render(request, 'index.html', context)

def urlRedirect(request, slugs):
    try:
        data = UrlData.objects.get(slug=slugs)
        if data.url.startswith('/'):
            # If it's a relative path, prepend the full domain
            domain = request.build_absolute_uri('/')[:-1]  # This gets the full domain with protocol (e.g., 'http://example.com')
            url = f'{domain}{data.url}'  # Prepend the domain to the relative path
        else:
            # If it's already a full URL, use it as is
            url = data.url
        return redirect(url)
    
    except UrlData.DoesNotExist:
        return HttpResponse("URL not found", status=404)