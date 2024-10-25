from django.urls import path
from promo_diskon.views import show_main, create_disc_entry, add_disc_entry_ajax, edit_disc_info, delete_disc
from promo_diskon.views import show_xml, show_json, show_xml_by_id, show_json_by_id

app_name = 'promo-diskon'

urlpatterns = [
    path('', show_main, name='show_main'),  
    path('create-disc-entry/', create_disc_entry, name='create_disc_entry'),  
    path('add-disc-entry-ajax/', add_disc_entry_ajax, name='add_disc_entry_ajax'),
    path('edit-disc/', edit_disc_info, name='edit_disc_info'), 
    path('delete-disc/', delete_disc, name='delete_disc'),
    path('xml/', show_xml, name='show_xml'),  
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),

]