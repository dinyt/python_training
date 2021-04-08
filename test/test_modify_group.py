from model.group import Group

def test_modify_first_group(app):
    if app.group.count() == 0:
        app.group.create(Group(name="hello", header="hmm", footer="mmm"))
    app.group.modify_first(Group(name="New name", header="New header", footer="New footer"))

def test_modify_group_name(app):
    if app.group.count() == 0:
        app.group.create(Group(name="hello", header="hmm", footer="mmm"))
    app.group.modify_first_group(Group(name="New name 2"))

def test_modify_group_header(app):
    if app.group.count() == 0:
        app.group.create(Group(name="hello", header="hmm", footer="mmm"))
    app.group.modify_first_group(Group(header="New header 2"))