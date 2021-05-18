# -*- coding: utf-8 -*-
from model.group import Group
import pytest
#from data.groups import constant as testdata

#@pytest.mark.parametrize("group", testdata, ids=[repr(x) for x in testdata])
def test_add_group(app, db, json_groups):
    group = json_groups
    # название шага такое же как и в файле bdd/groups.feature
    with pytest.allure.step('Given a group list'):
        old_groups = db.get_group_list()
    with pytest.allure.step('When I add the group %s to the list' % group):
        app.group.create(group)
    with pytest.allure.step('Then the new group list is equal to the old list with the added group'):
       # assert len(old_groups) + 1 == app.group.count()
        new_groups = db.get_group_list()
        old_groups.append(group)
        assert sorted(old_groups, key=Group.id_or_max) == sorted(new_groups, key=Group.id_or_max)