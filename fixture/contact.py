from model.contact import Contact
from selenium.webdriver.support.ui import Select
from fixture.orm import ORMFixture
import re

class ContactHelper():

    def __init__(self, app):
        self.app = app

    def create(self, contact):
        wd = self.app.wd
        # click add contact
        wd.find_element_by_link_text("add new").click()
        self.fill_form_contact(contact)
        # save contact
        wd.find_element_by_xpath("(//input[@name='submit'])[2]").click()
        self.return_to_home_page()
        self.contact_cache = None

    def create_with_group(self, contact):
        wd = self.app.wd
        # click add contact
        wd.find_element_by_link_text("add new").click()
        self.fill_form_contact(contact)
        # save contact
        wd.find_element_by_xpath("(//input[@name='submit'])[2]").click()
        self.return_to_home_page()
        self.contact_cache = None

    def fill_form_contact(self, contact):
        wd = self.app.wd
        wd.find_element_by_name("firstname").clear()
        wd.find_element_by_name("firstname").send_keys(contact.fName)
        wd.find_element_by_name("middlename").clear()
        wd.find_element_by_name("middlename").send_keys(contact.mName)
        wd.find_element_by_name("lastname").clear()
        wd.find_element_by_name("lastname").send_keys(contact.lName)
        wd.find_element_by_name("nickname").clear()
        wd.find_element_by_name("nickname").send_keys(contact.nick)
        wd.find_element_by_name("title").clear()
        wd.find_element_by_name("title").send_keys(contact.title)
        wd.find_element_by_name("company").clear()
        wd.find_element_by_name("company").send_keys(contact.company)
        wd.find_element_by_name("address").clear()
        wd.find_element_by_name("address").send_keys(contact.address)
        wd.find_element_by_name("home").clear()
        wd.find_element_by_name("home").send_keys(contact.home_phone)
        wd.find_element_by_name("mobile").clear()
        wd.find_element_by_name("mobile").send_keys(contact.mobile)
        wd.find_element_by_name("work").clear()
        wd.find_element_by_name("work").send_keys(contact.work_phone)
        wd.find_element_by_name("fax").clear()
        wd.find_element_by_name("fax").send_keys(contact.fax)
        wd.find_element_by_name("email").clear()
        wd.find_element_by_name("email").send_keys(contact.email)
        wd.find_element_by_name("email2").clear()
        wd.find_element_by_name("email2").send_keys(contact.email2)
        wd.find_element_by_name("email3").clear()
        wd.find_element_by_name("email3").send_keys(contact.email3)
        wd.find_element_by_name("homepage").clear()
        wd.find_element_by_name("homepage").send_keys(contact.homePage)
        wd.find_element_by_name("address2").clear()
        wd.find_element_by_name("address2").send_keys(contact.address2)
        wd.find_element_by_name("phone2").clear()
        wd.find_element_by_name("phone2").send_keys(contact.phone2)
        wd.find_element_by_name("notes").clear()
        wd.find_element_by_name("notes").send_keys(contact.notes)
        wd.find_element_by_name("new_group").click()
        if contact.groupId is not None:
            Select(wd.find_element_by_name("new_group")).select_by_value(contact.groupId)
        else:
            Select(wd.find_element_by_name("new_group")).select_by_visible_text(contact.groupName)


    def return_to_home_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("/addressbook/") and len(wd.find_elements_by_link_text("add new")) > 0):
            wd.find_element_by_link_text("home").click()

    def modify_first(self, contact):
        self.modify_by_index(0, contact)

    def modify_by_index(self, index, contact):
        wd = self.app.wd
        self.click_edit_contact_by_index(index)
        self.fill_form_contact(contact)
        # update contact
        wd.find_element_by_name("update").click()
        self.return_to_home_page()
        self.contact_cache = None

    def modify_by_id(self, id, contact):
        wd = self.app.wd
        self.click_edit_contact_by_id(id)
        self.fill_form_contact(contact)
        # update contact
        wd.find_element_by_name("update").click()
        self.return_to_home_page()
        self.contact_cache = None

    def click_edit_contact_by_index(self, index):
        wd = self.app.wd
        wd.find_elements_by_xpath("//img[@alt='Edit']")[index].click()

    def click_edit_contact_by_id(self, id):
        wd = self.app.wd
        wd.find_element_by_css_selector('a[href="edit.php?id=%s"]' % id).click()

    def delete_first(self):
        self.delete_by_index(0)

    def delete_by_index(self, index):
        wd = self.app.wd
        self.select_contact_by_index(index)
        self.click_delete_contact()
        # accept deletion
        wd.switch_to_alert().accept()
        wd.implicitly_wait(3)
        self.return_to_home_page()
        self.contact_cache = None

    def delete_by_id(self, id):
        wd = self.app.wd
        self.select_contact_by_id(id)
        self.click_delete_contact()
        # accept deletion
        wd.switch_to_alert().accept()
        wd.implicitly_wait(3)
        self.return_to_home_page()
        self.contact_cache = None

    def select_contact_by_index(self, index):
        wd = self.app.wd
        wd.find_elements_by_xpath("//tr/td/input")[index].click()

    def select_contact_by_id(self, id):
        self.return_to_home_page()
        wd = self.app.wd
        wd.find_element_by_css_selector("input[value='%s']" % id).click()

    def click_delete_contact(self):
        wd = self.app.wd
        wd.find_element_by_xpath("//input[@value='Delete']").click()

    def count(self):
        wd = self.app.wd
        self.return_to_home_page()
        return len(wd.find_elements_by_name("selected[]"))

    contact_cache = None

    def get_contact_list(self):
        if self.contact_cache is None:
            wd = self.app.wd
            self.return_to_home_page()
            self.contact_cache = []
            for element in wd.find_elements_by_name("entry"):
                cells = element.find_elements_by_tag_name("td")
                firstName = cells[2].text
                lastName = cells[1].text
                id = cells[0].find_element_by_tag_name("input").get_attribute("id")
                all_phones = cells[5].text
                address = cells[3].text
                all_emails = cells[4].text
                self.contact_cache.append(Contact(fName=firstName, lName=lastName, id=id,
                                          all_phones_from_home_page=all_phones,
                                          all_emails_from_home_page=all_emails,
                                          address=address))
        return list(self.contact_cache)

    def open_contact_to_edit_by_index(self, index):
        wd = self.app.wd
        self.return_to_home_page()
        row = wd.find_elements_by_name('entry')[index]
        cell = row.find_elements_by_tag_name("td")[7]
        cell.find_element_by_tag_name("a").click()

    def open_contact_to_view_by_index(self, index):
        wd = self.app.wd
        self.return_to_home_page()
        row = wd.find_elements_by_name('entry')[index]
        cell = row.find_elements_by_tag_name("td")[6]
        cell.find_element_by_tag_name("a").click()

    def get_contact_info_from_edit_page(self, index):
        wd = self.app.wd
        self.open_contact_to_edit_by_index(index)
        firstname = wd.find_element_by_name("firstname").get_attribute("value")
        lastname = wd.find_element_by_name("lastname").get_attribute("value")
        id = wd.find_element_by_name("id").get_attribute("value")
        homephone = wd.find_element_by_name("home").get_attribute("value")
        workphone = wd.find_element_by_name("work").get_attribute("value")
        mobilephone = wd.find_element_by_name("mobile").get_attribute("value")
        secondaryphone = wd.find_element_by_name("phone2").get_attribute("value")
        address = wd.find_element_by_name("address").get_attribute("value")
        email = wd.find_element_by_name("email").get_attribute("value")
        email2 = wd.find_element_by_name("email2").get_attribute("value")
        email3 = wd.find_element_by_name("email3").get_attribute("value")
        return Contact(fName=firstname, lName=lastname, id=id,
                       homephone=homephone, mobilephone=mobilephone,
                       workphone=workphone,secondaryphone=secondaryphone,
                       address=address, email=email, email2=email2, email3=email3)

    def get_contact_from_view_page(self, index):
        wd = self.app.wd
        self.open_contact_to_view_by_index(index)
        text = wd.find_element_by_id("content").text
        homephone = re.search("H: (.*)", text).group(1)
        workphone = re.search("W: (.*)", text).group(1)
        mobilephone = re.search("M: (.*)", text).group(1)
        secondaryphone = re.search("P: (.*)", text).group(1)
        return Contact(homephone=homephone, mobilephone=mobilephone,
                       workphone=workphone, secondaryphone=secondaryphone)

    def set_listgroup_for_contacts(self, group):
        wd = self.app.wd
        self.return_to_home_page()
        if group.id == '[all]':
            self.return_to_home_page()
        elif group.id == '[none]':
            Select(wd.find_element_by_name("group")).select_by_value('[none]')
        else:
            Select(wd.find_element_by_name("group")).select_by_value(group.id)

    def add_contact_to_selected_group(self, group):
        wd = self.app.wd
        Select(wd.find_element_by_name("to_group")).select_by_value(group.id)
        wd.find_element_by_name("add").click()

    def delete_contact_from_selected_group(self):
        wd = self.app.wd
        wd.find_element_by_name("remove").click()

    def add_contact_to_group(self, contact, group):
        wd = self.app.wd
        self.return_to_home_page()
        self.select_contact_by_id(contact.id)
        self.add_contact_to_selected_group(group)

    def delete_contact_from_group(self, contact, group):
        wd = self.app.wd
        self.return_to_home_page()
        self.set_listgroup_for_contacts(group)
        self.select_contact_by_id(contact.id)
        self.delete_contact_from_selected_group()
        self.return_to_home_page()