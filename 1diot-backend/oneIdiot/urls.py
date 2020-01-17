"""oneIdiot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users import views as users_views
from questions import views as questions_views
from rooms import views as room_views
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^users/$', users_views.users_list),
    url(r'^users/(?P<pk>[0-9]+)$', users_views.users_detail),

    url(r'^questions/$', questions_views.questions_list),
    url(r'^questions/(?P<pk>[0-9]+)$', questions_views.questions_detail),
    url(r'^questions/(?P<pk>[0-9]+)/right$', questions_views.right_prompt),
    url(r'^questions/(?P<pk>[0-9]+)/wrong$', questions_views.wrong_prompt),
    url(r'^rooms/$', room_views.rooms_list),
    url(r'^rooms/(?P<room>[a-zA-Z0-9]+)$', room_views.rooms_detail),
    url(r'^rooms/(?P<room>[a-zA-Z0-9]{4})/adduser$', room_views.add_user),
    url(r'^rooms/(?P<room>[a-zA-Z0-9]{4})/removeuser$', room_views.remove_user),
    url(r'^rooms/(?P<room>[a-zA-Z0-9]{4})/removeroom$', room_views.remove_room),


    url(r'^rooms/(?P<room>[a-zA-Z0-9]{4})/getstate$', room_views.get_state),
    url(r'^rooms/(?P<room>[a-zA-Z0-9]{4})/setstate$', room_views.set_state),
    url(r'^rooms/(?P<room>[a-zA-Z0-9]{4})/submitanswer$', room_views.submit_answer),
    url(r'^rooms/(?P<room>[a-zA-Z0-9]{4})/getanswers$', room_views.get_answers),
    url(r'^rooms/(?P<room>[a-zA-Z0-9]{4})/setwronguser$', room_views.set_wrong_user),
    url(r'^rooms/(?P<room>[a-zA-Z0-9]{4})/getwronguser$', room_views.get_wrong_user),
    url(r'^rooms/(?P<room>[a-zA-Z0-9]{4})/setnewquestion$', room_views.set_new_question),
    url(r'^rooms/(?P<room>[a-zA-Z0-9]{4})/clearroom$', room_views.clear_room),
    url(r'^rooms/(?P<room>[a-zA-Z0-9]{4})/settime$', room_views.set_time),
    url(r'^rooms/(?P<room>[a-zA-Z0-9]{4})/vote$', room_views.vote),
    url(r'^rooms/(?P<room>[a-zA-Z0-9]{4})/determinewinner$', room_views.determine_winner),
    url(r'^rooms/(?P<room>[a-zA-Z0-9]{4})/voteresults$', room_views.vote_results),
    url(r'^rooms/(?P<room>[a-zA-Z0-9]{4})/iswinnerdetermined$', room_views.is_winner_determined),
    url(r'^rooms/(?P<room>[a-zA-Z0-9]{4})/uservotes$', room_views.user_votes)
]
