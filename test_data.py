dict_update = {"old_id": "157945990136517569019708845704657370535",
               "class_id": "53655506439711004738311928241632705959",
               "class_leader": "Yes",
               "student_id": 101,
               "student_name": "sarvesh",
               "selected_id": 1,
               "name": "sarvesh"}

dict_new = {
    "class_id": "53655506439711004738311928241632705959",
    "class_leader": "No",
    "name": "sarvesh",
    "selected_id": "53655506439711004738311928241632705959"}

dict_new_class = {
    "class_name": "BE EXTC A"
}

dict_delete = {"id": "170320365245479417011359743000895159719"}


def test_home(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/?name="sarvesh"')
    assert resp.status_code == 200


def test_show_class(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/view_class')
    assert resp.status_code == 200


def test_new(test_resp_code):
    abc = test_resp_code
    resp = abc.post('new', data=dict_new)
    assert resp.status_code == 302


def test_update(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/update_record', data=dict_update)
    assert resp.status_code == 200


def test_show_update(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/update', data=dict_update)
    assert resp.status_code == 302


def test_new_class(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/new_class', data=dict_new_class)
    assert resp.status_code == 302


def test_delete(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/delete', data=dict_delete)
    assert resp.status_code == 302
