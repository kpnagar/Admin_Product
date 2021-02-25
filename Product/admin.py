from django.contrib import admin
from .models import Category, Product
# Register your models here.
import csv
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import path
from django import forms

class HeroProxy(Category):
    class Meta:
        proxy = True


def mark_discount(modeladmin, request, queryset):
    queryset.update(is_discount=True)
    mark_discount.short_description = "Mark discount"

def export_as_csv(self, request, queryset):
    meta = self.model._meta
    field_names = [field.name for field in meta.fields]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)
    writer.writerow(field_names)    # this is first line for field heading name and next writerow for values
    """
    writer.writerow(['model_header_field_1_name','model_header_field_2_name'])
    obj = Model.objects,all()
    for i in obj:
        writer.writerow([i.model_fiels_1, i.model_field_2])
    """
    for obj in queryset:            
        row = writer.writerow([getattr(obj, field) for field in field_names])
    return response

class CsvImportForm(forms.Form):
    csv_file = forms.FileField()

class Product_SF(admin.ModelAdmin):
    list_display = ('name', 'category', 'manufacture_date', 'is_discount','discount_price', 'added_by')
    readonly_fields = ['discount_price']
    search_fields = ['name','manufacture_date']
    list_filter = ('category', 'is_discount')
    actions = [mark_discount, export_as_csv]

    date_hierarchy = 'manufacture_date'

    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        super().save_model(request, obj, form, change)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["name", "category"]
        else:
            return []

    """
    # filter FK dropdown values in django admin
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.filter(name__in=['Vicle'])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    """
    
    # start add button 
    """
    change_list_template = "entities/admin_button.html" #disable this comment

    def set_immortal(self, request):
        self.model.objects.all().update(is_discount=True)
        self.message_user(request, "All heroes are now immortal")
        return HttpResponseRedirect("../")

    def set_mortal(self, request):
        self.model.objects.all().update(is_discount=False)
        self.message_user(request, "All heroes are now mortal")
        return HttpResponseRedirect("../")

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('immortal/', self.set_immortal),
            path('mortal/', self.set_mortal),
        ]
        return my_urls + urls
    """
    # End Start Button

    # import CSV link code
    change_list_template = "admin/import_link.html" 
     
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            reader = csv.reader(csv_file)
            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = CsvImportForm()
        return render(request, "admin/csv_form.html", {"form": form})

'''
    MAX_OBJECTS = 1
    def has_add_permission(self, request):
        if self.model.objects.count() >= self.MAX_OBJECTS:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_module_permission(self, request):
        return False
'''
class VillainInline(admin.StackedInline):
    model = Product

# class VillainInline(admin.TabularInline):
#     model = Product

class Category_SF(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ('name',)
    inlines = [VillainInline]

    list_per_page = 1

admin.site.register(Category, Category_SF)
admin.site.register(HeroProxy) 
admin.site.register(Product, Product_SF)


