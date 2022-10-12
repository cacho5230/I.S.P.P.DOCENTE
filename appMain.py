from flask import Flask, render_template, url_for, redirect, request, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_wtf import CSRFProtect

from database.connDb import config
from models.entity.EntityUser import User
from models.ModelUser import modeloUsuario
from functionalitys.configEmail import emailClass

app = Flask(__name__)
csrf = CSRFProtect()
mysql = MySQL(app)
login_manager_app = LoginManager(app)


@login_manager_app.user_loader
def load_user(id):
    return modeloUsuario.GetIdFunction(mysql, id)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        if not current_user.is_authenticated:
            return render_template('login.html')
        else:
            idusuario = current_user.id
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM usuario_personal WHERE id_user = %s', [str(idusuario)])
            tupl = cur.fetchone()
            print(tupl)
            return render_template('home.html', lista = tupl)
    else:
        idUser = request.form['usuario']
        pwUser = request.form['contraseña']
        user = User(idUser, pwUser)
        user = modeloUsuario.loginFunction(mysql, user)
        print("checkpoint 1 login")
        if user == None:
            flash('USUARIO O CONTRASEÑA INCORRECTA')
            return redirect(url_for('index'))
        if user.pw or user.pwtemp:
            print('login usuario')
            if user.pwtemp:
                #LOGIN CON PW TEMP
                print('redireccionando a cambiar la pw')
                flash('ACTRUALIZA ESTOS DATOS ANTES DE CONTINUAR')
                login_user(user)
                return render_template('first_login.html')
            #LOGIN PW NORMAL
            print('Login con pw normal')
            login_user(user)
            flash('SESION INICIADA')
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM usuario_personal WHERE id_user = %s', [str(current_user.id)])
            tupl = cur.fetchone()
            print(tupl)
            return render_template('home.html', lista = tupl)
        else:
            flash('USUARIO O CONTRASEÑA INCORRECTA')
            return redirect(url_for('index'))

@app.route('/first_login', methods=['POST'])
def FirstLogin():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuario_datos WHERE id_user = %s', [str(current_user.id)])
        consulta = cur.fetchone()
        if consulta == None:
            cur.execute("INSERT INTO usuario_datos(id_user) VALUES (%s)",[str(current_user.id)])
            creado = cur.fetchone()
            mysql.connection.commit()
            print("DATOS PERSONALES CREADOS")
            print(creado)
        correo = request.form['correo']
        newpw = request.form['newpw']
        modeloUsuario.PrimerLoginFunction(mysql,current_user.id,newpw,correo)
    return redirect(url_for('index'))

@app.route('/ver/', methods=['GET','POST'])
def GetDatos():
    idUser = current_user.id
    if request.method == 'GET':
        print(idUser)
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuario_personal p INNER JOIN usuario_datos d on p.id_user = d.id_user WHERE p.id_user = %s', [str(idUser)])
        data = cur.fetchone()
        print(data)
        return render_template('datos.html', info = data)
    else:
        request.method == 'POST'
        tel = request.form['tel']
        ciudad = request.form['ciudad']
        pais = request.form['pais']
        observacion = request.form['observaciones']
        cuil = request.form['cuil']
        nacionalidad = request.form['nacionalidad']
        fecha_nacim = request.form['fecha_nacim']
        sexo = request.form['sexo']
        titulo = request.form['titulo']
        calle = request.form['calle']
        numero = request.form['numero']
        piso = request.form['piso']
        departamento = request.form['departamento']
        manzana = request.form['manzana']
        barrio = request.form['barrio']
        cp = request.form['cp']
        provincia = request.form['provincia']
        cur = mysql.connection.cursor()
        cur.execute("""UPDATE usuario_datos 
            SET tel_user = %s, ciudad = %s, pais = %s, observacion = %s, CUIL=%s, Nacionalidad=%s, fecha_nacim=%s, sexo=%s, titulo=%s, calle=%s, numero=%s, piso=%s, dpto=%s, mza=%s, barrio=%s, cp=%s, provincia=%s WHERE id_user = %s""", (tel,ciudad,pais,observacion,cuil,nacionalidad,fecha_nacim,sexo,titulo,calle,numero,piso,departamento,manzana,barrio,cp,provincia,idUser))
        flash('DATOS ACTUALIZADOS CORRECTAMENTE')
        mysql.connection.commit()
        return redirect(url_for('GetDatos'))

        
@app.route('/cerrarSesion')
@login_required
def cerrarSesion():
    logout_user()
    flash('GRACIAS POR USAR EL SISTEMA')
    return redirect(url_for('index'))


@app.route('/RecuperarContraseña', methods=['GET', 'POST'])
def recuperarContraseña():
    if request.method == 'POST':
        if request.form['recuperar'] == 'enviar':
            receptor = request.form['Email']
            asunto = 'Recuperar Contraseña'
            p = emailClass.pwTempFunction()
            cuerpo = '''

Se solicito un cambio de contraseña

Su contraseña temporal es: '''+p+'''

La contraseña es de un solo uso, al ingresar le pedira que la cambie'''
            user = User(email=receptor, contraseñatemp=p)
            if modeloUsuario.checkEmailFunction(mysql, user):
                Email = emailClass(receptor, asunto, cuerpo)
                emailClass.enviarCorreo(Email)
                flash('Email Enviado')
            else:
                flash('Email no encontrado')
            return render_template('recuperar_pw.html')

        else:
            id = request.form['id']
            contraseña = request.form['contraseña']
            contraseñaconf = request.form['contraseñaconfirmar']
            if contraseña == contraseñaconf:
                modeloUsuario.CambiarPwFunction(mysql, id, contraseña)
                flash('Contraseña Cambiada')
                return redirect(url_for('index'))
            else:
                flash('Las contraseñas no coinciden')

            return render_template('cambiar_pw.html', id=id)
    return render_template('recuperar_pw.html')

    
# tratamiento de errores

def status_401(error):
    flash('Debes iniciar session para acceder')
    return redirect(url_for('index'))


def status_404(error):
    return "<h1>Página no encontrada !!!!</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['desarrollo'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()