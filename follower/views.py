from django.shortcuts import render
from django.shortcuts import redirect
from follower.models import Follow
from django.contrib.auth import get_user_model


def followers(request):
    following = Follow.objects.filter(user__exact=request.user)
    following_by = Follow.objects.filter(followed_user__exact=request.user)
    if request.POST:
        username = request.POST['username']
        User = get_user_model()
        user = User.objects.get(username__exact=username)
        if user != request.user:
            Follow.objects.get_or_create(user=request.user, followed_user=user)
        return redirect("followers")
    context = {
        'following': following,
        'following_by': following_by,
    }
    print(context)
    return render(request, 'followers/followers.html', context=context)


def delete_follower(request, follow_id):
    User = get_user_model()
    user = User.objects.get(id__exact=follow_id)
    follow = Follow.objects.get(
        user__exact=request.user,
        followed_user__exact=user
    )
    if follow is not None:
        follow.delete()
    return redirect('followers')
