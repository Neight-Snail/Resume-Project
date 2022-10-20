from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.index, name='index'),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_user, name="logout"),
    path("create/", views.create_post, name="create"),
    path('u/<str:username>', views.view_profile, name="view_profile"),
    path('delete/<int:post_id>', views.delete_post, name="delete_post"),
    path('edit/<int:post_id>', views.edit_post, name="edit_post"),
    path('upvote/<int:post_id>', views.upvote, name="upvote"),
    path('downvote/<int:post_id>', views.downvote, name="downvote"),
    path('stats/', views.stats, name="stats")
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)