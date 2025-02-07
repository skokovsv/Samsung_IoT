from flask_login import UserMixin


class UserLogin(UserMixin):

    def fromDB(self,user_id,db):
        self.__user = db.getUser(user_id)
        return self

    def create(self,user):
        self.__user = user
        return self


    def get_id(self):
        return str(self.__user['id'])


def verifyExt(filename):
    ext = filename.rsplit('.', 1)[-1]
    if ext == 'jpg' or ext == 'JPG':
        return True
    return False