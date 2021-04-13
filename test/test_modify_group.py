from model.group import Group

def test_modify_first_group(app):
    if app.group.count() == 0:
        app.group.create(Group(name="hello", header="hmm", footer="mmm"))
    old_groups = app.group.get_group_list()
    app.group.modify_first(Group(name="New name", header="New header", footer="New footer"))
    new_groups = app.group.get_group_list()
    assert len(old_groups) == len(new_groups)

def test_modify_group_name(app):
    if app.group.count() == 0:
        app.group.create(Group(name="hello", header="hmm", footer="mmm"))
    old_groups = app.group.get_group_list()
    group = Group(name="New name 2")
    group.id = old_groups[0].id
    app.group.modify_first_group(group)
    new_groups = app.group.get_group_list()
    assert len(old_groups) == len(new_groups)
    old_groups[0] = group
    assert sorted(old_groups, key=Group.id_or_max) == sorted(new_groups, key=Group.id_or_max)

#def test_modify_group_header(app):
#    if app.group.count() == 0:
#        app.group.create(Group(name="hello", header="hmm", footer="mmm"))
#    old_groups = app.group.get_group_list()
#    app.group.modify_first_group(Group(header="New header 2"))
#    new_groups = app.group.get_group_list()
#    assert len(old_groups) == len(new_groups)