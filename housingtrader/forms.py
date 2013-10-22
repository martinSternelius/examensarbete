# -*- coding: utf-8 -*- 
from django.forms import Form, ModelForm, MultipleChoiceField, CharField, IntegerField, ChoiceField
from django.forms.widgets import CheckboxSelectMultiple
from housingtrader.models import Listing, HOUSING_TYPE_CHOICES, FLOOR_CHOICES, get_listing_fields_by_prefix
from django.contrib.localflavor.se.forms import SEPostalCodeField, SECountySelect

def get_wanted_fields():
    '''
    Wrapper function that gets the names of all fields in the Listing model that starts with w_,
    AKA the prefix of the 'wanted' fields.
    
    The function is used to exclude these fields in the 'offered' part of the form,
    and to include only these fields in the 'wanted' part of the form
    '''
    return get_listing_fields_by_prefix('w_')


'''
This is a Django snippet that provides a checkbox widget that works with a CommaSeparatedIntegerField,
which is exactly what we need for the 'Wanted housing types' field.
Source: http://djangosnippets.org/snippets/2860/
'''

# Widget
class CSICheckboxSelectMultiple(CheckboxSelectMultiple):
    def value_from_datadict(self, data, files, name):
        # Return a string of comma separated integers since the database, and
        # field expect a string (not a list).
        return ','.join(data.getlist(name))

    def render(self, name, value, attrs=None, choices=()):
        # Convert comma separated integer string to a list, since the checkbox
        # rendering code expects a list (not a string)
        if value:
            value = value.split(',')
        return super(CSICheckboxSelectMultiple, self).render(
            name, value, attrs=attrs, choices=choices
        )


# Form field
class CSIMultipleChoiceField(MultipleChoiceField):
    widget = CSICheckboxSelectMultiple

    # Value is stored and retrieved as a string of comma separated
    # integers. We don't want to do processing to convert the value to
    # a list like the normal MultipleChoiceField does.
    def to_python(self, value):
        return value

    def validate(self, value):
        # If we have a value, then we know it is a string of comma separated
        # integers. To use the MultipleChoiceField validator, we first have
        # to convert the value to a list.
        if value:
            value = value.split(',')
        super(CSIMultipleChoiceField, self).validate(value)


class ListingOfferedForm(ModelForm):
    '''
    The 'offered' part of the Listing form
    '''
    o_county = CharField(widget=SECountySelect, label='Län')
    o_postal_code = SEPostalCodeField(label='Postnummer')

    class Meta:
        '''
        User and published fields should also be excluded
        '''
        excluded_fields = get_wanted_fields()
        excluded_fields.append('user')
        excluded_fields.append('published')
        
        model = Listing
        exclude = excluded_fields

class ListingWantedForm(ModelForm):
    '''
    The 'wanted' part of the Listing form
    '''
    w_types = CSIMultipleChoiceField(required=True, choices=HOUSING_TYPE_CHOICES, label='Önskade bostadstyper')
    w_county = CharField(widget=SECountySelect, label='Län')
    
    class Meta:
        model = Listing
        fields = get_wanted_fields()
        
class CompleteListingForm(ModelForm):
    '''
    The complete Listing form
    ''' 
    w_types = CSIMultipleChoiceField(required=True, choices=HOUSING_TYPE_CHOICES, label='Önskade bostadstyper')
    
    def __init__(self, user=None, *args, **kwargs):
        '''
        @type user: User 
        '''
        super(CompleteListingForm, self).__init__(*args, **kwargs)
        
        self.user = user
    
    def save(self):
        listing = super(CompleteListingForm, self).save(commit=False)
        listing.user = self.user
        listing.save()
    
    class Meta:
        model = Listing
        exclude = ('user', 'published')
        
class SearchForm(Form):
    yes_or_none_choices = ((0, 'Inget krav'), (1, 'Ja'))
    
    text = CharField(label='Fritext', required=False)
    county = CharField(widget=SECountySelect, label='Län')
    types = CSIMultipleChoiceField(label='Bostadstyp(er)', choices=HOUSING_TYPE_CHOICES)
    min_area = IntegerField(label='Minsta yta (kvm)')
    min_rooms = IntegerField(label='Minsta antal rum')
    max_rent = IntegerField(label='Max hyra/avgift')
    has_fireplace = ChoiceField(label='Öppen spis', choices=yes_or_none_choices)
    has_balcony = ChoiceField(label='Balkong', choices=yes_or_none_choices)
    has_elevator = ChoiceField(label='Hiss', choices=yes_or_none_choices)
    not_bottom_floor = ChoiceField(label='Våning', choices=FLOOR_CHOICES)