from model.group import Group
import random

def test_modify_group_name(app, db, check_ui):
    if db.get_group_list() == 0:
        app.group.create(Group(name="hello", header="hmm", footer="mmm"))
    old_groups = db.get_group_list()
    group = random.choice(old_groups)
    app.group.modify_by_id(group.id, group)
    assert len(old_groups) == app.group.count()
    new_groups = db.get_group_list()
    index = 0
    for gr in old_groups:
        if gr.id == group.id:
            break
        index = index + 1
    old_groups[index] = group
    assert sorted(old_groups, key=Group.id_or_max) == sorted(new_groups, key=Group.id_or_max)
    if check_ui:
        assert sorted(new_groups, key=Group.id_or_max) == sorted(app.group.get_group_list(), key=Group.id_or_max)