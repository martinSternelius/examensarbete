# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from housingtrader.forms import ListingOfferedForm, ListingWantedForm, CompleteListingForm
from housingtrader.models import Listing, TradeRequest
from django.db.models import Q

@login_required
def index(request):
    listings = Listing.objects.filter(user=request.user)
    trade_requests = TradeRequest.objects.filter(receiver__user=request.user, declined_by_receiver=0)
    return render(request, 'housingtrader/index.html',  {'listings':listings, 'trade_requests':trade_requests})

@login_required
def create_listing(request):
    offered_form = ListingOfferedForm()
    wanted_form = ListingWantedForm()
    if request.method == 'POST':
        offered_form = ListingOfferedForm(request.POST)
        wanted_form = ListingWantedForm(request.POST)
        try:
            offered_form.is_valid()
        finally:
            try:
                wanted_form.is_valid()
                complete_form = CompleteListingForm(data=request.POST, user=request.user)
                complete_form.save()
                return HttpResponseRedirect(reverse('housingtrader-index:index'))
            except:
                pass
        
    return render(request, 'housingtrader/create_listing.html', {'offered_form' : offered_form, 'wanted_form' : wanted_form})

@login_required
def edit_listing(request, listing_id):
    listing = get_object_or_404(Listing, user=request.user, pk=listing_id)
    offered_form = ListingOfferedForm(instance=listing)
    wanted_form = ListingWantedForm(instance=listing)
    if request.method == 'POST':
        offered_form = ListingOfferedForm(request.POST, instance=listing)
        wanted_form = ListingWantedForm(request.POST, instance=listing)
        try:
            offered_form.is_valid()
        finally:
            try:
                wanted_form.is_valid()
                complete_form = CompleteListingForm(data=request.POST, user=request.user, instance=listing)
                complete_form.save()
                return HttpResponseRedirect(reverse('housingtrader-index:index'))
            except:
                pass
    return render(request, 'housingtrader/create_listing.html', {'offered_form' : offered_form, 'wanted_form' : wanted_form})

@login_required
def find_trades(request, listing_id):
    listing = get_object_or_404(Listing, user=request.user, pk=listing_id)
    matched_listings = listing.find_matches()
    return render(request, 'housingtrader/find_trades.html', {'listing':listing, 'other_listings' : matched_listings})

@login_required
def detail(request, listing_id, other_listing_id):
    other_listing = get_object_or_404(Listing, pk=other_listing_id)
    return render(request, 'housingtrader/detail.html', {'listing':other_listing})

def search(request):
    if request.GET['submit']:
        search_listing = Listing()
        search_listing.w_county = request.GET['county']
        search_listing.w_types = ','.join(request.GET.getlist('types'))
        search_listing.w_min_area = request.GET['min_area']
        search_listing.w_min_rooms = request.GET['min_rooms']
        search_listing.w_max_rent = request.GET['max_rent']
        search_listing.w_has_fireplace = int(request.GET['has_fireplace'])
        search_listing.w_has_balcony = int(request.GET['has_balcony'])
        search_listing.w_has_elevator = int(request.GET['has_elevator'])
        search_listing.w_not_bottom_floor = int(request.GET['not_bottom_floor'])
        
        results = search_listing.listing_search()
        
        results = results.filter(
            Q(o_description__icontains = request.GET['text'])
            | Q(o_street_address__icontains = request.GET['text']) 
            | Q(o_postal_town__icontains = request.GET['text'])
        )
        
        return render(request, 'housingtrader/search_results.html', {'results':results})
