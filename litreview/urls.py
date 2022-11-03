from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path
import flux.views
import follower.views
import user.views


urlpatterns = [
    path("admin/", admin.site.urls),
    path('flux/', flux.views.flux, name='flux'),
    path('', LoginView.as_view(
        template_name='user/login.html',
        redirect_authenticated_user=True),
        name='login'),
    path("logout", user.views.logout_user, name="logout"),
    path('signup/', user.views.signup_page, name='signup'),
    path('posts/', flux.views.post, name='posts'),
    path('followers/', follower.views.followers, name='followers'),
    path('create_ticket/', flux.views.create_ticket, name='create_ticket'),
    path('create_review/', flux.views.create_review, name='create_review'),
    path('review_form/', flux.views.review_flux, name='review_form'),
    path('response_ticket/<int:ticket_id>/', flux.views.response_ticket, name='response_ticket'),
    path('ticket_review', flux.views.ticket_review, name='ticket_review'),
    path(
        'delete_ticket/<int:ticket_id>/',
        flux.views.delete_ticket,
        name='delete_ticket'),
    path(
        'delete_review/<int:review_id>/',
        flux.views.delete_review,
        name='delete_review'),
    path('edit_review/<int:pk>/', flux.views.EditReview.as_view(), name='edit_review'),
    path('edit_ticket/<int:pk>/', flux.views.EditTicket.as_view(), name='edit_ticket'),
    path('delete_follower/<int:follow_id>/', follower.views.delete_follower, name='delete_follower'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
