from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from barcode import EAN13
from barcode.writer import ImageWriter
from .models import (
    PRODUCT_SERVICE,
    ITEM_UNIT,
    ITEM_TYPE,
    Category,
    Inventory,
    Warehouse,
    Rack
)
from .utils import generate_barcode


@method_decorator([login_required], name="dispatch")
class AddNewCategory(View):

    template_name: str = "add_new_category.html"
    def get(self, request):
        categories = Category.objects.filter(user=request.user).order_by('-updated_at')
        return render(request, self.template_name, locals())

    def post(self, request):

        category = request.POST.get("category")        
        descriptions = request.POST.get("description")
        if category:
            if Category.objects.filter(user=request.user, name=category).exists():
                category_message: str ="Category Already Exists..!!!"
                return HttpResponseRedirect(reverse("add-category"), locals())
            else:
                Category.objects.create(user=request.user, name=category, description=descriptions)

        return redirect("add-category")


@method_decorator([login_required], name="dispatch")
class EditCategory(View):
    template_name: str = "update_category.html"
    def get(self, request, id):
        update_category = Category.objects.filter(user=request.user, id=id)
        return render(request, self.template_name, locals())

    def post(self, request, id):

        category = request.POST.get("category")        
        descriptions = request.POST.get("description")
        user_category = Category.objects.get(user=request.user, id=id)
        print('categgggggggobj',user_category)
        user_category.name = category
        user_category.description = descriptions
        user_category.save()

        return redirect("add-category")


@method_decorator([login_required], name="dispatch")
class DeleteCategory(View):

    def post(self, request, id):
        category = Category.objects.get(user=request.user, id=id)
        category.delete()
        return HttpResponseRedirect(reverse("add-category"))


@method_decorator([login_required], name="dispatch")
class AddInventoryItem(View):

    template_name: str = "inventory_dashboard.html"

    def get(self, request):
        search_id = request.GET.get("search_by_id")
        search_name = request.GET.get("search_by_name")
        search_category = request.GET.get("search_by_category")
        search_type = request.GET.get("search_by_type")
        search_hsn = request.GET.get("search_by_hsncode")
        units = ITEM_UNIT
        product_services = PRODUCT_SERVICE
        item_types = ITEM_TYPE
        warehouses = Warehouse.objects.all()
        if search_id:
            items = Inventory.objects.filter(user=request.user, sku__icontains=search_id)
        elif search_name:
            items = Inventory.objects.filter(user=request.user, item_name__icontains=search_name).order_by('-updated_at')
        elif search_category:
            try:
                item_category = Category.objects.get(user=request.user, name__icontains=search_category)
                items = Inventory.objects.filter(user=request.user, item_category=item_category).order_by('-updated_at')
            except:
                items = Inventory.objects.filter(user=request.user).order_by('-updated_at')
        elif search_type:
            items = Inventory.objects.filter(user=request.user, type__icontains=search_type).order_by('-updated_at')
        elif search_hsn:
            items = Inventory.objects.filter(user=request.user, hsn_code__icontains=search_hsn).order_by('-updated_at')
        else:       
            items = Inventory.objects.filter(user=request.user).order_by('-updated_at')
        categories = Category.objects.filter(user=request.user)
        return render(request, self.template_name, locals())

    def post(self, request):
        user = request.user
        item_sku = request.POST.get("item_sku")
        if Inventory.objects.filter(sku=item_sku).exists():
            message = "SKU item already exists..!!!"
            return HttpResponseRedirect(reverse("add-single-inventory-item"), locals())
        else:
            item_name = request.POST.get("item_name")
            stock = request.POST.get("stock")
            category = request.POST.get("category")
            product_service = request.POST.get("service_product")
            unit = request.POST.get("unit")
            hsn_code = request.POST.get("hsn_code")
            type = request.POST.get("item_type")
            tax = request.POST.get("tax")
            rack = request.POST.get("add-racks")
            price = request.POST.get("item_price")
            warehouses =  request.POST.get("ware_house")

            
            if category =='-------':
                error_message = "Choose the Category"
            else:
                user_category = Category.objects.get(id=category)
                Inventory.objects.create(user=request.user, price=price,racks=rack,item_name=item_name, item_category=user_category, sku=item_sku, stock=stock, product_or_service=product_service, unit_of_measurement=unit, hsn_code=hsn_code, type=type, tax=tax, warehouse=warehouses)

        return HttpResponseRedirect(reverse("add-single-inventory-item"), locals())


@method_decorator([login_required], name="dispatch")
class EditInventoryItem(View):

    template_name: str = "edit_inventory_items.html"

    def get(self, request, id):
        categories = Category.objects.filter(user=request.user)
        item_detail = Inventory.objects.filter(id=id)
        warehouses = Warehouse.objects.all()
        all_racks = Rack.objects.order_by('-updated_at')
        return render(request, self.template_name, locals())
    
    def post(self, request, id):
        item_sku = request.POST.get("item_sku")
        item_name = request.POST.get("item_name")
        stock = request.POST.get("stock")
        category = request.POST.get("category")
        user_category = Category.objects.get(id=category)
        product_service = request.POST.get("service_product")
        unit = request.POST.get("unit")
        price = request.POST.get("item_price")
        hsn_code = request.POST.get("hsn_code")
        type = request.POST.get("item_type")
        tax = request.POST.get("tax")
        rack = request.POST.get("add-racks")
        warehouse_name = request.POST.get("ware_house")
        item = Inventory.objects.filter(id=id).update(user=request.user, price=price, item_name=item_name, item_category=user_category, sku=item_sku, stock=stock, product_or_service=product_service, unit_of_measurement=unit, hsn_code=hsn_code, type=type, tax=tax,racks=rack, warehouse = warehouse_name)

        return HttpResponseRedirect(reverse("add-single-inventory-item"))


@method_decorator([login_required], name="dispatch")
class DeleteInventoryItem(View):

    def post(self, request, id):
        item_detail = Inventory.objects.get(id=id)
        item_detail.delete()
        return HttpResponseRedirect(reverse("add-single-inventory-item"))


@method_decorator([login_required], name="dispatch")
class AddWarehouse(View):
    
    template_name: str = 'add_warehouse.html'

    def get(self, request):
        warehouses = Warehouse.objects.order_by('-updated_at')
        racks = Rack.objects.all()
        return render(request, self.template_name, locals())
    def post(self, request):
        warehosue_name  = request.POST.get("warehouse_name")
        warehouse_location = request.POST.get("warehouse_loc")
        racks = request.POST.getlist("warehouse_racks")
        if Warehouse.objects.filter(name=warehosue_name).exists():
            pass
        else:
            warehouse_obj = Warehouse.objects.create(name=warehosue_name, address=warehouse_location)
            for rack in racks:
                warehouse_obj.rack.add(rack)
                warehouse_obj.save()
        return HttpResponseRedirect(reverse("add-warehouse"))


@method_decorator([login_required], name="dispatch")
class EditWarehouse(View):
    template_name: str = 'edit_warehouse.html'

    def get(self, request, id):

        warehouse_detail = Warehouse.objects.filter(id=id)
        return render(request, self.template_name, locals())
    
    def post(self, request, id):

        name = request.POST.get("warehouse")
        address = request.POST.get("address")
        if address and name:
            warehouse = Warehouse.objects.get(id=id)
            warehouse.name = name
            warehouse.address = address
            warehouse.save()

        return HttpResponseRedirect(reverse("add-warehouse"))



@method_decorator([login_required], name="dispatch")
class DeleteWarehouse(View):
    template_name: str = 'add_warehouse.html'

    def post(self, request, id):
        warehouse = Warehouse.objects.get(id=id)
        warehouse.delete()
        return HttpResponseRedirect(reverse("add-warehouse"))


@method_decorator([login_required], name="dispatch")
class AddRack(View):
    template_name: str = 'add_rack.html'
    def get(self, request):
        racks = Rack.objects.order_by('-updated_at')
        warehouses = Warehouse.objects.all()
        return render(request, self.template_name, locals())

    def post(self, request):
        rack = request.POST.get("racks")
        ware_id = request.POST.get("warehouse")
        warehouse = Warehouse.objects.get(id=ware_id)
        Rack.objects.create(warehouse=warehouse,rack=rack)
        
        return HttpResponseRedirect(reverse("add-rack"))


@method_decorator([login_required], name="dispatch")
class DeleteRack(View):
    template_name: str = 'add_rack.html'

    def post(self, request, id):
        rack = Rack.objects.get(id=id)
        rack.delete()
        return HttpResponseRedirect(reverse("add-rack"))


@method_decorator([login_required], name="dispatch")
class EditRack(View):
    template_name: str = 'edit_rack.html'

    def get(self, request, id):
        rack_detail = Rack.objects.get(id=id)
        return render(request, self.template_name, locals())
    def post(self, request, id):
        warehouse = request.POST.get('warehouse')
        rackname = request.POST.get('rack')
        warehouse_obj = Warehouse.objects.get(name=warehouse)
        rack = Rack.objects.get(id=id)
        rack.rack = rackname
        rack.warehosue = warehouse_obj
        rack.save()
        
        return HttpResponseRedirect(reverse("add-rack"))

@method_decorator([login_required], name="dispatch")
class GetWarehouseRack(View):

    def get(self, request, name):
        warehouse_obj = Warehouse.objects.get(name=name)
        rack_detail = Rack.objects.filter(warehouse=warehouse_obj)
        racks = []
        for rack in rack_detail:
            racks.append(rack.rack)
        context = {
            "status": 200,
            "racks": list(racks),
        }
        return JsonResponse(context)
