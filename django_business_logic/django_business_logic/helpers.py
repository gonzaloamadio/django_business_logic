# -*- coding: utf-8 -*-
import string
import random
from datetime import datetime, timedelta, date
from random import choice, randint
import logging
import hashlib


def to_epoch(date, miliseconds=True):
    """
        The Unix epoch (or Unix time or POSIX time or Unix timestamp) is the number of seconds that have elapsed since January 1, 1970
    """
    seconds = int((date - datetime(1970,1,1)).total_seconds())
    if miliseconds:
        ret = seconds * 1000
    else:
        ret = seconds
    return ret

def this_year():
      return int(datetime.now().year)

def weekday_to_str(num):
    data = {
        '0' : 'mon',
        '1' : 'tue',
        '2' : 'wed',
        '3' : 'thu',
        '4' : 'fri',
        '5' : 'sat',
        '6' : 'sun'
    }

    return data.get(str(num))

def gen_secret_key(numero):
    return ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(numero))

def gen_random_num_of_length(n):
    """
        Genera un numero aleatorio de n cifras
    """
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def is_password_ok(password):
    """
    Verificamos que el password tenga el formato correcto
    Actualmente si es ASCII, de 6 o más caracteres, está bien. No hay más restricciones
    Restricciones de longitúd podrían ir acá.
    """
    try:
      #  password.decode('ascii')
        ret = len(password) >= 6
    except UnicodeEncodeError:
        ret = False
    return ret


# ####################
# FORMAT DICTIONARIES

# Tenemos la data asi,
# "data": [
# {
   # "cost_price": 10,
   # "id": 1,
   # "valid": true
   # .....
# }
# ],

# y queremos ponerla
# "data": {
# "1" : {
   # "cost_price": 10,
   # "id": 1,
   # "valid": true
   # .....
# }
# },

def list_to_dict(lista):
    """
        Pasamos una lista de objetos, y convertimos a diccionario donde la key
        es el id, y el valor todo el objeto.
    """
    ret = {}
    try:
        for obj in lista:
            clave = obj.get('id')
            if clave:
                ret[clave] = obj
        return ret
    except Exception as e:
#        return ret
        raise Exception("Error procesando los datos hacia un diccionario")





