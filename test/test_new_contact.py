# -*- coding: utf-8 -*-
from model.contact import Contact

def test_new_contact(app):
    app.contact.create_contact(Contact("Isaak", "Ivanovich", "Nosov", "pes-barbos", "title for barbos", "something company",
                        "Moscow, red square, 1", "89991234567", "none1", "none2", "none3", "barbos@mail.ru", "none4",
                        "none5", "http://barbos.page.org", "none6", "This is contact for barbos", "none7"))

def test_new_empty_contact(app):
    app.contact.create_contact(Contact("", "", "", "", "", "",
                        "", "", "", "", "", "", "",
                        "", "", "", "", ""))