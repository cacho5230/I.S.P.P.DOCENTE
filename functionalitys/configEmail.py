from email.message import EmailMessage
import ssl
import smtplib
from random import choice


class emailClass:
    def __init__(self, emailreceptor,asunto, cuerpo) -> None:
        self.emailemisor = 'cuentadeprogramador0@gmail.com'
        self.emailcontraseña = 'itse2022'
        self.emailreceptor = emailreceptor
        self.asunto = asunto
        self.cuerpo = cuerpo

    @classmethod
    def enviarCorreo(self, email):
        em = EmailMessage()
        em['From'] = emailClass.emailemisor
        em['To'] = emailClass.emailreceptor
        em['Subject'] = emailClass.asunto
        em.set_content(emailClass.cuerpo)

        contexto = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=contexto) as smtp:
            smtp.login(email.emailemisor, email.emailcontraseña)
            smtp.sendmail(email.emailemisor,
                          email.emailreceptor, 
                          em.as_string())
        return True

    @classmethod
    def pwTempFunction(self):
        longitud = 10
        valores = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ=@#%&+"
        p=''
        p = p.join([choice(valores) for i in range(longitud)])
        return p