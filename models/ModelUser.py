from models.entity.EntityUser import User

class modeloUsuario():
    
    @classmethod
    def loginFunction(self, mysql, user):
        try:
            cur = mysql.connection.cursor()
            sql = 'SELECT * FROM usuario_personal WHERE dni_user = %s '
            cur.execute(sql,([user.dni]))
            row = cur.fetchone()
            print(row) #impresion de tupla user
            if row != None:
                pwUser = row[2]
                pwTemp = row[3]
                print('hasheo pw normal')
                pwNormalHash = (User.GenerateHashFunction(pwTemp))
                print('hasheo pw temp')
                pwTempHash = (User.GenerateHashFunction(pwTemp))
                print(pwNormalHash +'\n' +pwTempHash)
                User.CheckPwFunction(pwNormalHash, pwUser)
                if pwTemp != None:
                    User.CheckPwFunction(pwTempHash, pwTemp)
                else:
                    pwTemp=False
                user = User(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
                print(user) #objeto usuario
                return user
            else:
                print('invalido')
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def checkEmailFunction(self, mysql, user):
        try:
            cur = mysql.connection.cursor()
            cur.execute('SELECT email_user, id_user FROM usuario_personal WHERE email = \'{}\''.format(str(user.email)))
            row=cur.fetchone()
            correo=str(row[0])
            id=int(row[1])
            if user.email == correo:
                cur.execute('UPDATE usuario_personal SET pw_temp = %s WHERE id_user = %s',(str(User.GenerateHashFunction(user.pwTemp)), id))
                mysql.connection.commit()
                return True
            else:
                return False
        except Exception as ex:
            raise Exception(ex)
    

    @classmethod
    def GetIdFunction(self, mysql, idUser):
        try:
            cur = mysql.connection.cursor()
            sql = 'SELECT id_user, ape_user, nom_user, email_user, status_user FROM usuario_personal WHERE id_user = %s'
            cur.execute(sql,([int(idUser)]))
            row = cur.fetchone()
            if row != None:
                return User(row[0],row[1], row[2], row[3], row[4])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def BorrarPwTempFunction(self, mysql, id):
        try:
            cur = mysql.connection.cursor()
            sql = 'UPDATE usuario_personal SET pw_temp = NULL WHERE id_user = %s'
            cur.execute(sql,([int(id)]))
            mysql.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def CambiarPwFunction(self,mysql,id,pw):
        try:
            cur = mysql.connection.cursor()
            sql = 'UPDATE usuario_personal SET pw_user = %s WHERE id_user = %s'
            cur.execute(sql,([User.GenerateHashFunction(pw)],[int(id)]))
            mysql.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def PrimerLoginFunction(self,mysql,id,pw,email):
        try:
            cur = mysql.connection.cursor()
            sql = 'UPDATE usuario_personal SET pw_temp = NULL, pw_user = %s, email_user = %s WHERE id_user = %s'
            cur.execute(sql,([User.GenerateHashFunction(pw)],[str(email)],[int(id)]))
            mysql.connection.commit()
        except Exception as ex:
            raise Exception(ex)