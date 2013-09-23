# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from housingtrader.forms import ListingOfferedForm, ListingWantedForm, CompleteListingForm

@login_required
def index(request):
    return render(request, 'housingtrader/index.html')

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
            except:
                pass
        
    return render(request, 'housingtrader/create_listing.html', {'offered_form' : offered_form, 'wanted_form' : wanted_form})
