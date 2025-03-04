# Estadística computacional: la estadística sin dolor
![](img/school-4251037_1920.jpg)

{octicon}`calendar` 2024-04-25

Desde antiguo, las matemáticas se han servido de dos estrategias diferentes a la hora encontrar soluciones a problemas concretos: fuerza bruta o métodos analíticos. Hasta no hace tanto, la fuerza bruta era sinónimo de cálculos aritméticos llevados a cabo por humanos, un procedimiento que resultaba inviable en problemas mínimamente complejos. Por ello, generaciones de matemáticos brillantes tuvieron que inventar fórmulas alternativas para llegar a las soluciones. El uso de métodos analíticos necesitaba en cada caso asumir condiciones y hacer simplificaciones sobre el problema al cual se aplicaba, unas instrucciones que se convertían en sí mismas en una teoría sofisticada.

Sin embargo, desde hace un tiempo, la disponibilidad de los ordenadores y su capacidad de computación ha hecho que el planteamiento de la fuerza bruta haya ganado protagonismo en las matemáticas. Los métodos numéricos además ya no son exclusivos de las universidades y los centros de investigación, porque la facilidad de acceso a potentes procesadores y herramientas de programación ha permitido que cualquiera pueda simular un problema complejo a golpe de cálculos reiterativos.

La estadística se ha beneficiado especialmente de este cambio de paradigma, puesto que sus practicantes se pueden liberar de la complejidad de la teoría analítica, en la que realmente no se sabe muy bien qué es lo que se está haciendo, y centrarse en cambio en resolver el problema de una manera más intuitiva. La mayoría de los métodos analíticos no son fáciles de comprender y se limitan a describir cuándo y cómo aplicar las fórmulas, lo cual lleva a la frustración de los que buscan asimilar las ideas fundamentales que las sustentan.

Mediante la computación, sin embargo, la estadística puede convertirse en «elegantes algoritmos en lugar de confusas masas de ecuaciones». Lo explica de forma muy simple un científico de datos llamado John Rauser en su charla titulada [Statistics Without the Agonizing Pain](https://www.youtube.com/watch?v=5Dnw46eC-0o&t=2s) («Estadística sin dolorosa lucha»).

## ¿Te pican más los mosquitos si bebes cerveza?

En el vídeo, John Rauser se vale de un ejemplo para explicar la idea. Presenta un estudio en el que la pregunta de partida es: ¿Te vuelves más atractivo a los mosquitos si bebes cerveza? Se plantea un experimento con dos grupos de personas, unas que beben agua (18 participantes) y otras cerveza (25). Y a continuación la prueba computa la cantidad de mosquitos que ha atraído cada individuo. Los resultados se muestran en las siguientes listas:

```
agua = [21, 19, 13, 22, 15, 22, 15, 22, 20, 12, 24, 24, 21, 19, 18, 16, 23, 20]
media = 19.2

cerveza = [27, 19, 20, 20, 23, 17, 21, 24, 31, 26, 28, 20, 27, 19, 25, 31, 24, 28, 24, 29, 21, 21, 18, 27, 20]
media = 23.6
```

Es decir, los que bebieron agua atrajeron una media de 19.2 mosquitos, mientras que los que bebieron cerveza recibieron las visita de un promedio de 23.6 mosquitos. Entre estos dos grupos se produce una diferencia de 23.6 – 19.2 = 4.4 mosquitos a favor de los que bebieron cerveza. Y aquí es cuando surge la pregunta estadística: ¿es la diferencia obtenida de estas muestras _suficiente_ para declarar que, en términos generales, beber cerveza te hace más atractivo para los mosquitos?

En opinión del escéptico, esta diferencia de 4.4 mosquitos es pequeña y podría haberse dado por casualidad, sin que el consumo de cerveza influyera en ello:

→ H0 (hipótesis nula): La cerveza no influye en la cantidad de mosquitos atraídos.

La postura contraria defendería que 4.4 mosquitos es una diferencia considerable que rara vez ocurriría por azar y que por tanto la cerveza sí tiene efecto:

→ HA (hipótesis alternativa): beber cerveza atrae a los mosquitos.

Lo cierto es que no podemos saber si la diferencia observada entre estos dos grupos o muestras ocurrió por azar o no, pero lo que sí puede hacer la estadística por nosotros es calcular la probabilidad (valor-p) de que dicha diferencia contemplada fuera resultado de la fortuna (ruido, H0) o bien respondiera a una realidad de la población (patrón, HA).

## Método analítico

Para este tipo de problemas, utilizaríamos un test llamado prueba t de Student o Test-T. El nombre procede de un señor llamado [William Sealy Gosset](https://en.wikipedia.org/wiki/William_Sealy_Gosset), quien a principios del siglo XX trabajaba para la fábrica de Guiness en Dublin y desarrolló un método analítico para averiguar la calidad de la cerveza partiendo de pequeñas muestras. Para no dar pistas a la competencia, William Sealy Gosset publicó su trabajo bajo el seudónimo de _Student_ (estudiante), y de ahí el nombre del test.

&nbsp;

![](img/William_Sealy_Gosset.jpg)

&nbsp;

Su método proporciona una serie de ecuaciones, entre las cuales se encuentra la siguiente:

&nbsp;

![](img/t-test-formula.webp)

&nbsp;

Con esta ecuación se obtiene la distribución de probabilidades, en la cual habría que situar la probabilidad asociada a la muestra observada. Un valor-p muy bajo (típicamente inferior a 0.05 o 5%) indicaría que las probabilidades de que el fenómeno observado fuera fruto del azar serían muy bajas, más bajas cuanto más pequeño el valor-p. Tan bajas que, en el problema de los mosquitos y la cerveza, la asunción de la hipótesis nula (_H0: La cerveza no influye en la cantidad de mosquitos atraídos_) nos parecería incluso ridícula por sus escasas probabilidades de suceder, de manera que nos decantaríamos por la hipótesis alternativa (_HA : beber cerveza atrae a los mosquitos_).

Afortunadamente, hoy no hay necesidad de coger papel y lápiz para ponerse a hacer los cálculos a mano. Un programa escrito en el lenguaje Python resolvería la cuestión en un par de líneas de código utilizando la función correspondiente de la librería estadística.

```
# Import statistical package
import scipy.stats as stats

# Perform the two-sample t-test
t_result= stats.ttest_ind(agua, cerveza)
print(f"p = {t_result[1]:.4f}")
```
```
p = 0.0009
```

El valor-p obtenido en este caso resulta ser muy pequeño, de forma que refutaríamos H0 para abrazar HA.

Pero ¿en qué han consistido exactamente estos cálculos? Ni idea. Yo al menos no lo sabría explicar. Todo lo que tengo es el resultado. Elegí utilizar la _prueba t de Student_ o _Test-T_ porque es la receta que nos dicen que tenemos que utilizar en este tipo de problemas, pero alcanzamos a saber poco de cómo funciona (al menos si no hemos profundizado y somos expertos en estadística).

## Método computacional

La alternativa es utilizar un método computacional, también llamado de simulación. Lo que queremos dilucidar es si el valor observado, 4.4, es una diferencia pequeña o grande. Empecemos por plasmarlo en una gráfica.

&nbsp;

![](img/perm-2.png)

&nbsp;

Tomemos los datos de las muestras, coloreadas dependiendo de si el sujeto tomó agua o cerveza. Y ahora supongamos que es cierta la hipótesis nula H0: no hay diferencia alguna entre los dos grupos. Entonces, si es cierto esto, podríamos mezclar todos estos datos entre sí como quien baraja unos naipes y después repartir las cartas a los dos jugadores según la proporción inicial. Una permutación aleatoria, en términos matemáticos.