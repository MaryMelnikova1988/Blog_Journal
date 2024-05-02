from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogCreateView, BlogListView, BlogDetailView, BlogUpdateView, BlogDeleteView, toogle_activity, \
    IndexView, contacts

app_name = BlogConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contacts/', contacts, name='contacts'),

    path('blog/create/', BlogCreateView.as_view(), name='create'),
    path('blog/list/', BlogListView.as_view(), name='list'),
    path('blog/view/<int:pk>/', BlogDetailView.as_view(), name='view'),
    path('blog/edit/<int:pk>/', BlogUpdateView.as_view(), name='edit'),
    path('blog/delete/<int:pk>/', BlogDeleteView.as_view(), name='delete'),
    path('blog/activity/<int:pk>/', toogle_activity, name='toogle_activity'),

]