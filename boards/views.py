from django.contrib.auth.models import User
from .forms import NewTopicForm,  ReplyForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Board, topic, post
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView, ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = post
    fields = ('message', )
    template_name = 'boards/edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('boards:topic_posts', d=post.topic.board.pk, topic_pk=post.topic.pk)


'''def home(request):
    boards = Board.objects.all()
    return render(request, 'boards/index.html', {'boards': boards})
    
The above function is a view of home page    
'''



class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'boards/index.html'


class TopicListView(ListView):
    model = topic
    context_object_name = 'topics'
    template_name = 'boards/topics.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        kwargs['boards'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('d'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset


'''def topics(request, d):
    board = get_object_or_404(Board, id=d)
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts')-1)

    page = request.GET.get('page',1)
    paginator = Paginator(topics, 5)

    try:
        topics = paginator.page(page)

    except EmptyPage:
        topics = paginator.page(paginator.num_pages)

    except PageNotAnInteger:
        topics = paginator.page(1)


    return render(request, 'boards/topics.html', {'boards': board, 'topics': topics})
'''

@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email', )
    template_name = 'boards/my_account.html'
    success_url = reverse_lazy('boards:my_account')

    def get_object(self):
        return self.request.user


class PostListView(ListView):
    model = post
    context_object_name = 'posts'
    template_name = 'boards/topic_post.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):

        session_key = 'viewed_topic_{}'.format(self.topic.pk)

        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True


        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(topic, board__pk=self.kwargs.get('d'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset

def topic_post(request, d, topic_pk):
    topic_object = get_object_or_404(topic, board__pk=d, pk=topic_pk)

    topic_object.views += 1
    topic_object.save()
    return render(request, 'boards/topic_post.html', {'topic': topic_object})


@login_required
def post_reply(request, d, topic_pk):
    topic_object = get_object_or_404(topic, board__pk=d, pk=topic_pk)
    if request.method == 'POST':
        reply = ReplyForm(request.POST)
        if reply.is_valid():
            Post = reply.save(commit=False)
            Post.topic = topic_object
            Post.created_by = request.user


            topic_object.last_updated =timezone.now()
            topic_object.save()

            Post.save()
            return redirect('boards:topic_posts', d=d, topic_pk=topic_pk)


    else:
        reply = ReplyForm()
    return render(request, 'boards/post_reply.html', {'topic': topic_object,'form': reply})


@login_required
def new_topic(request, id):
    board = get_object_or_404(Board, id=id)

    if request.method == 'POST':

        faram = NewTopicForm(request.POST)
        if faram.is_valid():
            topic = faram.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            pos = post.objects.create(
                message=faram.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('boards:topic_posts',  d=id, topic_pk=topic.pk)
    else:
        faram = NewTopicForm()

    return render(request, 'boards/new_topic.html', {'board': board, 'form': faram})
