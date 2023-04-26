from django.urls import path
from .views import post_list, post_detail
app_name = "blog"

urlpatterns = [
    #se enruta la vista
    path("", post_list, name="post_list"),
    #path("<int:id>/", post_detail, name="post_detail")
    #año/mes/día/slug es lo que se pasa como parámetro a la función post_detail, post_detail es de la vista

    path("<int:year>/<int:month>/<int:day>/<slug:post>", post_detail, name="post_detail")
]