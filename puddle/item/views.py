from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Category
from .forms import NewItemForm, EditItemForm
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic import UpdateView
from django.db.models import Q

# Create your views here.
def items(request):
    items = Item.objects.filter(is_sold = False )
    categories = Category.objects.all()
    query = request.GET.get('query','')
    category = request.GET.get('category',0)

            
    if category:
        items = items.filter(category_id=category)
        
    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    
    return render(request, 'item/items.html', {'items':items, 'query':query, 'categories':categories, 'category_id':int(category)})

def detail(request, pk, *args, **kwargs):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[:3]
    return render(request, 'item/detail.html', {
        'item': item, 'related_items':related_items
    })
    
@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit= False)
            item.created_by = request.user
            item.save()
            return redirect('item:detail', pk = item.id)
    else:
        form = NewItemForm()
    return render(request,'item/form.html', {'form':form, 'title':'new Form'} )

@login_required
def delete(request, pk , *args, **kwargs):
    to_be_deleted = get_object_or_404(Item, pk=pk, created_by = request.user)
    if to_be_deleted:
        to_be_deleted.delete()
        return redirect('dashboard/')
    return None

@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by = request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance = item)
        if form.is_valid():
            form.save()
            return redirect('dashboard/' )
        print('invalid form', form)
    else:
        form = EditItemForm(instance=item)
    return render(request,'item/form.html', {'form':form, 'title':' Edit form'} )

# class EditItemView(LoginRequiredMixin, UpdateView):
#     template_name = 'item/form.html'
#     form_class = EditItemForm
#     redirect_field_name = 'dashboard'
#     model = Item

#     def get(self, request):
#         item = get_object_or_404(Item, self.kwargs.get('pk'))
#         form = EditItemForm(instance=item)
#         return render(request,'item/form.html', {'form':form, 'title':' Edit form'} )
    
    