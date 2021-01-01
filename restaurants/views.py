from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.conf import settings

import requests
import random

from . import utils


def index(request):
    if request.method == "POST":
        location = request.POST.get('address')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        radius = request.POST.get('radius')
        category = request.POST.get('categories')

        endpoint = "https://api.yelp.com/v3/businesses/search"
        headers = {"Authorization": f"Bearer {settings.YELP_API_KEY}"}
        parameters = {}

        # set search criteria depending on what information user filled out
        if category:
            parameters['categories'] = category
        # radius from kilometers to meters
        if radius:
            parameters['radius'] = int(radius) * 1000

        if location:
            parameters['location'] = location
        elif latitude and longitude:
            parameters['latitude'] = float(latitude)
            parameters['longitude'] = float(longitude)
        else:
            messages.error(request, 'No location has been entered')
            return HttpResponseRedirect(reverse('index'))

        try:
            resp = requests.get(endpoint, params=parameters, headers=headers).json()
            # display error message if zero results returned
            if resp['total'] == 0:
                messages.error(request, 'No restaurants of selected category within your specified search area')
                return HttpResponseRedirect(reverse('index'))
            else:
                # since only 20 businesses are returned, if total number of busineses exceed 20, set a random offset to get a wider variety of results
                if resp['total'] > 20:
                    offset = random.randint(0, resp['total'] - 20)
                    parameters['offset'] = offset
                    resp = requests.get(endpoint, params=parameters, headers=headers).json()

                # choose a random business
                business = resp['businesses'][random.randint(0, len(resp['businesses']) - 1)]
                return render(request, 'restaurants/business.html', {
                    'title': f"{business['name']} - Pick My Lunch",
                    'business': business
                })           
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.RequestException as err:
            print("Something else", err)

    categories = utils.list_categories("restaurants")

    return render(request, 'restaurants/index.html', {
        'categories': categories
    })

