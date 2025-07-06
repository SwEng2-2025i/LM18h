# Laboratorio 2: Implementacion de generacion de reportes en PDF y tests para el borrado de datos de prueba

**Autor: Adrian Ramirez Gonzalez**

Este codigo toma coma base el ejemplo mostrado en el repositorio y a partir de este incluye las siguientes funcionalidades:

1. Borrado de los datos de prueba generados ademas de tests que verifican el correcto borrado de estos datos.

2. Generacion de reportes en PDF tanto para los tests asociados al Back End como al Front End.

## Modificaciones realizadas

### `Front-End/main.py`

Se implementaron dos secciones más dentro del diseño de la pagina las cuales permitirán recibir el ID de las tareas y usuarios para poder eliminarlos. Ademas, se crearon las funciones **eliminarUsuario()** y **eliminarTarea()** las cuales están asociadas a estas secciones para que se pueda realizar el borrado de las tareas y usuarios.

### `Task_Service/main.py`

Se realiza la implementación de un nuevo endpoint el cual permitirá borrar una tarea en especifico haciendo uso de su ID.

```http
URL: http://localhost:5002/tasks/<int:task_id>
Metodo: DELETE
```

### `Test/BackEnd-Test.py`

Dentro de este archivo se implementan las siguientes funciones:

1. **get_users()**: Función encargada de realizar una petición GET al servicio de usuarios para obtener todos los usuarios almacenados en la base de datos.

2. **delete_user()**: Función encargada de realizar una petición DELETE para borrar un usuario de la base de datos haciendo uso de su ID.

3. **delete_task():** Función encargada de realizar una petición DELETE para borrar una tarea de la base de datos haciendo uso de su ID.

Estas funciones son usadas dentro de la función **integration_test()** para borrar los datos de prueba. Una vez los datos son borrados, se usan las funciones **get_users()** y **get_tasks()** para verificar que los datos si fueron borrados correctamente. Adicionalmente, se crea un arreglo llamado **resultados** el cual guarda los resultados obtenidos en cada uno de los test para posteriormente generar el PDF con el reporte.

### `Test/FrontEnd-Test.py`

Dentro de este archivo se implementan las siguientes funciones:

1. **eliminar_tarea**: Función encargada de hacer uso del Front End creado para eliminar una tarea por medio de su ID.

2. **eliminar_usuario**: Función encargada de hacer uso del Front End creado para eliminar un usuario por medio de su ID.

3. **verificar_tarea_eliminada**: Función encargada de realizar una petición GET al servicio de tareas para verificar si la tarea fue eliminada o no.

4. **verificar_usuario_eliminado**: Función encargada de realizar una petición GET al servicio de usuarios para verificar si el usuario fue eliminado o no.

Nuevamente, se hace uso de un arreglo llamado **resultados** para guardar los resultados de cada test realizado para luego poder generar el reporte en PDF.

### `Test/report_generator.py`

Este nuevo archivo se encarga de generar los reportes en PDF haciendo uso de los datos obtenido en cada test. Los resultados son guardados en las carpetas "Back End Test Reports" y "Front End Test Reports", dependiendo de cual test se está ejecutando.

### `Users_Service/main.py`

Se implementa un nuevo endpoint el cual permite la eliminacion de un usuario de la base de datos por medio de su ID.

```http
URL: http://localhost:5001/users/<int:user_id>
Metodo: DELETE
```

## Inicialización del proyecto

Es necesario ejecutar el siguiente comando para instalar los paquetes necesarios:

```bash
pip install -r requirements.txt
```

Una vez instalados, hay que ejecutar los siguientes comandos:

- **Ejecución servicio Front End**

```bash
python Front-End/main.py
```

- **Ejecución servicio Back End - Tasks**

```bash
python Task_Service/main.py
```

- **Ejecución servicio Back End - Users**

```bash
python Users_Service/main.py
```

Esto ejecutará los servicios Back End de usuarios y tareas, y también inicializará el Front End que permitirá usar estos servicios.

## Ejecución de tests

Para ejecutar las pruebas, es necesario ejecutar alguno de los siguientes comandos (dependiendo de que test se quiera realizar):

- **Ejecución test Back End**

```bash
    python Test/BackEnd-Test.py
```

- **Ejecución test Front End**

```bash
    python Test/FrontEnd-Test.py
```

Al finalizar cualquiera de los test, se generará un PDF con el reporte de los resultados de los tests. Este reporte se guardara en la carpeta "Back End Test Reports" ó "Front End Test Reports", dependiendo de que test se haya ejecutado.

## Resultados de los tests

### Servicios Back End

De acuerdo a lo tests realizados a los servicios Back End, se puede confirmar que ambos servicios están funcionando correctamente, permitiendo tanto la creacion de tareas y usuarios asi como el correcto borrado de estos.

### Servicio Front End

Respecto al servicio Front End, la ejecución del test permite confirmar que la pagina se esta comportando como se espera tanto al momento de crear usuarios y tareas asi como al momento de borrarlos. La visualizacion de tareas tambien parece funcionar correctamente. Todo esto lleva a concluir que el servicio Front End se está comunicando correctamente con los servicios Back End.
