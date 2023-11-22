from django.shortcuts import render, redirect, reverse, HttpResponse

# Create your views here.

def view_bag(request):
    """A view to show contents of shopping cart"""
    return render(request, 'bag/bag.html')


def adjust_bag(request, item_id):
    """Adjust quantity of specified product to specified amount"""
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
    else: 
        if quantity > 0:
            bag[item_id] = quantity
        else:
            bag.pop(item_id)

    request.session['bag'] = bag
    print(request.session['bag'])
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """Remove the item from the bag"""
    
    try:
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
        else: 
            bag.pop(item_id)

        request.session['bag'] = bag
        print(request.session['bag'])
        #As posting from javascript function, use HttpResponse to return 200 (success)
        return HttpResponse(status=200)
    except:
        return HttpResponse(status=500)


def add_to_bag(request, item_id):
    """Add a quantity of specified item to shopping bag"""
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if item_id in list(bag.keys()):
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity
            else:
                bag[item_id]['items_by_size'][size] = quantity
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}

    else: 
        if item_id in list(bag.keys()):
            bag[item_id] += quantity  #increment by quantity
        else:
            bag[item_id] = quantity

    request.session['bag'] = bag
    print(request.session['bag'])
    return redirect(redirect_url)