from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, idUser=None, dniUser=None, pwUser=None, pwTemp=None, apeUser=None, nomUser=None, emailUser='', statusUser=None):
        self.id = idUser
        self.dni = dniUser
        self.pw = pwUser
        self.pwtemp = pwTemp
        self.ape = apeUser
        self.nom = nomUser
        self.email = emailUser
        self.status = statusUser

    @classmethod
    def CheckPwFunction(self, hash, password):
        return check_password_hash(hash, password)

    @classmethod
    def GenerateHashFunction(self, contraseña):
        return generate_password_hash(contraseña)


