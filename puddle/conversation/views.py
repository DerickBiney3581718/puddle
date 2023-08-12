from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from item.models import Item
from .models import Conversation
from .forms import ConversationMessageForm

# Create your views here.
@login_required
def new_conversation(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if item.created_by == request.user:
        return redirect("dashboard:index")

    conversations = Conversation.objects.filter(item = item).filter(members__in = [request.user.id])
    if conversations.exists():
        return redirect('conversation:detail', pk=pk)
    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        print('form', form)
        
        if form.is_valid():
            conversation = Conversation.objects.create(item = item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()
            return redirect('item:detail', pk = item.id)
    else:
        form = ConversationMessageForm()
    return render(request, 'conversation/new.html', {'form': form})
    # new_convo = Conversation.objects.create(item,[item.user, request.user])
    # return render(request, 'conversation/chat.html', {'convo':new_convo})
    
@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in = [request.user.id])
    return render(request, 'conversation/inbox.html', {'conversations':conversations})

@login_required
def detail(request, pk):
    convo = get_object_or_404(Conversation, pk=pk)
    
    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = convo
            message.created_by = request.user
            message.save()
            
    form = ConversationMessageForm()
    return render(request, 'conversation/detail.html', {'conversation':convo, 'form':form})