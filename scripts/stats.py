def sessionStats():

    from scripts.db import pandasUtilPiloto
    from IPython.display import display
    from scripts.general import fechaLocal

    dbPiloto = pandasUtilPiloto()
    sessionInstances = dbPiloto['sessionInstance'].unique()
    for sessionInstance in sessionInstances:
        dbPilotoBySession = dbPiloto[dbPiloto['sessionInstance'] == sessionInstance]
        display ('El usuario ' + dbPilotoBySession.iloc[0]['alias'] + ' inicio sesion el ' + str(fechaLocal(sessionInstance)) + ' y juego ' + str(len(dbPilotoBySession['levelInstance'])) + ' niveles.')

def condicion(serie, M):
    from IPython.display import display
    import math
    """
    serie: cadena de true/false
    M: numero de opciones en cada respuesta (dos para paralelismo, tres para angulos)

    Esta funcion busca en la serie de datos como se puede catalogar la serie. Para eso se utiliza el siguiente analsis:

    Se busca que hubo mas, si correctas o incorretcas.
        Si hubo mas incorrectas si mira cual es la probabilidad de que se trate de una respuesta al azar. Si es significativamente poco probable que sea al azar se asume
            que el usuario esta distinguiendo pero interpretando mal. Si no se asume que el usuario no distingue.
        Si hubo mas correctas, entonces lo que interesa es ver si empeoro la performance hacia el final (es decir si al aumentar la dificultad hubo algun comabio en la performance).
        Para eso usamos un test de fisher entre la primer mitad y la segunda


    El return es una lista con los siguientes datos:
        pValue correctas
        pValue fisher primer mitad vs segunda mitad
    """


    # Vamos a usar la funcion distribucionDeProbabilidadRandom que tenia escrita, y que es mas compleja (sirve para calcular probabilidades con diferentes N todo junto) pero sirve igual

    if M==2:
        histograma = [0,len(serie)]
    if M==3:
        histograma = [0,0,len(serie)]

    # Calculamos la distribucion de una respuesta random con el setup de trials usado (esta funcion la habia hecho en otra epoca para casos mas complejos)
    distribucion = distribucionDeProbabilidadRandom (histograma)
    # Calculamos la cantidad de rtas correctas
    correctas = sum (1 for x in serie if x)
    # Calculamos los pValue, n el caso de las incorrectas sumamos uno por como selecciona en las listas python
    pValueCorrectas = sum (x for x in distribucion[correctas:])

    # Hacemos el pValue con una cuadro del tipo:
    #           Primer mitad   segunda mitad
    # correctas      a              b
    # incorrectas    c              d
    primerMitad = serie[:len(serie)//2]
    segundaMitad = serie[len(serie)//2:]
    a = sum (1 for x in primerMitad if x)
    b = sum (1 for x in segundaMitad if x)
    c = sum (1 for x in primerMitad if not x)
    d = sum (1 for x in segundaMitad if not x)
    n = a + b + c + d
    # Fuente : https://en.wikipedia.org/wiki/Fisher's_exact_test
    pValueFisher = math.factorial (a+b) * math.factorial (c+d) * math.factorial (a+c) * math.factorial (b+d) / (math.factorial (a) * math.factorial (b) * math.factorial (c) * math.factorial (d) * math.factorial (n))

    return pValueCorrectas, pValueFisher


def distribucionDeProbabilidadRandom (histograma):
    """
        Esta funcion sirve para analizar cual es la probabilidad de responder N trials correctos en funcion del setup del level y poder tener una medida de la significancia de la cantidad de aciertos medidos.
        Para eso se asume que la hipotesis nula es responder al azar y se calcula a partir de la cantidad de trials que hay con cada cantidad de opciones por trial cual seria la probabilidad de acierto respondiendo al azar.

        El input (histograma), es un vector de enteros donde cada casillero representa la cantidad de trials que hay en el level con ese numero de opciones (en realidad como el primer elemento del vector es el 0, en dicho casillero esta la cantidad de trials con una unica opcion a elegir y asi sucesivamente)
        El output es un vector de floats que representa la probabilidad de responder N (donde N es el indice del valor) respuestas correctas respondiendo al azar.
    """

    import sys
    if not sys.version_info[:2] == (3, 4):
        print ('Sos un boludo!, pero uno previsor')
        print ('Este codigo esta pensado para correr en python 3.4')


    import math

    distribuciones = [0] * len(histograma)
    # Primer calculamos la distribucion de probabilidad para cada subset de trials con identicas opciones de respuesta
    for i in range(len(histograma)):
        N = i+1 # Representa el numero de opciones posibles a elegir
        m = histograma[i] # Representa el numero de trials que se contestan en el subset
        subset_N = [0] * (m+1) # Sumamos el 1 porque si hay cero elementos igual hay una opcion, las opciones son el cerrado [0,numero de trials]
        p = 1/N # es la probabilidad de acertar entre la cantidad de opciones presentadas (que es i+1)
        if m==0:
            distribuciones[i] = [1]
        else:
            for j in range(m+1): # j representa la cantidad de opciones correctas
                # Calculamos la probabilidad de obtener una cantidad de respuestas correctas j, cuando cada trial tiene N opciones
                Pj = math.pow(p,j)*math.pow(1-p,m-j)*math.factorial(m)/(math.factorial(j)*math.factorial(m-j))
                subset_N[j] = Pj
            distribuciones[i] = subset_N
    # Aqui ya esta la distribucion de cada subset. ahora hay que calcular la distribucion global, para eso hay que combinar las dritribciones

    # La idea es que si tenemos dos distribuciones N1 y N2 cada uno con J y J' elementos (donde J y J' es el numero de trials maximo que hay con N1 y N2 opciones)
    # y j1 representa la probabilidad de responder j1 veces bien en los trials de N1 opciones y j2 representar la probabilidad de responder j2 veces bien
    # en los trials de N2 opciones,
    # entonces la suma de todos los productos cuyos indices j1 +j2 de j3 es la probabilidad de responde j3 veces bien entre los trials de N1 y N2 opciones
    combinado = [1] # Inicialmente hay probabilidad 1 de tener 0 bien
    for N in range(len(distribuciones)):
        combinadoNew = [0] * (sum(histograma)+1) # Armo una combinacion que este vacia
        for i_1 in range(len(combinado)):
            if combinado[i_1] != 0: # Esto tiene dos razones, una es evitar cuentas innecesarias. La otra mas importante es evitar que aplique el contador hasta el final y que la suma de los dos contadores de mas que el numero de trials maximos posible, lo que genera un error
                for i_2 in range(len(distribuciones[N])):
                    combinadoNew[i_1+i_2] = combinadoNew[i_1+i_2] + combinado[i_1]*distribuciones[N][i_2] #Acumulo todos las combinaciones
        combinado = combinadoNew

    return combinado


def statByUser (alias=["Todos"], completado=True, expList=['UmbralAngulosPiloto', 'UmbralParalelismoPiloto']):
    from scripts.db import pandasUtilPiloto
    from IPython.display import display
    from scripts.plots import plotConvergenciaVersionPiloto
    import pandas as pd

    db = pandasUtilPiloto()

    if alias == ["Todos"]:
        users = db['alias'].unique()
    else:
        users = alias

    stats = pd.DataFrame()

    for user in users:

        userDb = db[db['alias']==user]

        if completado:
            userDb = userDb[userDb['convergenciaFinalizada']==True]

        exps = userDb['expName'].unique()
        for exp in exps:
            if exp in expList:
                expDb = userDb[userDb['expName']==exp]
                for index, row in expDb.iterrows():
                    #plotConvergenciaVersionPiloto(db.ix[[index]], exp, fromStadistics=True)
                    if exp == 'UmbralAngulosPiloto':
                        M=3
                    if exp == 'UmbralParalelismoPiloto':
                        M=2
                    aciertos = [elemento['acertado'] for elemento in row['historial']]
                    valores = [elemento['estimulo']['desviacion'] for elemento in row['historial']]
                    senales = [elemento['estimulo']['nivelSenal'] for elemento in row['historial']]
                    mean = sum (valores[-6:]) / 6
                    if mean < 0:
                        mean = - mean
                    # Creamos la entrada para el DataFrame
                    elemento = {}
                    elemento['userId'] = row['userId']
                    elemento['userAlias'] = row['alias']
                    elemento['expName'] = row['expName']
                    elemento['identificador'] = row['identificador']
                    elemento['levelInstance'] = row['levelInstance']
                    elemento['referencia'] = row['referencia']
                    elemento['serieSenal'] = [senales]
                    elemento['serieValores'] = [valores]
                    elemento['serieAciertos'] = [aciertos]
                    elemento['meanValue'] = mean
                    elemento['pValueCorrectas'], elemento['pValueFisher'] = condicion (aciertos,M)
                    if elemento['pValueCorrectas'] < 0.05:
                        elemento['deteccionCorrecta'] = True
                    else:
                        elemento['deteccionCorrecta'] = False
                    if elemento['pValueCorrectas'] > 0.9:
                        elemento['deteccionInCorrecta'] = True
                    else:
                        elemento['deteccionInCorrecta'] = False
                    if elemento['pValueFisher'] < 0.1:
                        elemento['evolucionDetectada'] = True
                    else:
                        elemento['evolucionDetectada'] = False
                    elemento['contar'] = 1
                    if elemento['expName'] == 'UmbralParalelismoPiloto':
                        idCategoria = 'Paralelismo '
                    if elemento['expName'] == 'UmbralAngulosPiloto':
                        idCategoria = 'Angulo '
                    idCategoria = idCategoria + str(elemento['referencia']) + ' grados'
                    elemento['idCategoria'] = idCategoria
                    stats = pd.concat([stats, pd.DataFrame.from_dict(elemento)])

    return stats

def cualitativeStatsPlot(stats):
    from IPython.display import display
    import matplotlib.pyplot as plt
    import numpy as np

    deteccionesCorrectas = []
    deteccionesIncorrectas = []
    sinDetecciones = []
    etiqueta = []
    # Hacemos un grafico para cada referencia
    for idCategoria in stats['idCategoria'].unique():
        db=stats[stats['idCategoria']==idCategoria]

        etiqueta = etiqueta + [idCategoria]
        deteccionesCorrectas = deteccionesCorrectas + [len(db[db['deteccionCorrecta']==True])]

        deteccionesIncorrectas = deteccionesIncorrectas + [len(db[db['deteccionInCorrecta']==True])]
        sinDetecciones = sinDetecciones + [len (db[ (db['deteccionCorrecta']==False) & (db['deteccionInCorrecta']==False) ])]

    # Hacemos los graficos (ejemplo extraido de http://matplotlib.org/examples/api/barchart_demo.html)
    ind = np.arange(len(etiqueta))
    width = 0.35       # the width of the bars: can also be len(x) sequence
    p1 = plt.bar(ind, deteccionesCorrectas, width, color='b')
    p2 = plt.bar(ind, deteccionesIncorrectas, width, color='r', bottom=deteccionesCorrectas)
    p3 = plt.bar(ind, sinDetecciones, width, color='gray', bottom=[sum(x) for x in zip(deteccionesIncorrectas, deteccionesCorrectas)])

    plt.ylabel('Casos')
    plt.title('Grado de detección segun experimento y orientación (N= '+str((deteccionesCorrectas[0]+deteccionesIncorrectas[0]+sinDetecciones[0])/2)+')')
    plt.xticks(ind + width/2., etiqueta, rotation='vertical')
    plt.yticks(np.arange(0, len(deteccionesCorrectas) + len (deteccionesIncorrectas) + len(sinDetecciones) + 1, 1))
    plt.legend([p1[0],p2[0],p3[0]], ['Interpreta la señal correctamete (p=0.05)','Interpreta la señal incorrectamente (p=0.9)','No interpreta la señal (0.05<p<0.9)'], loc='center left', bbox_to_anchor=(1, 0.5))

    plt.show()

def cuantitativeStatsPlotParalelismo(stats):
    from IPython.display import display
    import matplotlib.pyplot as plt
    import numpy as np

    # Filtramos los datos donde hay deteccion positiva
    db = stats[stats['deteccionCorrecta']==True]
    db = db[db['expName']=='UmbralParalelismoPiloto']
    # Creamos la lista de variables
    etiquetas = []

    umbralPos = []
    errPos = []
    outliersPos = []
    nPos = []

    umbralNeg = []
    errNeg = []
    outliersNeg = []
    nNeg = []

    umbral = []
    err = []
    out = []
    n = []

    umbralTot = []
    errTot = []
    nTot = []


    # Hacemos los calculos para cada referencia
    for referencia in stats['referencia'].unique():
        dbCat=db[db['referencia']==referencia]
        etiquetas = etiquetas + [str(referencia)]
        # Acercamiento positivo
        datos = dbCat[dbCat['identificador']=='Acercamiento Positivo']['meanValue']
        datos = datos[is_outlier(datos)==False]
        umbralPos = umbralPos + [np.mean(datos)]
        errPos = errPos + [np.std(datos)]
        outliersPos = outliersPos + [len(dbCat[dbCat['identificador']=='Acercamiento Positivo']['meanValue']) - len(datos)]
        nPos = nPos + [len(datos)]
        # Acercamiento negativo
        datos = dbCat[dbCat['identificador']=='Acercamiento Negativo']['meanValue']
        datos = datos[is_outlier(datos)==False]
        umbralNeg = umbralNeg + [np.mean(datos)]
        errNeg = errNeg + [np.std(datos)]
        outliersNeg = outliersNeg + [len(dbCat[dbCat['identificador']=='Acercamiento Negativo']['meanValue']) - len(datos)]
        nNeg = nNeg + [len(datos)]
        #conjunto
        datos = dbCat['meanValue']
        datos = datos[is_outlier(datos)==False]
        umbral = umbral + [np.mean(datos)]
        err = err + [np.std(datos)]
        out = out + [len(dbCat['meanValue']) - len(datos)]
        n = n + [len(datos)]
        #conjunto total
        datos = dbCat['meanValue']
        umbralTot = umbralTot + [np.mean(datos)]
        errTot = errTot + [np.std(datos)]
        nTot = nTot + [len(datos)]


    # Hacemos el grafico, ejemplo extraido de : http://matplotlib.org/examples/api/barchart_demo.html
    ind = np.arange(len(etiquetas))  # the x locations for the groups
    width = 0.20       # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, umbralPos, width, color='lime', yerr=errPos)
    rects2 = ax.bar(ind + width, umbralNeg, width, color='lightgreen', yerr=errNeg)
    rects3 = ax.bar(ind + 2*width, umbral, width, color='green', yerr=err)
    rects4 = ax.bar(ind + 3*width, umbralTot, width, color='green', yerr=errTot)

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Angulo de separacion')
    ax.set_title('Umbral de deteccion del angulo de separacion en funcion de la orientacion')
    ax.set_xticks(ind + width)
    ax.set_xticklabels(etiquetas)

    for i in range(len(etiquetas)):
        # Ponemos el cabezal de los n para pos
        ax.text(ind[i] + width/2., umbralPos[i] + 0.15,
                'n='+str(nPos[i]),
                ha='center', va='bottom')
        ax.text(ind[i] + width/2., umbralPos[i] + 0.05,
                'out='+str(outliersPos[i]),
                ha='center', va='bottom')
        # Para los neg
        ax.text(ind[i] + width/2. + width, umbralNeg[i] + 0.15,
                'n='+str(nNeg[i]),
                ha='center', va='bottom')
        ax.text(ind[i] + width/2. + width, umbralNeg[i] + 0.05,
                'out='+str(outliersNeg[i]),
                ha='center', va='bottom')
        # Para el total
        ax.text(ind[i] + width/2. + 2*width, umbral[i] + 0.15,
                'n='+str(n[i]),
                ha='center', va='bottom')
        ax.text(ind[i] + width/2. + 2*width, umbral[i] + 0.05,
                'out='+str(out[i]),
                ha='center', va='bottom')
        # Para el total sin outs
        ax.text(ind[i] + width/2. + 3*width, umbralTot[i] + 0.15,
                'n='+str(nTot[i]),
                ha='center', va='bottom')


    ax.legend((rects1[0], rects2[0], rects3[0], rects4[0]), ('Aproximacion positiva', 'Aproximacion negativa', 'Aproximacion total', 'Total con outsiders'), loc='center left', bbox_to_anchor=(1, 0.5))


    plt.show()

def cuantitativeStatsPlotAngulos(stats):
    from IPython.display import display
    import matplotlib.pyplot as plt
    import numpy as np

    # Filtramos los datos donde hay deteccion positiva
    db = stats[stats['deteccionCorrecta']==True]
    db = db[db['expName']=='UmbralAngulosPiloto']
    # Creamos la lista de variables
    etiquetas = []

    umbralPos = []
    errPos = []
    outliersPos = []
    nPos = []

    umbralNeg = []
    errNeg = []
    outliersNeg = []
    nNeg = []

    umbral = []
    err = []
    out = []
    n = []

    umbralTot = []
    errTot = []
    nTot = []

    # Hacemos los calculos para cada referencia
    for referencia in stats['referencia'].unique():
        dbCat=db[db['referencia']==referencia]
        etiquetas = etiquetas + [str(referencia)]
        # Acercamiento positivo
        datos = dbCat[dbCat['identificador']=='1er Cuad.']['meanValue']
        datos = datos[is_outlier(datos)==False]
        datos = [-(dato - referencia  - 90) for dato in datos]
        umbralPos = umbralPos + [np.mean(datos)]
        errPos = errPos + [np.std(datos)]
        outliersPos = outliersPos + [len(dbCat[dbCat['identificador']=='1er Cuad.']['meanValue']) - len(datos)]
        nPos = nPos + [len(datos)]
        # Acercamiento negativo
        datos = dbCat[dbCat['identificador']=='2do Cuad.']['meanValue']
        datos = datos[is_outlier(datos)==False]
        datos = [dato - referencia  - 90  for dato in datos]
        umbralNeg = umbralNeg + [np.mean(datos)]
        errNeg = errNeg + [np.std(datos)]
        outliersNeg = outliersNeg + [len(dbCat[dbCat['identificador']=='2do Cuad.']['meanValue']) - len(datos)]
        nNeg = nNeg + [len(datos)]
        #conjunto sin outisiders
        datos = dbCat['meanValue']
        # Cambiamos el signo segun corresponda
        datos = [dato - referencia - 90 for dato in datos]
        datos = [-dato if dato < 0 else dato for dato in datos]
        datos = np.array(datos)
        datos = datos[is_outlier(datos)==False]
        umbral = umbral + [np.mean(datos)]
        err = err + [np.std(datos)]
        out = out + [len(dbCat['meanValue']) - len(datos)]
        n = n + [len(datos)]
        # conjunto total!
        datos = dbCat['meanValue']
        # Cambiamos el signo segun corresponda
        datos = [dato - referencia - 90 for dato in datos]
        datos = [-dato if dato < 0 else dato for dato in datos]
        umbralTot = umbralTot + [np.mean(datos)]
        errTot = errTot + [np.std(datos)]
        nTot = nTot + [len(datos)]

    # Hacemos el grafico, ejemplo extraido de : http://matplotlib.org/examples/api/barchart_demo.html
    ind = np.arange(len(etiquetas))  # the x locations for the groups
    width = 0.20       # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, umbralPos, width, color='lime', yerr=errPos)
    rects2 = ax.bar(ind + width, umbralNeg, width, color='lightgreen', yerr=errNeg)
    rects3 = ax.bar(ind + 2*width, umbral, width, color='green', yerr=err)
    rects4 = ax.bar(ind + 3*width, umbralTot, width, color='green', yerr=errTot)

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Angulo')
    ax.set_title('Diferencia minima respecto al angulo recto para que haya deteccion')
    ax.set_xticks(ind + width)
    ax.set_xticklabels(etiquetas)

    for i in range(len(etiquetas)):
        # Ponemos el cabezal de los n para pos
        ax.text(ind[i] + width/2., umbralPos[i] + 10,
                'n='+str(nPos[i]),
                ha='center', va='bottom')
        ax.text(ind[i] + width/2., umbralPos[i] + 5,
                'out='+str(outliersPos[i]),
                ha='center', va='bottom')
        # Para los neg
        ax.text(ind[i] + width/2. + width, umbralNeg[i] + 10,
                'n='+str(nNeg[i]),
                ha='center', va='bottom')
        ax.text(ind[i] + width/2. + width, umbralNeg[i] + 5,
                'out='+str(outliersNeg[i]),
                ha='center', va='bottom')
        # Para el total
        ax.text(ind[i] + width/2. + 2*width, umbral[i] + 10,
                'n='+str(n[i]),
                ha='center', va='bottom')
        ax.text(ind[i] + width/2. + 2*width, umbral[i] + 5,
                'out='+str(out[i]),
                ha='center', va='bottom')
        # Para el total con out
        ax.text(ind[i] + width/2. + 3*width, umbralTot[i] + 10,
                'n='+str(nTot[i]),
                ha='center', va='bottom')


    ax.legend((rects1[0], rects2[0], rects3[0], rects4[0]), ('Aproximacion desde los agudos', 'Aproximacion desde los graves', 'Conjunto', 'Conjunto con Outsiders'), loc='center left', bbox_to_anchor=(1, 0.5))


    plt.show()




def is_outlier(points, thresh=3.5):
    import numpy as np
    """

    Fuente : http://stackoverflow.com/questions/22354094/pythonic-way-of-detecting-outliers-in-one-dimensional-observation-data


    Returns a boolean array with True if points are outliers and False
    otherwise.

    Parameters:
    -----------
        points : An numobservations by numdimensions array of observations
        thresh : The modified z-score to use as a threshold. Observations with
            a modified z-score (based on the median absolute deviation) greater
            than this value will be classified as outliers.

    Returns:
    --------
        mask : A numobservations-length boolean array.

    References:
    ----------
        Boris Iglewicz and David Hoaglin (1993), "Volume 16: How to Detect and
        Handle Outliers", The ASQC Basic References in Quality Control:
        Statistical Techniques, Edward F. Mykytka, Ph.D., Editor.
    """
    if len(points.shape) == 1:
        points = points[:,None]
    median = np.median(points, axis=0)
    diff = np.sum((points - median)**2, axis=-1)
    diff = np.sqrt(diff)
    med_abs_deviation = np.median(diff)

    modified_z_score = 0.6745 * diff / med_abs_deviation

    return modified_z_score > thresh
