import re


def login(login):
    pattern = r'^[a-zA-Z][0-9a-zA-Z_]{4,18}[0-9a-zA-Z]$'
    if re.match(pattern, login):
        return True
    else:
        return False


def data(text):
    pattern = [
            r'\d{1,2}.\d{1,2}.\d{2,4}',
            r'\d{1,2}-\d{1,2}-\d{2,4}',
            r'\d{1,2}/\d{1,2}/\d{2,4}'
               ]
    for patt in pattern:
        return re.findall(patt, text)


def log(text):
    pattern = {
            'date': r'(\d{4}-\d{2}-\d{2})',
            'time': r'(\d{2}:\d{2}:\d{2})',
            'user': r'user=([a-z]+)',
            'action': r'action=([a-z]+)',
            'ip': r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    }
    data = {}
    for key, patt in pattern.items():
        data[key] = re.search(patt, text).group(1)
    return data
# print(log('2024-02-10 14:23:01 INFO user=ada action=login ip=192.168.1.15'))


def passw(passw):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*]).{8,}$'
    if re.match(pattern, passw):
        return True
    else:
        return False

# print(passw('dssdddddd2A%'))


def mail(mail):
    domains = [r'gmail\.com$', r'yandex\.ru$', r'edu\.ru$'] 
    # pattern = r'^[a-z][a-zA-Z0-9_]*@' + 
    for dom in domains:
        pattern = r'^[a-zA-Z][a-zA-Z0-9_]*\@' + dom
        if re.match(pattern, mail):
            return True
    return False

# print(mail('koshelot_2006@edu.ru'))


def number(number):
    pattern = r'\-|\s|[()]'
    return re.sub(pattern, '', number)

# print(number('+7 (952) 60--30 2-1(0)'))
