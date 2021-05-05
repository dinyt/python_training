from datetime import datetime
from pony.orm import *
from model.group import Group
from model.contact import Contact

# у меня работает прекрасно и без специальных конвертеров, но в видеоуроке это не так
# поэтому я просто повторю это
from pymysql.converters import decoders

class ORMFixture:

    db = Database()

    # описание структуры свойств интересующего класса
    # db.Entity - для связки с внешним классом db
    class ORMGroup(db.Entity):
        # _table_ - указывается название описываемой ниже таблицы
        _table_ = 'group_list'
        # column='group_id' - привязка переменной id к физическому слолбцу в таблице
        id = PrimaryKey(int, column='group_id')
        # Optional - поле может быть пустым
        name = Optional(str, column='group_name')
        header = Optional(str, column='group_header')
        footer = Optional(str, column='group_footer')
        # table='address_in_groups' - таблица в БД для связи,
        # column='id' - колонка в таблице, по которой устанавливается связь
        # reverse='groups' - свойство в связываемом классе для установления связи между ними
        # lazy=True - запрет загрузки рекурсивно-связанной информации из БД при создании объекта данного класса
        contacts = Set(lambda: ORMFixture.ORMContact, table='address_in_groups', column='id', reverse='groups', lazy=True)

    class ORMContact(db.Entity):
        _table_ = 'addressbook'
        id = PrimaryKey(int, column='id')
        # если название столбца совпадает с названием переменной, то его можно не указывать
        # но лучше это делать для наглядности
        firstname = Optional(str, column='firstname')
        lastname = Optional(str, column='lastname')
        # deprecated - нужно для фильтрации записей
        deprecated = Optional(datetime, column='deprecated')
        # table='address_in_groups' - таблица в БД для связи,
        # column='group_id' - колонка в таблице, по которой устанавливается связь
        # reverse='contacts' - свойство в связываемом классе для установления связи между ними
        # lazy=True - запрет загрузки рекурсивно-связанной информации из БД при создании объекта данного класса
        groups = Set(lambda: ORMFixture.ORMGroup, table='address_in_groups', column='group_id', reverse='contacts', lazy=True)

    def __init__(self, host, name, user, password):
        # .bind - привязка к БД
        # conv=decoders - используется для ситуаций, когда назначаются "принудительно" конвертеры
        # от выбранного модуля(в данном случае pymysql.converters), иначе будут работать по умочанию
        # конвертеры от pony
        #self.db.bind('mysql', host=host, user=user, password=password, database=name, conv=decoders)
        # оставлю предыдущий вариант, так как с указанным конвертером получаю ошибку:
        # Value of unexpected type received from database: instead of datetime got <class 'str'>
        self.db.bind('mysql', host=host, user=user, password=password, database=name)
        # generate_mapping - производится маппировка свойств описанных выше классов и
        # указанных в них таблиц
        self.db.generate_mapping()
        # в консоли будут отображаться SQL-запросы
        sql_debug(True)

    def convert_groups_to_model(self, groups):
        def convert(group):
            return Group(id=str(group.id), name=group.name, header=group.header, footer=group.footer)
        return list(map(convert, groups))


    @db_session # чтобы вся функция отработала в сессии, без указания этого будет ошибка:
    # db_session is required when working with the database
    def get_group_list(self):
        return self.convert_groups_to_model(select(g for g in ORMFixture.ORMGroup))

    def convert_contacts_to_model(self, contacts):
        def convert(contact):
            return Contact(id=str(contact.id), fName=contact.firstname, lName=contact.lastname)
        return list(map(convert, contacts))

    @db_session
    def get_contact_list(self):
        # ...if c.deprecated is None - позволяет указать условие в python
        # на подобие предложения where в SQL
        # нулевые даты должны будут автоматически заполниться в None
        return self.convert_contacts_to_model(select(c for c in ORMFixture.ORMContact if c.deprecated is None))

    @db_session
    def get_contacts_in_group(self, group):
        orm_group = list(select(g for g in ORMFixture.ORMGroup if g.id == group.id))[0]
        return self.convert_contacts_to_model(orm_group.contacts)

    @db_session
    def get_contacts_not_in_group(self, group):
        orm_group = list(select(g for g in ORMFixture.ORMGroup if g.id == group.id))[0]
        return self.convert_contacts_to_model(
            select(c for c in ORMFixture.ORMContact if c.deprecated is None and orm_group not in c.groups))