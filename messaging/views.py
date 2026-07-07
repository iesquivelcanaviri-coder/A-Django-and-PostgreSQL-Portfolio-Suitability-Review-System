"""Inbox, sent, archive and compose views."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from .forms import MessageForm
from .models import Message


@login_required
def inbox(request):
    msgs = Message.objects.filter(recipient=request.user, recipient_archived=False)
    return render(request, "messaging/inbox.html", {"messages_list": msgs, "box_title": "Inbox"})


@login_required
def sent(request):
    msgs = Message.objects.filter(sender=request.user, sender_archived=False)
    return render(request, "messaging/inbox.html", {"messages_list": msgs, "box_title": "Sent Messages"})


@login_required
def archived(request):
    msgs = Message.objects.filter(recipient=request.user, recipient_archived=True) | Message.objects.filter(sender=request.user, sender_archived=True)
    return render(request, "messaging/inbox.html", {"messages_list": msgs.distinct(), "box_title": "Archived Messages"})


@login_required
def compose(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.save()
            messages.success(request, "Message sent.")
            return redirect("messaging:sent")
    else:
        form = MessageForm()
    return render(request, "messaging/compose.html", {"form": form})


@login_required
def detail(request, pk):
    msg = get_object_or_404(Message, pk=pk)
    if request.user not in {msg.sender, msg.recipient}:
        raise PermissionDenied("You can only read messages that you sent or received.")
    if request.user == msg.recipient and not msg.is_read:
        msg.is_read = True
        msg.save(update_fields=["is_read"])
    return render(request, "messaging/message_detail.html", {"message_obj": msg})


@login_required
def archive_message(request, pk):
    msg = get_object_or_404(Message, pk=pk)
    if request.user == msg.recipient:
        msg.recipient_archived = True
    elif request.user == msg.sender:
        msg.sender_archived = True
    else:
        raise PermissionDenied("You can only archive your own messages.")
    msg.save()
    messages.success(request, "Message archived.")
    return redirect("messaging:inbox")
