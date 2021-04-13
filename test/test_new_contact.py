# -*- coding: utf-8 -*-
from model.contact import Contact

def test_new_contact(app):
    old_contacts = app.contact.get_contact_list()
    contact = Contact("Isaak", "Ivanovich", "Nosov", "pes-barbos", "title for barbos", "something company",
                        "Moscow, red square, 1", "89991234567", "none1", "none2", "none3", "barbos@mail.ru", "none4",
                        "none5", "http://barbos.page.org", "none6", "This is contact for barbos", "none7")
    app.contact.create(contact)
    new_contacts = app.contact.get_contact_list()
    assert len(old_contacts) + 1 == len(new_contacts)
    old_contacts.append(contact)
    assert sorted(old_contacts, key=Contact.id_or_max) == sorted(new_contacts, key=Contact.id_or_max)

def test_new_empty_contact(app):
    old_contacts = app.contact.get_contact_list()
    contact = Contact("", "", "", "", "", "",
                        "", "", "", "", "", "", "",
                        "", "", "", "", "")
    app.contact.create(contact)
    new_contacts = app.contact.get_contact_list()
    assert len(old_contacts) + 1 == len(new_contacts)
    old_contacts.append(contact)
    assert sorted(old_contacts, key=Contact.id_or_max) == sorted(new_contacts, key=Contact.id_or_max)