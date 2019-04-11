from django.urls import path as url
from Rules import views

__author__ = 'Saysell'

urlpatterns = [url(r'browse', views.view_rules, name='browse'),
               url(r'create_category', views.add_category, name='add_category'),
               url(r'edit_category', views.edit_category, name='edit_category'),
               url(r'delete_category/<int:category_id>', views.delete_category, name='delete_category'),
               url(r'add_rule/<int:category_id>', views.add_rule, name='add_rule'),
               url(r'delete_rule/(\d+)', views.delete_rule, name='delete_rule'),
               url(r'edit_rule', views.edit_rule, name='edit_rule'),
               url(r'get_edit_rule_form/(\d+)', views.get_edit_rule_form, name='get_edit_rule_form'),
               url(r'get_edit_category_form/<int:category_id>', views.get_edit_category_form, name='get_edit_category_form'),
               url(r'import_rules', views.import_rules, name='import_rules'),
               ]
