from model.contact import Contact
from model.group import Group
import random
from random import randrange

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
    if app.contact.count() == 0:
        suffix = str(random.randint(10000, 99999))
        app.contact.create(Contact(fName='New fName ' + suffix,
                                   lName='New lName ' + suffix,
                                   mName= 'New mName ' + suffix))

    if app.group.count() == 0:
        suffix = str(random.randint(10000, 99999))
        app.contact.create(Group(name='New group #' + suffix,
                                 header='New header #' + suffix,
                                 footer='New footer #' + suffix))

    groups = orm.get_group_list()
    index_group = randrange(len(groups))
    group = groups[index_group]
    contacts = orm.get_contacts_in_group(group)

    if len(contacts) == 0:
        contacts = orm.get_contact_list()
        index = randrange(len(contacts))
        contact = contacts[index]
        app.contact.add_contact_to_group(contact, group)
    else:
        index = randrange(len(contacts))
        contact = contacts[index]

    app.contact.delete_contact_from_group(contact, group)

    contacts_in_group = orm.get_contacts_in_group(group)

    assert contact not in contacts_in_group