from django.conf.urls import patterns, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'examensarbete.views.home', name='home'),
    # url(r'^examensarbete/', include('examensarbete.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', 'django.contrib.auth.views.login' , name='login'),
    url(r'^logout/', 'django.contrib.auth.views.logout' , name='logout'),
    url(r'^registration/', 'registration.views.register', name='register'),
)
