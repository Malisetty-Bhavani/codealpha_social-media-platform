from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Post, Comment, Follow
from .models import Post

@login_required
def create_post(request):

    if request.method == 'POST':

        content = request.POST.get('content')
        image = request.FILES.get('image')

        Post.objects.create(
            user=request.user,
            content=content,
            image=image
        )

        return redirect('home')

    return render(request, 'app/create_post.html')


# HOME PAGE
from django.contrib.auth.models import User

@login_required
def home(request):

    posts = Post.objects.all().order_by('-created_at')

    query = request.GET.get('q')

    if query:

        users = User.objects.filter(
            username__icontains=query
        )

    else:

        users = User.objects.none()

    return render(request, 'app/home.html', {

        'posts': posts,
        'users': users,

    })

# REGISTER
def register(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.create_user(
            username=username,
            password=password
        )

        login(request, user)

        return redirect('home')

    return render(request, 'app/register.html')


# LOGIN
def login_view(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('home')

    return render(request, 'app/login.html')


# LOGOUT
def logout_view(request):

    logout(request)

    return redirect('login')


# PROFILE
@login_required
def profile(request, username):

    profile_user = User.objects.get(
        username=username
    )

    posts = Post.objects.filter(
        user=profile_user
    ).order_by('-created_at')

    followers_count = Follow.objects.filter(
        following=profile_user
    ).count()

    following_count = Follow.objects.filter(
        follower=profile_user
    ).count()

    is_following = Follow.objects.filter(
        follower=request.user,
        following=profile_user
    ).exists()

    return render(request, 'app/profile.html', {

        'profile_user': profile_user,
        'posts': posts,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,

    })
# FOLLOW USER
@login_required
def follow_user(request, username):

    user_to_follow = User.objects.get(
        username=username
    )

    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=user_to_follow
    )

    if not created:
        follow.delete()

    return redirect('profile', username=username)


# LIKE POST
@login_required
def like_post(request, post_id):

    post = Post.objects.get(id=post_id)

    if request.user in post.likes.all():

        post.likes.remove(request.user)

    else:

        post.likes.add(request.user)

    return redirect('home')


# COMMENT
@login_required
def add_comment(request, post_id):

    if request.method == 'POST':

        post = Post.objects.get(id=post_id)

        text = request.POST['comment']

        Comment.objects.create(
            post=post,
            user=request.user,
            text=text
        )

    return redirect('home')
from django.contrib.auth.models import User
from django.contrib.auth import login

def register_view(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:

            if not User.objects.filter(username=username).exists():

                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1
                )

                login(request, user)

                return redirect('home')

    return render(request, 'app/register.html')
@login_required
def follow_user(request, username):

    user_to_follow = get_object_or_404(
        User,
        username=username
    )

    if request.user != user_to_follow:

        already_following = Follow.objects.filter(
            follower=request.user,
            following=user_to_follow
        ).exists()

        if already_following:

            Follow.objects.filter(
                follower=request.user,
                following=user_to_follow
            ).delete()

        else:

            Follow.objects.create(
                follower=request.user,
                following=user_to_follow
            )

    return redirect(
        'profile',
        username=username
    )