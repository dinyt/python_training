# -*- coding: utf-8 -*-
from operator import contains

from model.contact import Contact
import random
from fixture.orm import ORMFixture
from model.group import Group
#import pytest

#@pytest.mark.parametrize("contact", testdata, ids=[repr(x) for x in testdata])
def test_new_contact(app, db, json_contacts):
    contact = json_contacts
    old_contacts = db.get_contact_list()
    app.contact.create(contact)
    # assert len(old_contacts) + 1 == app.contact.count()
    new_contacts = db.get_contact_list()
    old_contacts.append(contact)
    assert sorted(old_contacts, key=Contact.id_or_max) == sorted(new_contacts, key=Contact.id_or_max)

def test_add_contact_with_group(app, db, json_contacts):
    contact = json_contacts
    old_contacts = db.get_contact_list()
    select_group_from_list = random.choice(db.get_group_list())
    contact.groupId = select_group_from_list.id
    contact.groupName = select_group_from_list.name
    print("Select group: " + str(select_group_from_list))
    app.contact.create(contact)
    new_contacts = db.get_contact_list()
    old_contacts.append(contact)
    assert sorted(old_contacts, key=Contact.id_or_max) == sorted(new_contacts, key=Contact.id_or_max)

def test_add_random_contact_to_random_group(app, orm):
    select_group_from_list = random.choice(orm.get_group_list())
    for i in range(10):
        contacts = orm.get_contacts_not_in_group(select_group_from_list)
        if contacts != list():
            break
        else:
            continue
    index = len(contacts)
    index = random.randint(0, index - 1)
    contact = contacts[index]
    app.contact.select_contact_by_id(contact.id)
    app.contact.add_contact_to_selected_group(select_group_from_list)
    assert orm.contact_in_group(contact, select_group_from_list) == True


def test_add_random_contact_to_random_group2(app, orm):
    new_group = None
    new_contact = None

    groups = orm.get_group_list()
    if len(groups) == 0:
        suffix = str(random.randint(10000, 99999))
        new_group = Group(name='New group #' + suffix,
                          header='New header #' + suffix,
                          footer='New footer #' + suffix)
        app.group.create(new_group)

    contacts = orm.get_contact_list()
    if len(contacts) == 0:
        suffix = str(random.randint(10000, 99999))
        new_contact = Contact(fName='New fName ' + suffix,
                              lName='New lName ' + suffix,
                              mName= 'New mName ' + suffix)
        app.contact.create(new_contact)

    if new_group is None:
        index = random.randint(0, len(groups) - 1)
        new_group = groups[index]

        if new_contact is None:
            for new_group in groups:
                contacts = orm.get_contacts_not_in_group(new_group)
                if len(contacts) != 0:
                    index = random.randint(0, len(contacts) - 1)
                    new_contact = contacts[index]
                    break

    app.contact.select_contact_by_id(new_contact.id)
    app.contact.add_contact_to_selected_group(new_group)
    assert orm.contact_in_group(new_contact, new_group) == True