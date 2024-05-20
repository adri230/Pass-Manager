# Password Manager

Este script realizado en lenguaje Python permite a un usuario guardar sus contraseñas en una base de datos y acceder a ella mediante un menú diseñado con Tkinter. Además, este script está diseñado para no permitir el acceso sin una llave de seguridad FIDO2 y una contraseña maestra.

## Requisitos

Para poder usar este script es necesario contar con MySQL, MariaDB u otro sistema gestor de bases de datos, que contenga una base de datos llamada proyecto.

Esta base de datos va a contener dos tablas llamadas webs y contrasenas, respectivamente. Webs contará con dos columnas, Id (INT como clave primaria) y Nombre (VARCHAR de 50), y contrasenas tendrá Id (INT como clave primaria), Contraseña (VARCHAR de 50) y Id_web (INT clave foránea del Id de webs).

Además también es necesario descargar mediante [pip](https://pip.pypa.io/en/stable/) varias bibliotecas:

```bash
pip install fido2 mysql-connector pyperclip
```

## Uso

Para usar el script simplemente se ejecuta y se pone la contraseña maestra, que es <<Contraseña>> de forma predeterminada. Si se quiere cambiar esta contraseña solo hay que cambiar el valor de la variable hash por la contraseña que se desee cifrada en SHA256, que se puede conseguir en páginas como [esta](https://10015.io/tools/sha256-encrypt-decrypt).

El script debe ejecutarse como administrador si se desea usar la versión con autentificación mediante llave de seguridad, ya que de otra manera fallaría.

