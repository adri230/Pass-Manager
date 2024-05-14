# Password-Manager

Para su correcta utilización se debe usar MySQL o MariaDB con una base de datos llamada proyecto. El script se comunica con dos tablas, webs y contrasenas, las cuales continenen un id y un varchar de 50 (con el nombre de la web y la contraseña, respectivamente). Además, en la tabla contrasenas también hay un campo id_web que es una clave foranea de el id en la tabla webs.

También pide una contraseña para empezar a guardar contraseñas, la cual esta guardada con un cifrado SHA256 en la variable hash. Si se quiere cambiar solo hay que poner otra contraseña en el mismo formato.

Por último, este script DEBE usarse en modo administrador, ya sea con sudo o con una terminal de administrador de Powershell, ya que si no va a fallar. Si se quiere evitar el uso de administrador hay que eliminar la parte de detectar una llave de seguridad (segundo if)
