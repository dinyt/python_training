# -*- coding: utf-8 -*-
from model.contact import Contact
import pytest
import random
import string

def random_any_symbols(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + string.punctuation + " "*10
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])

def random_digits(prefix, maxlen):
    symbols = string.digits
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])

def random_string(prefix, maxlen):
    symbols = string.ascii_letters
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])

testdata = [Contact(fName = "", mName = "", lName = "", nick = "", title = "", company = "",
            address = "", mobile = "", home_phone = "", work_phone = "", fax = "",
            email = "", email2 = "", email3 = "", homePage = "", phone2 = "", notes = "",
            address2 = "", id = "", homephone = "", mobilephone = "", workphone = "",
            secondaryphone = "")] + \
[
    Contact(fName = random_string("fName", 10),
            mName = random_string("mName", 10),
            lName = random_string("lName", 10),
            nick = random_any_symbols("nick", 20),
            title = random_any_symbols("title", 20),
            company = random_any_symbols("company", 20),
            address = random_string("address", 30),
            mobile = random_digits("mobile", 10),
            home_phone = random_digits("home_phone", 10),
            work_phone = random_digits("work_phone", 10),
            fax = random_digits("fax", 10),
            email = random_string("email", 20),
            email2 = random_string("email2", 20),
            email3 = random_string("email3", 20),
            homePage = random_string("homePage", 20),
            phone2 = random_digits("phone2", 10),
            notes = random_any_symbols("notes", 30),
            address2 = random_string("address2", 10),
            homephone = random_digits("homephone", 10),
            mobilephone = random_digits("mobilephone", 10),
            workphone = random_digits("workphone", 10),
            secondaryphone = random_digits("secondaryphone", 10))
    for i in range(5)
]

@pytest.mark.parametrize("contact", testdata, ids=[repr(x) for x in testdata])
def test_new_contact(app, contact):
    old_contacts = app.contact.get_contact_list()
    app.contact.create(contact)
    assert len(old_contacts) + 1 == app.contact.count()
    new_contacts = app.contact.get_contact_list()
    old_contacts.append(contact)
    assert sorted(old_contacts, key=Contact.id_or_max) == sorted(new_contacts, key=Contact.id_or_max)