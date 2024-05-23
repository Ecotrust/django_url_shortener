from django.shortcuts import render, redirect
from django.http import HttpResponse
from url.forms import Url
from url.models import UrlData
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
                slug = ''.join(random.choice(string.ascii_letters)
                            for x in range(10))
                new_url.slug =slug
                new_url.save()
            return redirect('/')
    else:
        form = Url()
    data = UrlData.objects.all()
    context = {
        'form': form,
        'data': data
    }
    return render(request, 'index.html', context)

def urlRedirect(request, slugs):
    data = UrlData.objects.get(slug=slugs)
    # if the url doesn't start with http, it will be treated and a relative address, rather than absolute. It's 2024, we can assume 'https':
    if not 'http' == data.url[0:4]:
        url = 'https://{}'.format(data.url)
    else:
        url = data.url
    return redirect(url)