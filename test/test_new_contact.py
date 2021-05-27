# -*- coding: utf-8 -*-
from operator import contains

from model.contact import Contact
import random
from random import randrange
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
    def generate_contact():
        suffix = str(random.randint(10000, 99999))
        return Contact(fName='New fName ' + suffix,
                       lName='New lName ' + suffix,
                       mName='New mName ' + suffix,
                       nick='Nick ' + suffix,
                       title='Title ' + suffix,
                       company='Company ' + suffix,
                       address='Address ' + suffix,
                       mobile='Mobile ' + suffix,
                       home_phone='Home ' + suffix,
                       work_phone='Work' + suffix,
                       fax='Fax ' + suffix,
                       email='Email@' + suffix,
                       email2='Email2@' + suffix,
                       email3='Email3@' + suffix,
                       homePage='Home ' + suffix,
                       phone2='Phone2 ' + suffix,
                       notes='Notes: ' + suffix,
                       address2='Address2 ' + suffix,
                       homephone='Home ' + suffix,
                       mobilephone='Mobile ' + suffix,
                       workphone='Work ' + suffix,
                       secondaryphone='Secondary ' + suffix)

    if app.contact.count() == 0:
        contact = generate_contact()
        app.contact.create(contact)

    if app.group.count() == 0:
        suffix = str(random.randint(1000000, 9999999))
        app.group.create(Group(name='New group #' + suffix,
                                 header='New header #' + suffix,
                                 footer='New footer #' + suffix))

    # old_contacts = orm.get_contact_list()
    # groups = orm.get_group_list()
    # index = randrange(len(old_contacts))
    # index_group = randrange(len(groups))
    # group = groups[index_group]
    # contact = old_contacts[index]
    # contacts_in_group = orm.get_contacts_in_group(group)
    #
    # if contact in contacts_in_group:
    #     app.contact.delete_contact_from_group(contact, group)

    # устанавливаем признак списка контактов, которые не содержатся в какой-нибудь группе
    flag = False
    # получаем список групп
    groups = orm.get_group_list()
    # проверяем среди всех групп
    for group in groups:
        # контакты, которые не содержатся в очередной группе
        contact_list = orm.get_contacts_not_in_group(group)
        # и если результирующий список контактов (для очередной группы) не пуст
        if len(contact_list) != 0:
            # тогда помечаем признак
            flag = True
            # запоминаем группу (чтобы потом в неё добавить контакт из списка)
            gr = group
            # и выходим из цикла
            break

    # если найден список контактов, которые не содержатся в какой-нибудь группе
    if flag:
        # берём случайный индекс
        index = randrange(len(contact_list))
        # и по этому индексу запоминаем контакт из списка
        contact = contact_list[index]
        # а также группу, в которую будем добавлять контакт
        group = gr
    # иначе, если такой список обнаружен не был
    else:
        # то создаём новый контакт
        contact = generate_contact()
        app.contact.create(contact)
        # и выбираем случайную группу из списка групп по индексу
        index_group = randrange(len(groups))
        group = groups[index_group]

    # добавляем в заранее определённую группу подготовленный контакт
    app.contact.add_contact_to_group(contact, group)
    # получаем список всех контактов в группе, в которую добавили контакт
    contacts_in_group = orm.get_contacts_in_group(group)

    # проверяем вхождение подготовленного контакта в список контактов
    assert contact in contacts_in_group