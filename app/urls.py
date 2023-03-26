from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import views
from django.conf import settings

urlpatterns = [
    path('', views.index),
    path('api/home/', include('home.api.urls')),
    path('api/meta/', include('model_meta_data.api.urls.model_meta_urls')),
    path('api/coupons/', include('core.api.urls.coupons_urls')),
    path('api/specialoffers/', include('core.api.urls.special_offers_urls')),
    path('api/rooms/', include('core.api.urls.rooms_urls')),
    path('api/customers/', include('core.api.urls.customers_urls')),
    path('api/roomservices/', include('core.api.urls.room_service_urls')),
    path('api/bookings/', include('core.api.urls.booking_urls')),
    path('api/forms/', include('core_forms.api.urls')),
    path('api/banners/', include('core.api.urls.banners_urls')),
    path('api/activities/', include('core.api.urls.activities_urls')),
    path('api/strengths/', include('core.api.urls.strengths_urls')),
    path('api/gallery/', include('core.api.urls.gallery_urls')),
    path('api/services/', include('core.api.urls.services_urls')),
    path('api/kitchen/', include('core.api.urls.kitchens_urls')),
    path('api/accounts/', include('accounts.api.urls.user_urls')),
    path('api/roles/', include('accounts.api.urls.role_urls')),
    path('api/positions/', include('accounts.api.urls.position_urls')),
    path('api/permissions/', include('accounts.api.urls.permission_urls')),
                                     
    path('api/primary_contact/', include('core.api.urls.primary_contact_urls')),                          

    path('api/documents/', include('documents.api.urls')),
    path('api/images/', include('documents.api.images_urls')),
    
    path('api/modelrelations/', include('modelrelations.api.urls')),
    path('api/model-lookups/', include('core.api.urls.model_lookups_data_urls')),

    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
