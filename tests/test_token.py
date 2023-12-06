import copy
from tests.http_service import request_func

username = 'aasgsfgsSDFG'
password = 'asghGG3445'
email = 'sgfs@sfhfs.ru'

def check_keys(keys_needed, keys_from_request):
    for key in keys_needed:
        if key not in keys_from_request:
            raise ValueError


active_token1 = ''
deactivate_token = ''
active_token = ''


# регистрируемся, получаем токен
def test_register():
    response = request_func(username=username, password=password, email=email,
                            endpoint="register", method="POST")
    assert response.status_code == 200
    data = response.json()
    check_keys(['access_token'], data.keys())
    global active_token1
    active_token1 = data.get("access_token")
    assert type(active_token) == str


# деактивируем токен
def test_logout():
    response = request_func(method="POST", token=active_token1, endpoint='logout')
    assert response.status_code == 204
    global deactivate_token
    deactivate_token = copy.deepcopy(active_token1)


# логинимся, получаем токен
def test_login():
    response = request_func(password=password, username=username,
                            method="POST", endpoint='login')
    data = response.json()
    check_keys(['access_token'], data.keys())
    global active_token
    active_token = data.get("access_token")
    assert type(active_token) == str
    assert response.status_code == 200


# Пробуем получить инфо о пользователе без токена и неверным токеном
def test_get_info():
    # отсутствие заголовка авторизации
    response = request_func(method="GET")
    assert response.status_code == 403

    # неправильный токен
    response = request_func(method="GET", token="sgkhuskgjghoigjs24345")
    assert response.status_code == 401

    # валидный токен
    response = request_func(method="GET", token=active_token)
    assert response.status_code == 200
    data = response.json()
    check_keys(['data'], data.keys())
    check_keys(['username', 'email', 'registration_date'], data['data'].keys())

    # деактивированный токен
    response = request_func(method="GET", token=deactivate_token)
    assert response.status_code == 401


def test_update():
    # отсутствие заголовка авторизации
    response = request_func(password=password, email=email, method="PUT")
    assert response.status_code == 403
    
    # неправильный токен
    response = request_func(password=password, email=email, method="PUT",
                            token="sgkhuskgjghoigjs24345")
    assert response.status_code == 401
    
    # валидный токен, данные пользователя не изменились
    response = request_func(password=password, email=email,
                            method="PUT", token=active_token)
    assert response.status_code == 200
    
    # валидный токен, меняем только email
    new_email = email + 'u'
    response = request_func(password=password, email=new_email,
                            method="PUT", token=active_token)
    assert response.status_code == 200
    
    # валидный токен, меняем только пароль
    new_password = password + 'U'
    response = request_func(password=new_password, email=new_email,
                            method="PUT", token=active_token)
    assert response.status_code == 200
    
    # валидный токен, меняем все вместе
    response = request_func(password=password, email=email,
                            method="PUT", token=active_token)
    assert response.status_code == 200
    

    # деактивированный токен
    response = request_func(password=password, email=email,
                            method="PUT", token=deactivate_token)
    assert response.status_code == 401


def test_delete():
    # без токена
    response = request_func(method="DELETE")
    assert response.status_code == 403

    # c неверным токеном
    response = request_func(method="DELETE", token="sfdgsgsg")
    assert response.status_code == 401

    # с деактивированным токеном

    response = request_func(method="DELETE", token=deactivate_token)
    assert response.status_code == 401

    # с валидным токеном
    response = request_func(method="DELETE", token=active_token)
    assert response.status_code == 204
