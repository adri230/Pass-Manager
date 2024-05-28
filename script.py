## ANTES DE EJECUTAR EL SCRIPT INSTALAR CON PIP mysql.connector, pyperclip, fido2, tk y customtkinter

import hashlib, mysql.connector, pyperclip, tkinter   # Usado para el cifrado hash de la contraseña, conectar con MySQL y copiar la contraseña en el portapapeles
import customtkinter as ctk
from getpass import getpass                           # Usado para que la contraseña no se vea
from fido2.hid import CtapHidDevice                   # Usado para detectar la llave de seguridad FIDO2
from tkinter import simpledialog, messagebox          # Usado para los cuadros de dialogo de tkinter y los cuadros de información


hash="a389a638dec32538f55b0c8dc5c84f84aad65bcd5aacd5f05d36f30b71271a6b"


dbserver=mysql.connector.connect(        # Variable con los datos necesarios para la conexion con la base de datos
    host="localhost",
    user="root",
    password="",
    database="proyecto",
)

cursor=dbserver.cursor()                  # Es necesario crear un cursor para que funcione la libreria de mysql.connector

def main_menu():
    main=ctk.CTk()
    #main=tkinter.Tk()
    main.title("Gestor de Contraseñas")
    main.geometry("400x300")

    def add_pass():
        web=simpledialog.askstring("Añadir contraseña","Nombre de la web: ")
        cursor.execute(f"INSERT INTO webs(Nombre) VALUES('{web}')")
        
        contraseña=simpledialog.askstring("Añadir contraseña", "Contraseña a almacenar: ")
        cursor.execute(f"INSERT INTO contrasenas(contraseña, Id_web) SELECT '{contraseña}', webs.ID FROM webs WHERE webs.Nombre='{web}'")

        dbserver.commit()             # Hago un commit para guardar la insercion de datos
        messagebox.showinfo()

    def access_pass():
        submenu=ctk.CTkToplevel()
        #submenu=tkinter.Toplevel()
        submenu.title("Acceso a contraseñas")
        submenu.geometry("400x300")

        def show_pass():
            web=simpledialog.askstring("Mostrar contraseña","Nombre de la web:")
            cursor.execute(f"SELECT Contraseña FROM Contrasenas WHERE Id_web IN (SELECT ID FROM webs WHERE Nombre='{web}')")

            passwd=cursor.fetchone()
            for passw in passwd:
                pyperclip.copy(passw)

            messagebox.showinfo("Información","La contraseña se ha copiado al portapapeles")

        def show_webs():
            cursor.execute("SELECT Nombre FROM webs")           
            webs=cursor.fetchall()
            nombres=[]
            for web in webs:
                nombres.append(web[0])
            
            if nombres:
                lista="\n".join(nombres)
            else:
                lista="No hay webs almacenadas"
            
            messagebox.showinfo("Webs almacenadas", lista)
                
        def delete_pass():
            web=simpledialog.askstring("Borrar contraseña", "Sitio web a eliminar:")
            cursor.execute(f"DELETE FROM contrasenas WHERE Id_web in (SELECT ID FROM webs WHERE Nombre='{web}')")
            cursor.execute(f"DELETE FROM webs WHERE Nombre='{web}'")

            dbserver.commit()
            messagebox.showinfo("Información","Contraseña borrada")

        tkinter.Button(master=submenu, text="Ver contraseña de sitio web", command=show_pass).pack(anchor="center")
        tkinter.Button(master=submenu,text="Ver sitios webs almacenados", command=show_webs).pack(anchor="center")
        tkinter.Button(master=submenu,text="Borrar contraseña", command=delete_pass).pack(anchor="center")
    
    tkinter.Button(text="Añadir nueva contraseña",command=add_pass).pack(anchor="center")
    tkinter.Button(text="Acceder a información sobre contraseñas", command=access_pass).pack(anchor="center")
    tkinter.Button(text="Salir", command=main.destroy).pack(anchor="center")

    main.mainloop()



contr=getpass("Contraseña: ")             # Pido por consola la contraseña y la guardo en una variable
passwd= hashlib.sha256()
passwd.update(contr.encode('utf-8'))      # Creo una variable en la que uso la liberia hashlib con sha256 y codifico la cadena con utf-8 para despues devolver
salida=passwd.hexdigest()                 # los datos como cadena hexadecimal

if salida==hash:                         
    devices= True
    #devices = list(CtapHidDevice.list_devices())            # Variable en la que se guardan los dipositivos FIDO2
    if devices:

        main_menu()

    else:
        print("Llave FIDO2 no conectada. Saliendo...")

else:
    print("Contraseña incorrecta. Saliendo...")
