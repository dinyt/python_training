from fixture.db import DbFixture

db = DbFixture(host='localhost',
               user='root',
               password='',
               name='addressbook')

try:
    #groups = db.get_group_list()
    contacts = db.get_contact_list()
    for contact in contacts:
        print(contact)
    print(len(contacts))
finally:
    db.destroy()
