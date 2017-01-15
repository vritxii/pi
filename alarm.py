from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import os, time
import libbeep


def beep():
    print('beep')
    libbeep.beepAction(0.05, 0.05, 200)


def cut_pic():
    for i in range(1, 4):
        os.system('fswebcam --no-banner -r 560x480 %d.jpg'%(i))
    os.system('zip -r all.zip *.jpg')


def send_email():
    cut_pic()
    file_name = 'all.zip'
    msg = MIMEMultipart()
    msg['From'] = 'desirev@suster.ticp.net'
    msg['To'] = 'nkdzt@foxmail.com'
    msg['Subject'] = 'subject'
    msg.attach(MIMEText('text'))
    part = MIMEBase('application', 'tar')
    part.set_payload(open(file_name, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment;filename=all.zip')
    msg.attach(part)
    server = smtplib.SMTP()
    server.connect('smtp.ym.163.com')
    server.login(msg['From'], 'sustc1510')
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
    try:
        os.system('rm -f *.jpg')
        os.system('rm -f %s' % file_name)
    except:
        print('No such file')


if __name__ == '__main__':
    cut_pic()
    send_email()
    beep()
