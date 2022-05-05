import re

emailRegex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
passRegex = re.compile(r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[*.!@$%^&(){}[]:;<>,.?/~_+-=|\]).{6,32}$')
nameRegex = re.compile(r'^[A-Za-z][A-Za-z0-9_]{3,19}$')

def emailValidator(email: str):
    if re.fullmatch(emailRegex, email):
      return True
    else:
      return False

def passValidator(password: str):
    if re.fullmatch(passRegex, password):
        return True
    else:
        return False

def nameValidator(name: str):
    if re.fullmatch(nameRegex, name):
        return True
    else:
        return False