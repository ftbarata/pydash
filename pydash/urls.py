from django.conf.urls import url
from django.contrib import admin
from .core.views import home_page_view, show_message_view, add_message_view, delete_message_view, add_group_view, del_group_view, public_home_view
from .auth_manager.views import login_user, logout_user
from .profiles_manager.views import profile_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', public_home_view, name='public_home'),
    url(r'^private-home/$', home_page_view, name='home'),
    url(r'^add-message/$', add_message_view, name='add_message'),
    url(r'^messages/(?P<group>\w+)$', show_message_view, name='show_message'),
    url(r'^messages/delete/(?P<id>\d+)$', delete_message_view, name='delete_message'),
    url(r'^groups/add$', add_group_view, name='add_group'),
    url(r'^groups/del$', del_group_view, name='del_group'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', login_user, name='login'),
    url(r'^logout/$', logout_user, name='logout'),
    url(r'^profile-view/$', profile_view, name='profile-view'),
    url(r'^profile-view/(?P<username>.*)$', profile_view, name='profile-view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
