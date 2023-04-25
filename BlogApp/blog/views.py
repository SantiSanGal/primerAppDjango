from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import HttpResponse, Http404
# Create your views here.

def post_list(request):
    #request trae la ruta que se consulta, ejemplo: GET http://127.0.0.1:8000/blog/posts/
    posts = Post.published.all()
    #print(posts)
    #return HttpResponse(f"<h1>{posts[0].title}</h1>")
    return render(request, "blog/post/list.html", {"posts": posts})

def post_detail(request, id):
    #try:
    #    post = Post.published.get(id=id)
    #except Post.DoesNotExist:
    #    raise Http404("Post Not Found")

    #busca si existe el Post con el id obtenido de la url y sólo lo trae si está con Status="PB" Público
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)

    return render(request, "blog/post/detail.html", {"post": post})
