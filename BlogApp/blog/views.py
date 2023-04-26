from django.shortcuts import render, get_object_or_404
from .models import Post
#from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#vista por clase
from django.views.generic import ListView
# Create your views here.
from .forms import EmailPostForm
from django.core.mail import send_mail

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"

def post_list(request):
    #request trae la ruta que se consulta, ejemplo: GET http://127.0.0.1:8000/blog/posts/
    posts_list = Post.published.all()

    #se pasa como parámetro la instancia que obtiene todos los post, y el 3 es la cantidad a mostrarse por página
    paginator = Paginator(posts_list, 3)
    #obtiene el número de página de la url
    page_number = request.GET.get("page", 1)
    try:
        #trae el paginator y guarda en la variable, los que se deben mostrar
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    #print(posts)
    #return HttpResponse(f"<h1>{posts[0].title}</h1>")
    return render(request, "blog/post/list.html", {"posts": posts})

def post_detail(request, year, month, day, post):
    #try:
    #    post = Post.published.get(id=id)
    #except Post.DoesNotExist:
    #    raise Http404("Post Not Found")

    #busca si existe el Post con el id obtenido de la url y sólo lo trae si está con Status="PB" Público
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             slug=post)

    return render(request, "blog/post/detail.html", {"post": post})

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status = Post.Status.PUBLISHED)
    sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #creando la url absoluta de un post
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recomienda que leas {post.title}"
            message = f"Read {post.title} at {post_url}"
            send_mail(subject, message, "admin@gmail.com", [f"{cd['to']}"])
            sent=True
    else:
        form = EmailPostForm()
    return render(request, "blog/post/share.html", {"post": post, "form": form, "sent": sent})
