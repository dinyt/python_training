import re
from random import randrange
from fixture.db import DbFixture
from model.contact import Contact

def test_phones_on_home_page(app):
    contact_from_home_page = app.contact.get_contact_list()[0]
    contact_from_edit_page = app.contact.get_contact_info_from_edit_page(0)
    assert contact_from_home_page.all_phones_from_home_page == merge_phones_like_on_home_page(contact_from_edit_page)

def test_phones_on_contact_view_page(app):
    contact_from_view_page = app.contact.get_contact_from_view_page(0)
    contact_from_edit_page = app.contact.get_contact_info_from_edit_page(0)
    assert contact_from_view_page.homephone == contact_from_edit_page.homephone
    assert contact_from_view_page.workphone == contact_from_edit_page.workphone
    assert contact_from_view_page.mobilephone == contact_from_edit_page.mobilephone
    assert contact_from_view_page.secondaryphone == contact_from_edit_page.secondaryphone

def test_compare_info_between_main_and_edit_pages(app):
    count_contacts = app.contact.get_contact_list()
    index = randrange(len(count_contacts))
    contact_from_home_page = app.contact.get_contact_list()[index]
    contact_from_edit_page = app.contact.get_contact_info_from_edit_page(index)
    assert contact_from_home_page.all_phones_from_home_page == merge_phones_like_on_home_page(contact_from_edit_page)
    assert contact_from_home_page.all_emails_from_home_page == merge_emails_like_on_home_page(contact_from_edit_page)
    assert contact_from_home_page.fName == contact_from_edit_page.fName
    assert contact_from_home_page.lName == contact_from_edit_page.lName
    assert contact_from_home_page.address == contact_from_edit_page.address

def test_compare_info_all_contacts_on_main_page_and_info_from_db(app, db):
    all_contacts_from_main_page = sorted(app.contact.get_contact_list(), key=Contact.id_or_max)
    all_contacts_from_db = sorted(db.get_contact_list(), key=Contact.id_or_max)
    i = 0
    for item in all_contacts_from_main_page:
        assert all_contacts_from_main_page[i].id == all_contacts_from_db[i].id
        assert all_contacts_from_main_page[i].fName == all_contacts_from_db[i].fName
        assert all_contacts_from_main_page[i].lName == all_contacts_from_db[i].lName
        assert all_contacts_from_main_page[i].address == all_contacts_from_db[i].address
        assert all_contacts_from_main_page[i].all_phones_from_home_page == merge_phones_like_on_home_page(
            all_contacts_from_db[i])
        assert all_contacts_from_main_page[i].all_emails_from_home_page == merge_emails_like_on_home_page(
            all_contacts_from_db[i])
        i = i + 1

def clear(s):
    return re.sub("[() -]", "", s)

def merge_phones_like_on_home_page(contact):
    return "\n".join(filter(lambda x: x != "",
        map(lambda x: clear(x),
            filter(lambda x: x is not None,
                   [contact.homephone, contact.mobilephone, contact.workphone, contact.secondaryphone]))))

def merge_emails_like_on_home_page(contact):
    return "\n".join(filter(lambda x: x != "",
        map(lambda x: clear(x),
            filter(lambda x: x is not None,
                   [contact.email, contact.email2, contact.email3]))))