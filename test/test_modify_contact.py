from model.contact import Contact

def test_modify_first_contact(app):
    if app.contact.count() == 0:
        app.contact.create(Contact("", "", "", "", "", "",
                        "", "", "", "", "", "", "",
                        "", "", "", "", ""))
    old_contacts = app.contact.get_contact_list()
    contact = Contact("N.Isa", "I.Ivach", "N.Nos", "N.pes-barbos", "N.title for barbos",
        "N.something company", "St.Peterburg", "87771234567", "unknown1", "unknown2", "unknown3", "N.barbos@mail.ru",
        "unknown4", "unknown5", "http://new.barbos.page.org", "unknown6", "This is NEW contact for barbos", "unknown7")
    contact.id = old_contacts[0].id
    app.contact.modify_first(contact)
    new_contacts = app.contact.get_contact_list()
    assert len(old_contacts) == len(new_contacts)
    old_contacts[0] = contact
    assert sorted(old_contacts, key=Contact.id_or_max) == sorted(new_contacts, key=Contact.id_or_max)