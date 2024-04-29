# Pass-Manager

Para su correcta utilización se debe usar MySQL o MariaDB con una base de datos llamada proyecto. El script se comunica con dos tablas, webs y contrasenas, las cuales continenen un id y un varchar de 50 (con el nombre de la web y la contraseña, respectivamente). Además, en la tabla contrasenas también hay un campo id_web que es una clave foranea de el id en la tabla webs.
