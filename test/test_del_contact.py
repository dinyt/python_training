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
        suffix = str(random.randint(1000000, 9999999))
        app.contact.create(Contact(fName='New fName ' + suffix,
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
                                   secondaryphone='Secondary ' + suffix))

    if app.group.count() == 0:
        suffix = str(random.randint(10000, 99999))
        app.group.create(Group(name='New group #' + suffix,
                               header='New header #' + suffix,
                               footer='New footer #' + suffix))

    # groups = orm.get_group_list()
    # index_group = randrange(len(groups))
    # group = groups[index_group]
    # contacts = orm.get_contacts_in_group(group)

    # устанавливаем признак списка контактов, которые содержатся в какой-нибудь группе
    flag = False
    # получаем список групп
    groups = orm.get_group_list()
    # проверяем среди всех групп
    for group in groups:
        # контакты, которые содержатся в очередной группе
        contact_list = orm.get_contacts_in_group(group)
        # и если результирующий список контактов (для очередной группы) не пуст
        if len(contact_list) != 0:
            # тогда помечаем признак
            flag = True
            # запоминаем группу (чтобы потом из неё удалить контакт из списка)
            gr = group
            # и выходим из цикла
            break

    # если найден список контактов, которые содержатся в какой-нибудь группе
    if flag:
        # берём случайный индекс
        index = randrange(len(contact_list))
        # и по этому индексу запоминаем контакт из списка
        contact = contact_list[index]
        # а также группу, из которой будем удалять контакт
        group = gr
    # иначе, если такой список обнаружен не был
    else:
        # выбираем любую группу из списка
        groups = orm.get_group_list()
        index_group = randrange(len(groups))
        # запоминаем её
        group = groups[index_group]

        # выбираем любой контакт из списка
        contacts = orm.get_contact_list()
        index = randrange(len(contacts))
        # запоминаем его
        contact = contacts[index]
        # и добавляем этот контакт в группу group
        app.contact.add_contact_to_group(contact, group)

    # if len(contacts) == 0:
    #     contacts = orm.get_contact_list()
    #     index = randrange(len(contacts))
    #     contact = contacts[index]
    #     app.contact.add_contact_to_group(contact, group)
    # else:
    #     index = randrange(len(contacts))
    #     contact = contacts[index]

    # удаляем контакт contact из группы group
    app.contact.delete_contact_from_group(contact, group)
    # получаем список всех контактов в группе, в которую добавили контакт
    contacts_in_group = orm.get_contacts_in_group(group)

    # проверяем отсутствие контакта contact в список контактов
    assert contact not in contacts_in_group