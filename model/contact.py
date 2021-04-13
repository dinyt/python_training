from sys import maxsize

class Contact:
    def __init__(self, fName = None, mName = None, lName = None, nick = None, title = None, company = None,
                 address = None, mobile = None, home_phone = None, work_phone = None, fax = None,
                 email = None, email2 = None, email3 = None, homePage = None, phone2 = None, notes = None,
                 address2 = None, id = None):
        self.fName = fName
        self.mName = mName
        self.lName = lName
        self.nick = nick
        self.title = title
        self.company = company
        self.address = address
        self.mobile = mobile
        self.home_phone = home_phone
        self.work_phone = work_phone
        self.fax = fax
        self.email = email
        self.email2 = email2
        self.email3 = email3
        self.homePage = homePage
        self.phone2 = phone2
        self.notes = notes
        self.address2 = address2
        self.id = id

    def __repr__(self):
        return "%s:%s %s" % (self.id, self.fName, self.lName)

    def __eq__(self, other):
        return ((self.id is None) or (other.id is None) or (self.id == other.id)) and (self.fName == other.fName) and (self.lName == other.lName)

    def id_or_max(self):
        if self.id:
            return int(self.id)
        else:
            return maxsize