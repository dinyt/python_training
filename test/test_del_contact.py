from model.contact import Contact
from model.group import Group
import random

def test_delete_any_contact(app, db, check_ui):
    if db.get_contact_list() == 0:
        app.contact.create(Contact("", "", "", "", "", "",
                        "", "", "", "", "", "", "",
                        "", "", "", "", ""))
    old_contacts = db.get_contact_list()
    contact = random.choice(old_contacts)
    app.contact.delete_by_id(contact.id)
    new_contacts = db.get_contact_list()
    assert len(old_contacts) - 1 == app.contact.count()
    old_contacts.remove(contact)
    assert old_contacts == new_contacts
    if check_ui:
        assert sorted(new_contacts, key=Contact.id_or_max) == sorted(app.contact.get_contact_list(), key=Contact.id_or_max)

def test_delete_random_contact_from_group(app, orm):
    group_list = orm.get_group_list()
    contacts = list()
    group = Group(id='[none]')
    for gr in group_list:
        count_contacts = orm.get_count_contacts_in_group(Group(id=gr.id))
        if count_contacts > 0:
            group = gr
            contacts = orm.get_contacts_in_group(Group(id=gr.id))
            break
    contact = contacts[random.randint(0, len(contacts) - 1)]
    app.contact.set_listgroup_for_contacts(group)
    app.contact.select_contact_by_id(contact.id)
    app.contact.delete_contact_from_selected_group()
    assert orm.contact_in_group(contact, group) == False