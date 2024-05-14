## ANTES DE EJECUTAR EL SCRIPT INSTALAR CON PIP mysql.connector, pyperclip y fido2

import hashlib, mysql.connector, pyperclip    # Usado para el cifrado hash de la contraseña, conectar con MySQL y copiar la contraseña en el portapapeles
from getpass import getpass                   # Usado para que la contraseña no se vea
from fido2.hid import CtapHidDevice           # Usado para detectar la llave de seguridad FIDO2


hash="a389a638dec32538f55b0c8dc5c84f84aad65bcd5aacd5f05d36f30b71271a6b"


#############################################
## Funcion que imprime por pantalla un menú##
#############################################
def menu(): 
    print("-------------")
    print("1. Añadir nueva contraseña")
    print("2. Acceder a las contraseñas")
    print("3. Salir")
    print("-------------")

def menu2():
    print("--------------")
    print("1. Ver contraseña de sitio web")
    print("2. Ver todos las webs almacenadas")
    print("3. Borrar contraseña")
    print("4. Volver")
    print("--------------")

dbserver=mysql.connector.connect(        # Variable con los datos necesarios para la conexion con la base de datos
    host="localhost",
    user="root",
    password="",
    database="proyecto",
)

cursor=dbserver.cursor()                  # Es necesario crear un cursor para que funcione la libreria de mysql.connector

contr=getpass("Contraseña: ")             # Pido por consola la contraseña y la guardo en una variable
passwd= hashlib.sha256()
passwd.update(contr.encode('utf-8'))      # Creo una variable en la que uso la liberia hashlib con sha256 y codifico la cadena con utf-8 para despues devolver
salida=passwd.hexdigest()                 # los datos como cadena hexadecimal

if salida==hash:                         

    devices = list(CtapHidDevice.list_devices())            # Variable en la que se guardan los dipositivos FIDO2
    if devices:

        menu()
        option = int(input("Elija una opcion: "))

        while True:
            if option==1:
                web=input("Nombre de la página web sobre la que quieres guardar una contraseña: ")
                cursor.execute(f"INSERT INTO webs(Nombre) VALUES('{web}')")

                contraseña=getpass("Contraseña a almacenar: ")
                cursor.execute(f"INSERT INTO contrasenas(contraseña, Id_web) SELECT '{contraseña}', webs.ID FROM webs WHERE webs.Nombre='{web}'")

                dbserver.commit()             # Hago un commit para guardar la insercion de datos

                print ("Contraseña almacenada.")

                menu()
                option = int(input("Elija una opcion: "))

            elif option==2:
                menu2()
                option2= int(input("Di una opcion: "))
                if option2==1:
                    # Aqui codigo sobre ver contraseñas #

                    web=input("Sitio web del que deseas la contraseña: ")
                    cursor.execute(f"SELECT Contraseña FROM Contrasenas WHERE Id_web IN (SELECT ID FROM webs WHERE Nombre='{web}')")

                    passwd=cursor.fetchone()
                    for passw in passwd:
                        pyperclip.copy(passw)


                elif option2==2:
                    # Aqui codigo sobre ver sitios web #

                    cursor.execute("SELECT * FROM webs")           
                    webs=cursor.fetchall()
                    
                    print ("Webs disponibles:")
                    print ("--------------")
                    for web in webs:
                        print(web)


                elif option2==3:
                    # Aqui codigo sobre borrar contraseña #

                    web=input("Sitio web que deseas eliminar: ")

                    cursor.execute(f"DELETE FROM contrasenas WHERE Id_web in (SELECT ID FROM webs WHERE Nombre='{web}')")
                    cursor.execute(f"DELETE FROM webs WHERE Nombre='{web}'")

                    dbserver.commit()

                    print("Contraseña borrada.")

                    menu()
                    option = int(input("Elija una opcion: "))


                elif option2==4:
                    menu()
                    option=int(input("Di una opcion: "))

            elif option==3:
                print("Saliendo...")
                break
            else:
                print("Error.")
                print("Elija una opcion valida.")
                menu()
                option = int(input("Di una opcion: "))

    else:
        print("Llave FIDO2 no conectada. Saliendo...")

else:
    print("Contraseña incorrecta. Saliendo...")
