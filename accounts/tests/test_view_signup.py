from django.test import TestCase
from ..views import signup
from django.urls import resolve, reverse
from ..forms import SignUpForm
from django.contrib.auth.models import User


class SignUpTest(TestCase):

    def setUp(self):
        url = reverse('boards:signup')
        self.response=self.client.get(url)

    def test_signup_view_success_status_code(self):
        url = reverse('boards:signup')
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_to_signup_view(self):
        view = resolve('/boards/signup/')
        self.assertEquals(view.func, signup)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)


class SuccessfulSignUpTest(TestCase):

    def setUp(self):
        url = reverse('boards:signup')
        data = {
            'username': 'john',
            'email':'test@test.com',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('boards:home')

    def test_redirection(self):
        self.assertRedirects(self.response, self.home_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        '''
                Create a new request to an arbitrary page.
                The resulting response should now have a `user` to its context,
                after a successful sign up.
        '''
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)






