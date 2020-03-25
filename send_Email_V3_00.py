# V3.00 sende eine Email bei Sammelstoerung
import smtplib
def send_mail(Nachricht):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("dieterlutz188@gmail.com", "!234123$")
    
    msg = Nachricht
    server.sendmail("dieterlutz188@gmail.com", "paulkober@gmail.com", msg)
    server.quit()
    print "Email bezueglich Sammelstoerung gesandt!"
    return None