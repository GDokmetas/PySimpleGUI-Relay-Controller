import PySimpleGUI as sg 
import serial
import sys
import glob

ser = None  #Global tanımlanmalı

def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(32)] # Hız için 256'dan 32'e düşürüldü.
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    #print(ports)
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def serial_baglan():
    com_deger = value[0]
    baud_deger = value[1]
    print("Baud Deger", value[1])
    global ser
    ser = serial.Serial(com_deger, baud_deger, timeout=0, parity=serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE , bytesize = serial.EIGHTBITS, rtscts=0)
    window["-BAGLANDI_TEXT-"].update('Bağlandı...')

def role1_ac():
    ser.write('1'.encode('Ascii'))
    window["-ROLE1AC-"].update(disabled=True)
    window["-ROLE1KAPA-"].update(disabled=False)
def role1_kapa():
    ser.write('2'.encode('Ascii'))
    window["-ROLE1AC-"].update(disabled=False)
    window["-ROLE1KAPA-"].update(disabled=True)
def role2_ac():
    ser.write('3'.encode('Ascii'))
    window["-ROLE2AC-"].update(disabled=True)
    window["-ROLE2KAPA-"].update(disabled=False)
def role2_kapa():
    ser.write('4'.encode('Ascii'))
    window["-ROLE2AC-"].update(disabled=False)
    window["-ROLE2KAPA-"].update(disabled=True)
def role3_ac():
    ser.write('5'.encode('Ascii'))
    window["-ROLE3AC-"].update(disabled=True)
    window["-ROLE3KAPA-"].update(disabled=False)
def role3_kapa():
    ser.write('6'.encode('Ascii'))
    window["-ROLE3AC-"].update(disabled=False)
    window["-ROLE3KAPA-"].update(disabled=True)
def role4_ac():
    ser.write('7'.encode('Ascii'))
    window["-ROLE4AC-"].update(disabled=True)
    window["-ROLE4KAPA-"].update(disabled=False)
def role4_kapa():
    ser.write('8'.encode('Ascii'))
    window["-ROLE4AC-"].update(disabled=False)
    window["-ROLE4KAPA-"].update(disabled=True)
def ayarlar():
    layout = [[sg.Text(text="Ayarlar")], 
    [sg.Text(text="Röle 1 Adı:"), sg.Input(default_text=window["-ROLE1AC-"].get_text()[:-3], key="role1ad")],
    [sg.Text(text="Röle 2 Adı:"), sg.Input(default_text=window["-ROLE2AC-"].get_text()[:-3], key="role2ad")],
    [sg.Text(text="Röle 3 Adı:"), sg.Input(default_text=window["-ROLE3AC-"].get_text()[:-3], key="role3ad")],
    [sg.Text(text="Röle 4 Adı:"), sg.Input(default_text=window["-ROLE4AC-"].get_text()[:-3], key="role4ad")],
    [sg.Button(button_text="Kaydet", key="kaydet")]
    ]
    window2 = sg.Window("Ayarlar", layout, modal=True)
    while True: 
        event, values = window2.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break 
        if event == "kaydet":
            print(values)
            window["-ROLE1AC-"].update(values["role1ad"]+" AÇ")
            window["-ROLE1KAPA-"].update(values["role1ad"]+" KAPA")
            window["-ROLE2AC-"].update(values["role2ad"]+" AÇ")
            window["-ROLE2KAPA-"].update(values["role2ad"]+" KAPA")
            window["-ROLE3AC-"].update(values["role3ad"]+" AÇ")
            window["-ROLE3KAPA-"].update(values["role3ad"]+" KAPA")
            window["-ROLE4AC-"].update(values["role4ad"]+" AÇ")
            window["-ROLE4KAPA-"].update(values["role4ad"]+" KAPA")
            window2.close()


def zamanlama():
    layout = [[sg.Text(text="Zamanlama Yapılacak Röleyi Seçiniz", size=(30,1))],
              [sg.Combo([window["-ROLE1AC-"].get_text()[:-3], window["-ROLE2AC-"].get_text()[:-3], window["-ROLE3AC-"].get_text()[:-3], window["-ROLE4AC-"].get_text()[:-3]], size=(30,1), key="rolesecim")],
              [sg.Text(text="Dakika:"), sg.Input(default_text="0", size=(20,1), key="dakika")],
              [sg.Text(text="Saniye:"), sg.Input(default_text="0", size=(20,1), key="saniye")],
              [sg.Button(button_text="BAŞLAT", key="zamanlama_baslat")] 
    ]
    window3 = sg.Window("Zamanlama", layout, modal=True)
    sayac = 0
    sure = 0
    while True: 
        event, values = window3.read(timeout=100)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break 
        if event == "zamanlama_baslat":
            sure = ((int(values['dakika']) * 60) + int(values['saniye'])) * 1000 + sayac
            print("Sure:", sure)
            if (values['rolesecim'] == window["-ROLE1AC-"].get_text()[:-3]):
                role1_ac()
            elif(values['rolesecim'] == window["-ROLE2AC-"].get_text()[:-3]):
                role2_ac()
            elif(values['rolesecim'] == window["-ROLE3AC-"].get_text()[:-3]):
                role3_ac()
            elif(values['rolesecim'] == window["-ROLE4AC-"].get_text()[:-3]):
                role4_ac()
        print(values)    
        sayac += 100
        if (sayac >= sure):
            role1_kapa()
            role2_kapa()
            role3_kapa()
            role4_kapa()


sg.theme("Reddit")

layout = [ [sg.Text("Port Seçiniz:"), sg.Combo(serial_ports(), size=(10,1)),
            sg.Text("Baud Seçiniz:"), sg.Combo(["110","300","600","1200", "2400", "4800", "9600", "14400", "19200", "38400", "57600", "115200", "128000", "256000"]), 
            sg.Button(button_text="Bağlan", key="-BAGLAN-", size=(10,1)) ],
            [sg.Text("", size=(10,1), key="-BAGLANDI_TEXT-")],
            [sg.Button(button_text="RÖLE 1 AÇ", key="-ROLE1AC-", button_color=("black", "OliveDrab1"), font=("Arial Black", 10), mouseover_colors=("black", "green"), size=(30,2)), 
            sg.Button(button_text="RÖLE 1 KAPA", disabled=True, button_color=("white", "firebrick2"), font=("Arial Black", 10), key="-ROLE1KAPA-", mouseover_colors=("white", "red"), size=(30,2))],
            [sg.Button(button_text="RÖLE 2 AÇ", key="-ROLE2AC-", button_color=("black", "OliveDrab1"), font=("Arial Black", 10), 	mouseover_colors=("black", "green"), size=(30,2)), 
            sg.Button(button_text="RÖLE 2 KAPA", disabled=True, button_color=("white", "firebrick2"), font=("Arial Black", 10), key="-ROLE2KAPA-", mouseover_colors=("white", "red"), size=(30,2))],
            [sg.Button(button_text="RÖLE 3 AÇ", key="-ROLE3AC-", button_color=("black", "OliveDrab1"), font=("Arial Black", 10), 	mouseover_colors=("black", "green"), size=(30,2)), 
            sg.Button(button_text="RÖLE 3 KAPA", disabled=True, button_color=("white", "firebrick2"), font=("Arial Black", 10), key="-ROLE3KAPA-", mouseover_colors=("white", "red"), size=(30,2))],
            [sg.Button(button_text="RÖLE 4 AÇ", key="-ROLE4AC-", button_color=("black", "OliveDrab1"), font=("Arial Black", 10), 	mouseover_colors=("black", "green"), size=(30,2)), 
            sg.Button(button_text="RÖLE 4 KAPA", disabled=True, button_color=("white", "firebrick2"), font=("Arial Black", 10), key="-ROLE4KAPA-", mouseover_colors=("white", "red"),size=(30,2))],
            [sg.Button(button_text="AYARLAR", key="settings", size=(15,1)), sg.Button(button_text="ZAMANLAMA", key="zamanlama", size=(15,1))]
            ]

window = sg.Window("PySimpleGUI Röle Kontrol", layout)

while True:
    event, value = window.read() 
    print(event)
    if event == "-BAGLAN-":
        serial_baglan()
    if event == "-ROLE1AC-":
        role1_ac()
    if event == "-ROLE1KAPA-":
        role1_kapa()
    if event == "-ROLE2AC-":
        role2_ac()
    if event == "-ROLE2KAPA-":
        role2_kapa()
    if event == "-ROLE3AC-":
        role3_ac() 
    if event == "-ROLE3KAPA-":
        role3_kapa()
    if event == "-ROLE4AC-":
        role4_ac() 
    if event == "-ROLE4KAPA-":
        role4_kapa() 
    if event == "settings":
        ayarlar()
    if event == "zamanlama":
        zamanlama()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break      
window.close()
