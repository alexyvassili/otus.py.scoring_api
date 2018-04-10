# -*- coding: utf-8 -*-
from datetime import datetime
import logging

UNKNOWN = 0
MALE = 1
FEMALE = 2
GENDERS = {
    UNKNOWN: "unknown",
    MALE: "male",
    FEMALE: "female",
}


class Field(type):
    def __new__(cls, required=False, nullable=True, **kwargs):

        def validate(value):
            raise NotImplementedError

        attrs = {}
        newclass = type.__new__(cls, cls.__name__, (Field,), attrs)
        setattr(newclass, 'validate', validate)
        setattr(newclass, 'required', required)
        setattr(newclass, 'nullable', nullable)
        for name, value in cls.__dict__.items():
            if not name.startswith('__'):
                if callable(value):
                    setattr(newclass, value.__name__, value)
        return newclass

    def __init__(self, *args, **kwargs):
        pass

    def __get__(self, obj, objtype=None):
        logging.info(f'get value {self.value}')
        return self.value

    def __set__(self, obj, value):
        if value is None and (self.required or not self.nullable):
            raise AttributeError('Value is required', value)
        elif value is None and self.nullable:
            self.value = value
        elif self.validate(self, value):
            self.value = value
        else:
            raise ValueError('Validating error:', value)


class FieldObj:
    def __init__(self, required=False, nullable=True):
        self.required = required
        self.nullable = nullable

    def __get__(self, obj, objtype=None):
        logging.info(f'get value {self.value}')
        return self.value

    def __set__(self, obj, value):
        if value is None and (self.required or not self.nullable):
            raise AttributeError('Value is required', value)
        elif value is None and self.nullable:
            self.value = value
        elif self.validate(self, value):
            self.value = value
        else:
            raise ValueError('Validating error:', value)

    def validate(self, value):
        raise NotImplementedError


class CharField(Field):

    def validate(self, value):
        logging.info('validating chars')
        return type(value) == str


class ListField(Field):

    def validate(self, value):
        logging.info('validating list')
        return type(value) == list


class DictField(Field):

    def validate(self, value):
        logging.info('validating list')
        return type(value) == dict


class EmailField(CharField):

    def validate(self, value):
        logging.info('validating mail')
        return super().validate(value) and '@' in value


class PhoneField(Field):

    def validate(self, value):
        logging.info('validating phone')
        value = str(value)
        return len(value) == 11 and value[0] == '7'


class DateField(CharField):

    def validate(self, value):
        logging.info('validating date')
        if not super().validate(value):
            return False
        try:
            datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            return False
        return True


class BirthDayField(DateField):

    def validate(self, value):
        logging.info('validating bthday')
        if not super().validate(value):
            return False
        value = datetime.strptime(value, "%d.%m.%Y").date()
        today = datetime.now().date()
        return (today - value).days // 365 < 70


class GenderField(Field):

    def validate(self, value):
        logging.info('validating gender')
        return value in (UNKNOWN, MALE, FEMALE)


class ClientIDsField(ListField):

    def validate(self, value):
        logging.info('validating client ids')
        return super().validate(value) and all(map(lambda x: type(x) is int, value))


class ArgumentsField(DictField):

    def validate(self, value):
        return super().validate(value)
