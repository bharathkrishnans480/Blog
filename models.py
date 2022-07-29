from django.db import models
from django.contrib.auth.models import User
import random
# Create your models here.

class UserProfile(models.Model):
    profile_pic=models.ImageField(upload_to="profile_pic",null=True)
    bio=models.CharField(max_length=120)
    phone=models.CharField(max_length=15)
    date_of_birth=models.DateField(null=True)
    options=(
        ("male","male"),
        ("female","female"),
        ("other","other"),
    )
    gender=models.CharField(max_length=12,choices=options,default="male")
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="users")        #related name is important when calling request.user.users
    following=models.ManyToManyField(User,related_name="following",blank=True)

    @property
    def fetch_following(self):
        return self.following.all()
    @property
    def fetch_following_count(self):
        return self.fetch_following.count()

    @property
    def invitations(self):
        #fetch all profile users except current user
        all_userprofile=UserProfile.objects.all().exclude(user=self.user)
        #taking user objects from all users
        user_list=[userprofile.user for userprofile in all_userprofile]
        #getting following list
        following_list=[user for user in self.fetch_following]
        #excluded my followings from all users
        invitations=[user for user in user_list if user not in following_list]
        #return invitations (using random for invitations)
        return random.sample(invitations,1)    #error occurs if there are no 5 users

    def get_followers(self):
        all_userprofile=UserProfile.objects.all()
        myfollowers=[]
        for profile in all_userprofile:
            if self.user in profile.fetch_following:
                myfollowers.append(profile)
        return myfollowers
    def myfollower_count(self):
        return len(self.get_followers())


class Blogs(models.Model):
    title=models.CharField(max_length=120)
    description=models.CharField(max_length=230)
    image=models.ImageField(upload_to="blogimages",null=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name="author")
    posted_date=models.DateTimeField(auto_now_add=True)
    liked_by=models.ManyToManyField(User)

    @property                                  #when at property is used ,the no need to call it with function brackets
    def get_like_count(self):
        like_count=self.liked_by.all().count()
        return like_count

    def __str__(self):
        return self.title

class Comments(models.Model):
    blog=models.ForeignKey(Blogs,on_delete=models.CASCADE)
    comment=models.CharField(max_length=160)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.comment



#python manage.py createsuperuser
#fetching all comments related to a specific blog,
#blog.comments_set.all()