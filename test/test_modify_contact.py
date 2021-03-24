from model.contact import Contact

def test_modify_first_contact(app):
    app.session.login(username="admin", password="secret")
    app.contact.modify_first(Contact("N.Isa", "I.Ivach", "N.Nos", "N.pes-barbos", "N.title for barbos", "N.something company",
                        "St.Peterburg", "87771234567", "unknown1", "unknown2", "unknown3", "N.barbos@mail.ru", "unknown4",
                        "unknown5", "http://new.barbos.page.org", "unknown6", "This is NEW contact for barbos", "unknown7"))
    app.session.logout()