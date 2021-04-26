from model.contact import Contact
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