from _datetime import datetime
import hashlib
import functools
from fields import *
from scoring import get_score, get_interests
from constants import *

# Задание пытался реализовывать самостоятельно, не заглядывая в код Django
# Плюсы этого скрипта - он работает
# Минусы - не уверен что правильно разобрался с наследованием - (код ApiRequest.__new__ и
# fields.py -> Field.__new__
# - функция validate кажется как-то не так подхватывается, потому что приходится
# писать self.validate(self, value) вместо self.validate(value)
# зачем нужен словарь контекста я тоже не очень понял.


class ApiRequest:
    def __new__(cls, **kwargs):
        obj = super(ApiRequest, cls).__new__(cls)
        api_fields = []
        for field in cls.__dict__:
            if not field.startswith('__'):
                if hasattr(cls.__dict__[field], '__base__') and cls.__dict__[field].__base__ is Field:
                    api_fields.append(field)
                    obj.__dict__[field] = cls.__dict__[field]()
                else:
                    obj.__dict__[field] = cls.__dict__[field]
        obj.__dict__['api_fields'] = api_fields
        return obj

    def __init__(self, **kwargs):
        bad_fields = []
        required_field_errs = []
        self.has = []
        for field, cls in self.__dict__.items():
            if field in self.api_fields:
                if field in kwargs:
                    value = kwargs[field]
                    self.has.append(field)
                else:
                    value = None
                try:
                    logging.info(f'SET {field} TO {value}')
                    setattr(self, field, value)
                except ValueError:
                    logging.info(f'FAILED TO SET {field} TO {value}')
                    bad_fields.append(field)
                except AttributeError:
                    required_field_errs.append(field)
        if required_field_errs:
            raise AttributeError(f'This fields is required: {required_field_errs}')
        if bad_fields:
            raise TypeError(f'Bad fields: {bad_fields}')


class ClientsInterestsRequest(ApiRequest):
    client_ids = ClientIDsField(required=True)
    date = DateField(required=False, nullable=True)


class OnlineScoreRequest(ApiRequest):
    first_name = CharField(required=False, nullable=True)
    last_name = CharField(required=False, nullable=True)
    email = EmailField(required=False, nullable=True)
    phone = PhoneField(required=False, nullable=True)
    birthday = BirthDayField(required=False, nullable=True)
    gender = GenderField(required=False, nullable=True)


class MethodRequest(ApiRequest):
    account = CharField(required=False, nullable=True)
    login = CharField(required=True, nullable=True)
    token = CharField(required=True, nullable=True)
    arguments = ArgumentsField(required=True, nullable=True)
    method = CharField(required=True, nullable=False)

    @property
    def is_admin(self):
        return self.login == ADMIN_LOGIN


def check_auth(request: MethodRequest):
    if request.login == ADMIN_LOGIN:
        digest = hashlib.sha512((datetime.now().strftime("%Y%m%d%H") + ADMIN_SALT).encode('utf-8')).hexdigest()
    else:
        digest = hashlib.sha512((request.account + request.login + SALT).encode('utf-8')).hexdigest()
    logging.info(f'DIGEST: {digest}')
    if digest == request.token:
        return True
    return False


def login_required(method_handler: callable):
    @functools.wraps(method_handler)
    def wrapper(request: MethodRequest, ctx, store):
        if check_auth(request):
            res = method_handler(request, ctx, store)
        else:
            res = (FORBIDDEN, ERRORS[FORBIDDEN])
        return res
    return wrapper


def method_handler(request, ctx, store):
    methods = {
        'online_score': online_score_handler,
        'clients_interests': clients_interests_handler,
    }
    try:
        req_obj = MethodRequest(**request["body"])
        code, response = methods[req_obj.method](req_obj, ctx, store)
    except AttributeError as e:
        return INVALID_REQUEST, e.args[0]
    except TypeError as e:
        return INVALID_REQUEST, e.args[0]
    else:
        return code, response


@login_required
def online_score_handler(request: MethodRequest, ctx, store):
    api_request = OnlineScoreRequest(**request.arguments)
    logging.info(f'HAS: {api_request.has}')
    ctx['has'] = api_request.has
    score = get_score(store,
                     phone=api_request.phone,
                     email=api_request.email,
                     birthday=api_request.birthday,
                     gender=api_request.gender,
                     first_name=api_request.first_name,
                     last_name=api_request.last_name)
    return OK, {"score": score}


@login_required
def clients_interests_handler(request: MethodRequest, ctx, store):
    api_request = ClientsInterestsRequest(**request.arguments)
    logging.info(f'HAS: {api_request.has}')
    ctx['has'] = api_request.has
    return OK, {cid: get_interests(store, cid) for cid in api_request.client_ids}
