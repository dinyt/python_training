from model.contact import Contact
from random import randrange

def test_modify_first_contact(app):
    if app.contact.count() == 0:
        app.contact.create(Contact("", "", "", "", "", "",
                        "", "", "", "", "", "", "",
                        "", "", "", "", ""))
    old_contacts = app.contact.get_contact_list()
    index = randrange(len(old_contacts))
    contact = Contact("N.Isa", "I.Ivach", "N.Nos", "N.pes-barbos", "N.title for barbos",
        "N.something company", "St.Peterburg", "87771234567", "unknown1", "unknown2", "unknown3", "N.barbos@mail.ru",
        "unknown4", "unknown5", "http://new.barbos.page.org", "unknown6", "This is NEW contact for barbos", "unknown7")
    contact.id = old_contacts[index].id
    app.contact.modify_by_index(index, contact)
    assert len(old_contacts) == app.contact.count()
    new_contacts = app.contact.get_contact_list()
    old_contacts[index] = contact
#    assert sorted(old_contacts, key=Contact.id_or_max) == sorted(new_contacts, key=Contact.id_or_max)