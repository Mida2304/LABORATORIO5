<h1 align="center"> LABORATORIO 5. Variabilidad de la Frecuencia Cardiaca usando la Transformada Wavelet </h1>

Autores: Midalys Vanessa Aux y Manuela Martínez Camacho

# Introducción
Somos seres humanos, cada uno de nosotros cuenta con un grupo de organos que cumplen con distintas funciones para permitirnos estar vivos, sin embargo, hay uno que, en lo personal, es el más importante de todos, y lo podríamos catalogar como "El centro de la vida". Exactamente, se trata del corazón, cuya función principal es bombear la sangre a todo el cuerpo para que las células que nos componen reciban oxígeno y nutrientes, y así se pueda eliminar el dióxido de carbono y otros desechos.

Lo anterior es de gran importancia para entender un siguiente concepto, el cual se trata de la frecuencia cardiaca, pero ¿Qué es la frecuencia cardiaca y que relación tiene con nuestra vida, y así mismo, con esta área de procesamiento de señales?

En el presente laboratorio se pretende responder esta pregunta mediante el análisis de la variabilidad de la frecuencia cardiaca (HRV) haciendo uso de la transformada wavelet para, de esta forma, identificar las frecuencias características y analizar la dinámica temporal de la señal cadiaca, esto mediante el uso se otros componentes como un modulo ECG, código en Python, entre otros.

### Procedimiento:

En primer lugar se crea la interfaz grafica con cada uno de los items a tener en cuenta, como el tomar la captura a tiempo real, guardar todos los datos tomados, plantear el analisis espectral y prueba de hipotesis.

<img src="https://github.com/Mida2304/LABORATORIO5/blob/main/interfaz.png?raw=true" width="20%" />


Posteriormente, gracias a la teoria se planteo en el laboratorio, se procede instalar el programa NI MAX el cual permitira identificar la conexion de DAQ National Instruments, para ser conectado al AD8232 que permitira adquirir la señal ECG.

<img src="https://github.com/Mida2304/LABORATORIO5/blob/main/conexion.jpg?raw=true" width="20%" />

A continuacion se muestra la conexion con el DAQ

<img src="https://github.com/Mida2304/LABORATORIO5/blob/main/daq.jpg?raw=true" width="40%" />

Posteriormente se realiza la prueba de aquisiscion de datos:

<img src="https://github.com/Mida2304/LABORATORIO5/blob/main/adquisicion.jpg?raw=true" width="40%" />

### Conceptos para tener en cuenta:
En este siguiente ítem se encuentran los conceptos que se deben tener en cuenta para poder entender de forma más adecuada el presente laboratorio.
##### • [^1^] Frecuencia cardiaca (HRV): 
La frecuencia cardiaca se refiere al número de veces que el corazón late por minuto (gracias a ello estamos vivos). Esta es una medida clave del funcionamiento del sistema cardiovascular. Se expresar en latidos por minuto (lpm), y su valor normal en reposo debe ser entre los 60 y 100 lpm.

Esta medida puede variar según la edad y sirve como un indicador del estado de salud del corazón y del sistema cardiovascular. Por ejemplo, un corazón sano late de manera eficiente para poder bombear la sangre necesaria para el cuerpo, sin embargo, una frecuencia alta o baja puede indicar problemas cardíacos o desequilibrios del organismos. Así mismo, personas como los atletas suelen poseer una frecuencia cardíaca en reposo más baja, lo cual muestra que su corazón es mucho más eficiente, aunque una frecuencia alta indica que existe una falta de condición física o estrés corporal. Estos y muchos más indicadores se pueden divisar al obtener la frecuencia cardíaca, y de igual forma, es mucho más valiosa al momento en que se analiza, como se hará en este presente.
[^1^]:Edward R. Laskowski, M. D. (2022, October 8). Dos maneras fáciles y precisas de Medir Tu Frecuencia Cardíaca. Mayo Clinic. https://www.mayoclinic.org/es/healthy-lifestyle/fitness/expert-answers/heart-rate/faq-20057979 

##### • [^2^] Señal de frecuencia cardiaca: 
La señal de frecuencia cardiaca es una representación eléctrica o digital del ritmo de los latidos del corazón a lo largo del tiempo, esta es la señal que se va a proceder a análizar. Se obtiene mediante sensores que detectan cada latidos y generan una señal que puede ser analizada o visualizada.

Existen dos formas comunes de esta señal: Electrocardiograma (ECG) y Señal de pulsaciones (PPG). Para esta práctica, se tiene el ECG, el cual mide la actividad eléctrica del corazón, y esta muestra ondas que representan cómo se activan las distintas partes del corazón en cada latido. Como se mencionó anteriormente, se usa en hospitales y equipos médicos para detectar algún tipo de patología como lo pueden ser arritmias, infartos, entre otros.
[^2^]: Heart rate signal. Heart Rate Signal - an overview | ScienceDirect Topics. (n.d.). https://www.sciencedirect.com/topics/computer-science/heart-rate-signal 

##### • [^3^] Transformada Wavelet: 
Esta es una técnica matemática que nos permite analizar señales en el tiempo y en la frecuencia al mismo tiempo. Es de gran utilidad para poder estudiar señales que cambian a lo largo del tiempo, como la señal de frecuencia cardíaca, lo cual no lo puede hacerr la transformada de Fouriere tradicional.

El procedimiento que esta requiere es tener una señal, escoger entre los distintos tipos de Wavelets que se tienen (como Haar, Daubechies, Morlet, etc), interpretar la señal eliminando el ruido y detectando los picos o eventos (como los latidos cardíacos anómalos), y esta puede ser visible haciendo uso de un software como lo es en este caso Python.
[^3^]: Transformada wavelet. acervo para el mejoramiento del aprendizaje de alumnos de ingeniera en Inteligencia Artificial. (n.d.). https://virtual.cuautitlan.unam.mx/intar/?page_id=1108  

Para el procedimiento anterior se tienen que tomar en cuenta las siguientes librerias:
##### - sys: Interactuar con sistema operativo de la interfaz.
##### - csv: Sirve para leer y escribir archivos en formatos CSV.
##### - PyQt6: Libreria empelada para la creación de la interfaz grafica, botones, ventanas y muestra de la adquisicion de los datos.
##### - numpy: Para la realización de calculos numericos, estadistica, algebra y arreglos. 
##### - pyqtgraph: Para graficar datos dentro de la interfaz en tiempo real.
##### - nidaqmx: libreria empleada para controlar dispositivos de adquisición de National Instruments NI DAQ, leyendo directamente la señal EMG de la targeta de adquisicion (en el caso del presente, se empleo un AD8232).
##### - AcquisitionType: Para especificar el tipo de adquisicion de datos (lectura continua o captura puntual).
##### - butter, filtfilt, iirnotch: Crea un filtro Butterworth sin cambiar la fase y un filtro rechaza banda para eliminar el ruido de 50 a 60 Hz, filtrando y suavizando la señal.

<img src="https://github.com/Mida2304/LABORATORIO5/blob/main/librerias.png?raw=true" width="20%" />

Posteriormente, se crea la adquisicion de datos a tiempo real con DAQ y utilizando el boton iniciar captura se procede a visualizar los datos de la señal ECG a tiempo real.

<img src="https://github.com/Mida2304/LABORATORIO5/blob/main/iniciar.png?raw=true" width="20%" />
En la anterior parte de codigo se puede visualizar su estructura tanto par iniciar como para detener dado que debemos tener un tiempo de toma de la muestra de 5 minutos o 300 s

Seguidamente, una vez obtenida la señal a tiempo real, se utiliza el boton "guardar cvs" ara que los datos obtenidos en tiempo real sean guardados en este tipo de archivo y el boton "cargar cvs" para cargar los datos en pantalla y hacer su respectivo analisis.

<img src="https://github.com/Mida2304/LABORATORIO5/blob/main/se%C3%B1al.png?raw=true" width="20%" />

Con esta parte obtenida se procede a implementar un sistema de filtrado, gracias a la literatura, se aplicara un filtro IIR y buterwort para que la señal de la frecuencia cardiaca salga con menos interferencia:

<img src="https://github.com/Mida2304/LABORATORIO5/blob/main/filtro%2B.png?raw=true" width="60%" />

Posteriormente, se identifican los picos R de toda la señal cabe resaltar que se trata de 300 s

<img src="https://github.com/Mida2304/LABORATORIO5/blob/main/picos.png?raw=true" width="60%" />

A continuación se calcula los intervalos R-R para la obtencion de una nueva señal.
<img src="https://github.com/Mida2304/LABORATORIO5/blob/main/rr.png?raw=true" width="60%" />

Con estos resoltados podemos obtener la frecuencia cardiaca promedio, del anterior grafico se obtienen los siguientes resultados:
<img src="https://github.com/Mida2304/LABORATORIO5/blob/main/datosrr.png?raw=true" width="60%" />

Con el resultado de la media de intervalos podemos obtener la frecuencia cardiaca dividiendo 60 sobre el promedio y posteriormente tomar el tiempo total (en el presente 300 segundos) y dividirlo por el resultado anterior, con ello tenemos que nuestro sujeto tuvo una Frecuencia de 66

Con estos resultados, vamos a estudiar dos tipos de transformada Wavelet en la parte continua y Discreta, en continua usaremos Morlet y discreta Daubechies:

<img src="https://github.com/Mida2304/LABORATORIO5/blob/main/dabushe.png?raw=true" width="60%" />

Esta transformada se utiliza para la compresión de señales, eliminación de ruido, extracción de características.
<img src="https://github.com/Mida2304/LABORATORIO5/blob/main/morlet.png?raw=true" width="60%" />

La transformada Wavelet Morlet detectar características transitorias, como los picos R, ondas P y T con buena precisión en ambas dimensiones.


# Requisitos
- Contar con Python 3.9.0 instalado.
- Contar con señal internet.
- Instalar las librerías necesarias instaladas para ejecutar el código correctamente.
- Contar con conocimiento sobre programacion en Python.
- Contar con un AD8232
- Instalar IN MAX
- Tener conocimientos sobre el funcionamiento de DAQ
  
  
# Usar
Por favor, cite este articulo de la siguiente manera:

Aux, M.; Martinez, M.;  LABORATORIO 4. FATIGA. 4 de Abril de 2025.

# Información de contacto

est.manuela.martin@unimilitar.edu.co y est.midalys.aux@unimilitar.edu.co
