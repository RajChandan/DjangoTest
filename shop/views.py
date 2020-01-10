from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,Contact,Orders,OrderUpdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request):
   # products = Product.objects.all()
    allProds = []
    catProds = Product.objects.values('category','id')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n=len(prod)
        n_slides=n//4 + ceil((n/4)-(n//4))
        allProds.append([prod,range(1,n_slides),n_slides])
    #params = {'product': products, 'no_of_slides':n_slides, 'range': range(n_slides)}
    #allProds = [[products,range(1,n_slides),n_slides],[products,range(1,n_slides),n_slides]]
    params={'allProds':allProds}

    return render(request,'shop/index.html', params)

def searchMatch(query,item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    # products = Product.objects.all()
    allProds = []
    query = request.GET.get('search')
    catProds = Product.objects.values('category','id')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query,item)]
        n = len(prod)
        nSlides = n//4 +ceil((n/4)-(n//4))
        if len(prod)!=0:
             allProds.append([prod,range(1,nSlides),nSlides])
    params={'allProds':allProds,'msg':''}
    if len(allProds) ==0 or len(query)<4:
        params = {'msg':'Product not found'}
    print(params)
    return render(request,'shop/search.html',params)


def about(request):
    return render(request,'shop/about.html')

def contact(request):
    thank = False
    if request.method=="POST":
        print('request')
        name = request.POST.get('name', '')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        desc = request.POST.get('desc','')
        print(name,email,phone,desc)
        contact=Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
        thank = True
    return render(request,'shop/contactus.html', {'thank':thank})

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success","updates":updates,"itemsJson":order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')



def productView(request,myid):
    #fetch the product using id
    product = Product.objects.filter(id=myid)
    return render(request,'shop/prodView.html', {'product':product[0]})



def checkout(request):
    if request.method=="POST":
        print('request')
        items_json = request.POST.get('itemsJson','')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount','')
        email = request.POST.get('email','')
        address = request.POST.get('address','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        zip_code = request.POST.get('zip_code','')
        phone = request.POST.get('phone','')
        order = Orders(items_json=items_json,name=name,email=email,address=address,city=city,state=state,zip_code=zip_code,phone=phone,amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id,update_desc='Your order has been placed')
        update.save()
        thank = True
        id = order.order_id
        return render(request,'shop/checkout.html',{'thank':thank,'id':id})
        #request paytm to transfer the amount
    return render(request,'shop/checkout.html')

@csrf_exempt
def handlerequest(request):
    #paytm will send post request here.
    pass