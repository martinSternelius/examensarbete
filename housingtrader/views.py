# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.views.generic.edit import DeleteView
from housingtrader.forms import ListingOfferedForm, ListingWantedForm, CompleteListingForm, SearchForm
from housingtrader.models import Listing, TradeRequest
from django.db.models import Q
from string import strip

@login_required
def index(request):
    listings = Listing.objects.filter(user=request.user)
    trade_requests = TradeRequest.objects.filter(receiver__user=request.user, declined_by_receiver=False)
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
                return HttpResponseRedirect(reverse('housingtrader:index'))
            except:
                pass
        
    return render(request, 'housingtrader/create_listing.html', {'offered_form' : offered_form, 'wanted_form' : wanted_form})

@login_required
def change_published_state(request, listing_id):
    if request.method == 'POST':
        exists = Listing.objects.filter(pk=listing_id, user=request.user).exists()
        if exists:
            listing = Listing.objects.get(pk=listing_id, user=request.user)
            listing.change_published_state()
    return HttpResponseRedirect(reverse('housingtrader:index'))

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
    my_listing = get_object_or_404(Listing, user=request.user, pk=listing_id)
    mutual_matches = my_listing.find_mutual_matches()
    basic_matches = my_listing.find_matches()
    reverse_matches = my_listing.find_reverse_matches()
    return render(request, 'housingtrader/find_trades.html', {'my_listing':my_listing, 'mutual_matches':mutual_matches ,'basic_matches':basic_matches, 'reverse_matches':reverse_matches})

@login_required
def detail(request, listing_id, other_listing_id):
    my_listing = get_object_or_404(Listing, pk=listing_id, user=request.user)
    other_listing = get_object_or_404(Listing, pk=other_listing_id)
    trade_request = TradeRequest.objects.filter(requester=my_listing, receiver=other_listing).exists()
    reverse_trade_request = TradeRequest.objects.filter(requester=other_listing, receiver=my_listing).exists()
    return render(request, 'housingtrader/detail.html', {'my_listing':my_listing, 'listing':other_listing, 'trade_request_exists':trade_request, 'reverse_trade_request_exists':reverse_trade_request})

@login_required
def preview(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id, user=request.user)
    return render(request, 'housingtrader/preview.html', {'listing':listing})

@login_required
def send_trade_request(request, listing_id, other_listing_id):
    if request.method == 'POST':
        if listing_id == other_listing_id:
            messages.warning(request, 'Du försökte göra en intresseanmälan för att byta en bostad mot sig själv. Knasboll!')
            return HttpResponseRedirect(reverse('housingtrader:find_trades', args=[listing_id]))
        
        my_listing = Listing.objects.get(pk=listing_id, user=request.user)
        other_listing = Listing.objects.get(pk=other_listing_id)
        trade_request = TradeRequest(requester=my_listing, receiver=other_listing)
        try:
            trade_request.save()
            messages.success(request, 'Intresseanmälan skickad.')
        except IntegrityError:
            messages.warning(request, 'Du har redan gjort en intresseanmälan för det här bytet.')
    return HttpResponseRedirect(reverse('housingtrader:find_trades', args=[listing_id]))

@login_required
def trade_request_detail(request, requester_id, receiver_id):
    receiver = get_object_or_404(Listing, pk=receiver_id, user=request.user)
    requester = get_object_or_404(Listing, pk=requester_id)
    trade_request = get_object_or_404(TradeRequest, requester=requester, receiver=receiver)
    print trade_request.declined_by_receiver
    return render(request, 'housingtrader/trade_request_detail.html', {'requester':requester, 'receiver':receiver, 'trade_request':trade_request})

@login_required
def trade_request_decline(request, requester_id, receiver_id):
    if request.method == 'POST':
        receiver = get_object_or_404(Listing, pk=receiver_id, user=request.user)
        requester = get_object_or_404(Listing, pk=requester_id)
        trade_request = get_object_or_404(TradeRequest, requester=requester, receiver=receiver)
        trade_request.declined_by_receiver = True
        trade_request.save()
        messages.success(request, 'Du tackade nej till bytesförslaget.')
    
    return HttpResponseRedirect(reverse('housingtrader:index'))
    

class ListingDelete(DeleteView):
    model = Listing
    success_url = reverse_lazy('housingtrader:index')
    
    def get_object(self):
        queryset = Listing.objects.filter(user=self.request.user)
        return DeleteView.get_object(self, queryset=queryset)
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ListingDelete, self).dispatch(*args, **kwargs)

def search(request):
    if request.GET.get('submit'):
        form = SearchForm(request.GET)
        try:
            form.is_valid()
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
            
            search_text = strip(request.GET['text'])
            
            results = results.filter(
                Q(o_description__icontains = search_text)
                | Q(o_street_address__icontains = search_text) 
                | Q(o_postal_town__icontains = search_text)
            )
            
            return render(request, 'housingtrader/search_results.html', {'results':results, 'form':form})
        except ValueError:
            return render(request, 'housingtrader/search_base.html', {'form':form})
    else:
        return render(request, 'housingtrader/search_base.html', {'form':SearchForm()})
    
def public_detail(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    return render(request, 'housingtrader/public_detail.html', {'listing':listing})
