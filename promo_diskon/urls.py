# urls.py
from django.urls import path
from promo_diskon.views import (
    show_main, create_disc_entry, add_disc_entry_ajax,
    edit_disc_entry, delete_disc, show_xml, show_json, show_xml_by_id, show_json_by_id,
    add_disc_entry_flutter, edit_disc_entry_flutter, delete_disc_entry_flutter
)

app_name = 'promo_diskon'

urlpatterns = [
    path('', show_main, name='show_main'),  
    path('create-disc-entry/', create_disc_entry, name='create_disc_entry'),  
    path('add-disc-entry-ajax/', add_disc_entry_ajax, name='add_disc_entry_ajax'),
    path('edit-disc/<uuid:id>/', edit_disc_entry, name='edit_disc_entry'),  # Fixed to pass ID
    path('delete-disc/<uuid:id>/', delete_disc, name='delete_disc'),  # Fixed to pass ID
    path('xml/', show_xml, name='show_xml'),  
    path('json/', show_json, name='show_json'),
    path('xml/<uuid:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<uuid:id>/', show_json_by_id, name='show_json_by_id'),
    path('add-disc-entry-flutter/', add_disc_entry_flutter, name='add_disc_entry_flutter'),
    path('edit-disc-entry-flutter/<uuid:id>/', edit_disc_entry_flutter, name='edit_disc_entry_flutter'),
    path('delete-disc-entry-flutter/<uuid:id>/', delete_disc_entry_flutter, name='delete_disc_entry_flutter'),
]
