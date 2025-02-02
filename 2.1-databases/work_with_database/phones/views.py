from django.shortcuts import render, redirect

from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    sort = request.GET.get('sort')
    template = 'catalog.html'
    phones_objects = Phone.objects.all()
    phones = [p for p in phones_objects]
    if sort == 'name':
        phones.sort(key=lambda x: x.name)
    if sort == 'min_price':
        phones.sort(key=lambda x: x.price)
    if sort == 'max_price':
        phones.sort(key=lambda x: x.price, reverse=True)
    context = {
        'phones': phones,
    }
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    p = Phone.objects.get(slug=slug)
    context = {'phone': p}
    return render(request, template, context)
