import pytest
import fields


def test_CharField_validate_incorrect_value():
    with pytest.raises(ValueError):
        fields.CharField.validate(None, 5)
    with pytest.raises(ValueError):
        fields.CharField.validate(None, dict())
    with pytest.raises(ValueError):
        fields.CharField.validate(None, list())
    with pytest.raises(ValueError):
        fields.CharField.validate(None, True)


def test_CharField_validate_correct_value():
    assert fields.CharField.validate(fields.CharField(), '5') is None


def test_ListField_validate_incorrect_value():
    pass


def test_ListField_validate_correct_value():
    assert fields.ListField.validate(fields.ListField(), [1, 2, 3]) is None


def test_DictField_validate_incorrect_value():
    pass


def test_DictField_validate_correct_value():
    assert fields.DictField.validate(fields.DictField(), {'name': 'Alexy', 'surname': 'Vassili'}) is None


def test_EmailField_validate_incorrect_value():
    pass


def test_EmailField_validate_correct_value():
    assert fields.EmailField.validate(fields.EmailField(), 'petros@gmail.com') is None


def test_PhoneField_validate_incorrect_value():
    pass


def test_PhoneField_validate_correct_value():
    assert fields.PhoneField.validate(fields.PhoneField(), '79637222999') is None


def test_DateField_validate_incorrect_value():
    pass


def test_DateField_validate_correct_value():
    assert fields.DateField.validate(fields.DateField(), '08.05.2003') is None
    assert fields.DateField.validate(fields.DateField(), '08.05.1920') is None


def test_BirthDayField_validate_incorrect_value():
    pass


def test_BirthDayField_validate_correct_value():
    assert fields.BirthDayField.validate(fields.BirthDayField(), '09.05.1997') is None


def test_GenderField_validate_incorrect_value():
    pass


def test_GenderField_validate_correct_value():
    assert fields.GenderField.validate(fields.GenderField(), fields.UNKNOWN) is None
    assert fields.GenderField.validate(fields.GenderField(), fields.MALE) is None
    assert fields.GenderField.validate(fields.GenderField(), fields.FEMALE) is None


def test_ClientIDsField_validate_incorrect_value():
    pass


def test_ClientIDsField_validate_correct_value():
    assert fields.ClientIDsField.validate(fields.ClientIDsField(), [1, 2, 3, 4, 5]) is None


def test_ArgumentsField_validate_incorrect_value():
    pass


def test_ArgumentsField_validate_correct_value():
    assert fields.ArgumentsField.validate(fields.ArgumentsField(), {"phone": "79175002040",
                                                 "email": "stuv@otus.ru",
                                                 "first_name": "Сергей",
                                                 "last_name": "Костюков",
                                                 "birthday": "01.01.1990",
                                                 "gender": 1}
                                          ) is None
