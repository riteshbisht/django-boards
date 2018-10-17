from ..forms import SignUpForm
from django.test import TestCase


def test_form_has_fields(TestCase):
    form = SignUpForm()
    expected = ['Username', 'email', 'password1', 'password2']
    actual = list(form.field)
    self.assertSequence(expected, actual)
