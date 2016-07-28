from django.conf.urls import url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^catalog/', views.Catalog.as_view()),
    url(r'^updatecatalog/', views.UpdateCatalog.as_view()),
    url(r'^register/', views.Register.as_view()),
    url(r'^lablist/', views.LabList.as_view()),
    url(r'^rebuildlab/', views.RebuildLab.as_view()),
    #url(r'^getips/', views.FloatingIpList.as_view())
]

#urlpatterns = format_suffix_patterns(urlpatterns)

