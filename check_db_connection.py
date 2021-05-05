from fixture.orm import ORMFixture
from model.group import Group

db = ORMFixture(host='localhost',
               user='root',
               password='',
               name='addressbook')

try:
    l = db.get_contacts_not_in_group(Group(id=49))
    #contacts = db.get_group_list()
    for item in l:
        print(item)
    print(len(l))
finally:
    pass
    #db.destroy()
