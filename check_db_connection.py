from fixture.orm import ORMFixture
import random
from model.group import Group
from model.contact import Contact

db = ORMFixture(host='localhost',
               user='root',
               password='',
               name='addressbook')

try:
    cnt = db.get_count_contacts_in_group(Group(id=49))
    print('\ncnt = ' + str(cnt))
    #l = db.get_contacts_in_group(Group(id=49))
    #if db.get_count_groups_for_contact(Contact(id=83)) > 0:
        #l = db.get_groups_for_contact(Contact(id=83))
        #contacts = db.get_group_list()
        #l = db.get_group_list()
    #for item in l:
    #    print(item)
    #print(len(l))
    #group = random.choice(l)
    #print("size: " + str(group))
    #else:
     #   print('No groups')
finally:
    pass
    #db.destroy()
