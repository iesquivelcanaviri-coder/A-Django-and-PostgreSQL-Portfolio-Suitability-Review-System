from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import UpdatePostForm
from .models import UpdatePost


@login_required
def update_list(request):
    posts = UpdatePost.objects.filter(is_visible=True)

    return render(request, "updates/update_list.html", {
        "posts": posts,
    })


@login_required
def update_create(request):
    if request.method == "POST":
        form = UpdatePostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.save()
            return redirect("updates:list")

    else:
        form = UpdatePostForm()

    return render(request, "updates/update_form.html", {
        "form": form,
    })