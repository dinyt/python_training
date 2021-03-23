# -*- coding: utf-8 -*-
from fixture.application import Application
from model.contact import Contact
import pytest

@pytest.fixture
def app(request):
    fixture = Application()
    request.addfinalizer(fixture.destroy)
    return fixture

def test_new_contact(app):
    app.login(username="admin", password="secret")
    app.create_contact(Contact("Isaak", "Ivanovich", "Nosov", "pes-barbos", "title for barbos", "something company",
                        "Moscow, red square, 1", "89991234567", "none1", "none2", "none3", "barbos@mail.ru", "none4",
                        "none5", "http://barbos.page.org", "none6", "This is contact for barbos", "none7"))
    app.logout()

def test_new_empty_contact(app):
    app.login(username="admin", password="secret")
    app.create_contact(Contact("", "", "", "", "", "",
                        "", "", "", "", "", "", "",
                        "", "", "", "", ""))
    app.logout()