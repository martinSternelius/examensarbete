# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from housingtrader.forms import ListingOfferedForm, ListingWantedForm, CompleteListingForm
from housingtrader.models import Listing

@login_required
def index(request):
    listings = Listing.objects.filter(user=request.user)
    return render(request, 'housingtrader/index.html',  {'listings':listings})

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
                complete_form = CompleteListingForm(request.POST, user=request.user)
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
