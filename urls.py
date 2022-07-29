from django.urls import path
from blogapp import views


urlpatterns=[
    path('account/signup',views.SignUpView.as_view(),name='signup'),
    path('account/signin',views.SignInView.as_view(),name='signin'),
    path('home',views.IndexView.as_view(),name='home'),
    path('user/profile/add',views.CreateProfileView.as_view(),name='add-profile'),
    path('user/profile/view',views.ProfileView.as_view(),name='view-profile'),
    path('user/password/change',views.PasswordResetView.as_view(),name='password-reset'),
    path('user/profile/edit/<int:user_id>',views.ProfileUpdateView.as_view(),name='edit-profile'),
    path('user/pic/<int:user_id>',views.ProPicView.as_view(),name='pro-pic'),
    path('user/post/comment/add/<int:post_id>',views.add_comment,name="add-comment"),
    path('user/post/like/add/<int:post_id>',views.add_like,name='add-like'),
    path('user/account/logout',views.log_outView,name='logout'),
    path('user/friend/follow/<int:user_id>',views.follow_friend,name='follow'),
    path('index',views.NewIndexView.as_view(),name='feed'),
    path('design',views.DesignView.as_view(),name='design'),
    path('base1',views.Base1_View.as_view(),name='base1'),
    path('user/profile/following',views.Following_Page_View.as_view(),name='following-page'),
    path('user/profile/aboutus',views.AboutUs_View.as_view(),name='aboutus')
]

