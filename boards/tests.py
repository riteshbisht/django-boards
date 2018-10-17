from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from .models import Board,topic, post
from .views import topics, home, new_topic
from .forms import NewTopicForm


def createBoard(name, desc):
    return Board.objects.create(Name=name, description=desc)


class HomeTests(TestCase):

    def setUp(self):
        self.board = Board.objects.create(Name='Python', description='Python discussion board')
        self.response = self.client.get(reverse('boards:home'))

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_to_home_view(self):
        view = resolve('/boards/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('boards:topics', kwargs={'d': self.board.id})
        self.assertContains(self.response, 'href = "{0}"'.format(board_topics_url))

    def test_board_topic_view_contains_link_back_to_home_view(self):
        board_topic_url = reverse('boards:topics', kwargs={'d': self.board.id})
        response = self.client.get(board_topic_url)
        home_url = reverse('boards:home')
        self.assertContains(response, 'href = "{0}"'.format(home_url))


class BoardTopicsTests(TestCase):

    def test_board_topics_view_success_status_code(self):
        board = createBoard(name='Django', desc='General Django discussion board')
        response = self.client.get(reverse('boards:topics', kwargs={'d': 1}))
        self.assertEquals(response.status_code, 200)

    def test_board_topic_view_not_found_status_code(self):
        response = self.client.get(reverse('boards:topics', kwargs={'d': 99}))
        self.assertEquals(response.status_code, 404)

    def test_board_topic_url_resolves_board_topic_view(self):
        board = createBoard(name='Python', desc='Pythonn discussion board')
        view = resolve('/boards/1/')
        self.assertEquals(view.func, topics)

    def test_board_topic_view_contains_navigation_link(self):
        board = createBoard(name='Random', desc='Random')
        board_topics_url = reverse('boards:topics', kwargs ={'d': board.id})
        new_topic_url = reverse('boards:new_topic', kwargs={'id': board.id})
        home_url = reverse('boards:home')

        response = self.client.get(board_topics_url)
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))
        self.assertContains(response, 'href="{0}"'.format(home_url))




class NewTopicTests(TestCase):

    def setUp(self):
        self.board = Board.objects.create(Name='Random board', description='Random discussion')
        User.objects.create_user(username='john', email='john@doe.com', password='123')
        self.response = self.client.get(reverse('boards:new_topic', kwargs={'id': self.board.id}))

    def test_new_topic_view_success_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_new_topic_url_url_resolves_to_new_topic_view(self):
        view = resolve('/boards/1/new/')
        self.assertEquals(view.func, new_topic)

    def test_new_topic_view_not_found_status_code(self):
        response = self.client.get(reverse('boards:new_topic', kwargs={'id': 100}))
        self.assertEquals(response.status_code, 404)

    def test_new_topic_view_contains_link_to_Boards_topic_view(self):
        board_topic_url = reverse('boards:topics', kwargs={'d': 1})
        new_topic_url = reverse('boards:new_topic', kwargs={'id': 1})
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(board_topic_url))

    def test_csrf(self):
        url = reverse('boards:new_topic', kwargs={'id': self.board.id})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):
        url = reverse('boards:new_topic', kwargs={'id': self.board.id})
        data = {
            'subject': 'Test title',
            'message': 'Lorem ipsum dolor sit amet'
        }
        response = self.client.post(url, data)
        self.assertTrue(topic.objects.exists())
        self.assertTrue(post.objects.exists())

    def test_new_topic_invalid_post_data(self):
        url = reverse('boards:new_topic', kwargs={'id': self.board.id})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_topic_invalid_post_data_empty_fields(self):
        url = reverse('boards:new_topic', kwargs={'id': self.board.id})
        data = {
            'message': '',
            'subject': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(topic.objects.exists())
        self.assertFalse(post.objects.exists())

    def test_contains_form(self):  # <- new test
        url = reverse('boards:new_topic', kwargs={'id': 1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)





