# -*- coding: utf-8 -*-
from model.contact import Contact

def test_new_contact(app):
    app.session.login(username="admin", password="secret")
    app.contact.create_contact(Contact("Isaak", "Ivanovich", "Nosov", "pes-barbos", "title for barbos", "something company",
                        "Moscow, red square, 1", "89991234567", "none1", "none2", "none3", "barbos@mail.ru", "none4",
                        "none5", "http://barbos.page.org", "none6", "This is contact for barbos", "none7"))
    app.session.logout()

def test_new_empty_contact(app):
    app.session.login(username="admin", password="secret")
    app.contact.create_contact(Contact("", "", "", "", "", "",
                        "", "", "", "", "", "", "",
                        "", "", "", "", ""))
    app.session.logout()