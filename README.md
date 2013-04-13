qsim
====

simulación equilibrio y cuasiequilibrio para localización urbana

Archivos .py:
- main.py
- model_template.py
- custom_file_reader.py
- data_manager.py
- data_struct.py
- data_plot.py
- Models/*.py


Como está ahora, funciona así:

main.py lee el archivo qsim-config.txt y lanza una corrida, 
usando los datos de la carpeta Data y un modelo de la carpeta Models.

Se usa data_manager.py para leer los datos de los archivos txt y convertirlos 
en variables. data_struct.py es una unidad de datos, en data_manager hay un array
de data_structs. custom_file_reader.py es el lector de los archivos.

El data_manager.py interactúa con el modelo escogido. Los modelos están en la carpeta Models.
Todos heredan de la clase model_template.py, y lo que hacen es implementar ciertas funciones 
que quedaron en blanco en el template.

Durante la ejecución del modelo y a la salida se imprimen varios archivos log (esto está bien 
desordenado, cualquiera puede imprimir un log). Al final de todo el proceso se genera 
un archivo con el package pickle, y se generan varios output (carpetas datfiles y Output)

Posteriormente a la ejecución, puede correrse la rutina data_plot.py para generar gráficos en base al
último pickle generado.



By Cristian Prado
