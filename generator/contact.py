from model.contact import Contact
import random
import string
import os.path
import jsonpickle
import getopt
import sys

try:
    opts, args = getopt.getopt(sys.argv[1:], "n:f:", ["contact count", "output file"])
except getopt.GetoptError as err:
    getopt.usage()
    sys.exit(2)

n = 3
f = "data/contacts.json"

for o, a in opts:
        if o == "-n":
            n = int(a)
        elif o == "-f":
            f == a

def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + string.punctuation + " "*10
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])

testdata = [Contact(fName="", mName="", lName="", nick="", title="",
                    company="", address="", mobile="", home_phone="",
                    work_phone="", fax="", email="", email2="",
                    email3="", homePage="", phone2="", notes="",
                    address2="", homephone="", mobilephone="",
                    workphone="", secondaryphone="")] + \
    [Contact(
            fName = random_string("fName", 10),
            mName = random_string("mName", 10),
            lName = random_string("lName", 10),
            nick = random_string("nick", 20),
            title = random_string("title", 20),
            company = random_string("company", 20),
            address = random_string("address", 30),
            mobile = random_string("mobile", 10),
            home_phone = random_string("home_phone", 10),
            work_phone = random_string("work_phone", 10),
            fax = random_string("fax", 10),
            email = random_string("email", 20),
            email2 = random_string("email2", 20),
            email3 = random_string("email3", 20),
            homePage = random_string("homePage", 20),
            phone2 = random_string("phone2", 10),
            notes = random_string("notes", 30),
            address2 = random_string("address2", 10),
            homephone = random_string("homephone", 10),
            mobilephone = random_string("mobilephone", 10),
            workphone = random_string("workphone", 10),
            secondaryphone = random_string("secondaryphone", 10))
    for i in range(n)
]

file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", f)

with open(file, "w") as out:
    jsonpickle.set_encoder_options("json", indent=2)
    out.write(jsonpickle.encode(testdata))