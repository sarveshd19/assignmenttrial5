import main

# def test_student(new_home):
#    assert new_home.name == "BodduBhai

dict_add = {"old_id": 101,
            "class_id": 1,
            "class_leader": "Yes",
            "student_id": 101,
            "student_name": "sarvesh",
            "selected_id": 1,
            "name": "sarvesh"}

dict_new = {
    "class_id": 1,
    "class_leader": "No",
    "student_name": "sarvesh",
}

dict_new_class = {
    "class_name": "BE EXTC A"
}

dict_delete = {"id": 3}


def test_home(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/?name="Ratan"')
    assert resp.status_code == 200


def test_show_class(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/view_class')
    assert resp.status_code == 200


def test_show_update(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/update', data=dict_add)
    assert resp.status_code == 302


def test_new(test_resp_code):
    abc = test_resp_code
    resp = abc.post('new', data=dict_add)
    assert resp.status_code == 302


def test_new_class(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/new_class', data=dict_new_class)
    assert resp.status_code == 302


def test_delete(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/delete', data=dict_delete)
    assert resp.status_code == 302
