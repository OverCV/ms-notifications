import os
from flask import Flask, request
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from twilio.rest import Client

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, maths!"


# TODO?[00]: Se empiezan a generar los métodos que por defecto son GET.
@app.route("/email", methods=["POST"])
def email():
    try:  # Traer las variables de entorno (ve).
        API_KEY = os.environ.get("SENDGRID_API_KEY")
        EMAIL_SENDER = os.environ.get("SENDGRID_EMAIL_SENDER")
        HASH_VALIDATOR = os.environ.get("SENDGRID_HASH_VALIDATOR")
    except Exception as error:
        return f"|[ Datos incompletos para el envío email {error} ]|"

    # Para que no todo el mundo realice los emails se usa un hash.
    hash = request.form["hash_validator"]
    if hash == HASH_VALIDATOR:
        print(f"Equal")
        # Desde Postman se darán valor a estos "requests".
        email_sender = EMAIL_SENDER
        to = request.form["destination"]
        subject = request.form["subject"]
        message_content = request.form["message"]

        message = Mail(
            # TODO?[01]: Se realiza el envío por vía email.
            from_email=email_sender,
            to_emails=to,
            subject=subject,
            html_content=message_content
        )
        try:
            SG = SendGridAPIClient(API_KEY)
            response = SG.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
            return "OK"
        except Exception as error:
            print("Error message:", error)
            return "KO"
    else:
        print(f"SE | {HASH_VALIDATOR} != {hash}")
        return f"|[ hash_error: {hash} ]|"


# TODO?[02]: Hacemos envío de notificaciones vía mobile.
@app.route("/sms", methods=["POST"])
def sms():
    try:
        TWILIO_SID = os.environ.get("TWILIO_ACCOUNT_SID")
        TWILIO_TOKEN = os.environ.get("TWILIO_AUTHENTICATION_TOKEN")
        HASH_VALIDATOR = os.environ.get("TWILIO_HASH_VALIDATOR")

        NUMBER = os.environ.get("TWILIO_NUMBER")
        TARGET_NUMBER = os.environ.get("TWILIO_TARGET_NUMBER")
    except Exception as error:
        return f"|[ Datos incompletos para el envío movil: {error} ]|"

    hash = request.form["hash_validator"]
    print(f"01", hash)
    """
    Pachón, ahora me encuentro realizando un proyecto de Programación III y estoy aprendiendo a usar API's como Twilio para envío de notificaciones sms o correo electrónico.
    """
    if hash == HASH_VALIDATOR:
        destination = request.form["destination"]
        message = request.form["message"]
        print(f"02", message)
        ## destination = request.form["destination"]

        # Para uso con Twilio.
        try:
            account_sid = TWILIO_SID
            auth_token = TWILIO_TOKEN
            print(f"03", account_sid, auth_token)
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                from_=NUMBER,
                # messaging_service_sid = TWILIO_SID,
                to=destination,
                body=message
            )
            print(f"04", message)
            """ 
                messaging_service_sid=os.environ["messaging_service_sid"],
                body=message,
                to=destination
            """
            print(message.sid)
            return 'OK'
        except:
            return 'KO'
    else:
        print(f"TS | {HASH_VALIDATOR} != {hash}")
        return f"|[ hash_error: {hash} ]|"


""" 
def sms():
    hash = request.form['hash_validator']
    if(hash == "Admin12345@2022Ucaldas"):
        destination = request.form['destination']
        message = request.form['message']
        # Create an SNS client
        client = boto3.client(
            "sns",
            aws_access_key_id=os.environ["aws_access_key_id"],
            aws_secret_access_key=os.environ["aws_secret_access_key"],
            region_name="us-east-1"
        )

        # Send your sms message.
        client.publish(
            PhoneNumber=destination,
            Message=message
        )
        return 'OK'
    else:
        return "hash_error"
 """

if __name__ == "__main__":
    app.run()
