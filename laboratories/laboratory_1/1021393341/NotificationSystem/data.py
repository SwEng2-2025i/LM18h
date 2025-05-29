#DB simulated
_data = []

def loadUserInfo(userInfo):
    _data.append(userInfo)

def getAllUsers():
    return _data

def getUserInfo(name):
    for user in _data:
        if user['name'] == name:
            return user
    return None
