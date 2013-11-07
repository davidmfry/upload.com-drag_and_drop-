from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'upload.views.home', name='home'),
    # url(r'^upload/', include('upload.foo.urls')),
    #(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT }), 
    #(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'doucment_root': settings.MEDIA_ROOT}),
    url(r'^form/$', 'drag_and_drop_app.views.uploadform', name='uploadform'),
    url(r'^upload/(?P<user_id>\d+)/$', 'drag_and_drop_app.views.upload', name='upload'),
    #url(r'^upload/$', 'drag_and_drop_app.views.upload', name='upload'),
    url(r'^upload/(?P<user_id>\d+)/upload-files/$', 'drag_and_drop_app.views.upload_files', name='upload_files'),
    url(r'^master/$', 'drag_and_drop_app.views.master', name='master'),
    url(r'^master/master-checked/$', 'drag_and_drop_app.views.master_checked', name='master_checked'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()