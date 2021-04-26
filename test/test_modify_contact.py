from model.contact import Contact
import random

def test_modify_any_contact(app, db, check_ui):
    if db.get_contact_list() == 0:
        app.contact.create(Contact("", "", "", "", "", "",
                        "", "", "", "", "", "", "",
                        "", "", "", "", ""))
    old_contacts = db.get_contact_list()
    contact = random.choice(old_contacts)
    new_contact = Contact("N.Isa", "I.Ivach", "N.Nos", "N.pes-barbos", "N.title for barbos",
        "N.something company", "St.Peterburg", "87771234567", "unknown1", "unknown2", "unknown3", "N.barbos@mail.ru",
        "unknown4", "unknown5", "http://new.barbos.page.org", "unknown6", "This is NEW contact for barbos", "unknown7")
    app.contact.modify_by_id(contact.id, new_contact)
    assert len(old_contacts) == app.contact.count()
    new_contacts = db.get_contact_list()
    index = 0
    for cnt in old_contacts:
        if cnt.id == contact.id:
            break
        index = index + 1
    new_contact.id = contact.id
    old_contacts[index] = new_contact
    assert sorted(old_contacts, key=Contact.id_or_max) == sorted(new_contacts, key=Contact.id_or_max)
    if check_ui:
        assert sorted(new_contacts, key=Contact.id_or_max) == sorted(app.contact.get_contact_list(), key=Contact.id_or_max)