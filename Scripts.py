def distribucionDeProbabilidadRandom (histograma):
    
    
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


def fechaLocal (millisec):
    
    import sys
    if not sys.version_info[:2] == (3, 4):
        print ('Sos un boludo!, pero uno previsor')
        print ('Este codigo esta pensado para correr en python 3.4')
    
    
    import datetime
    
    return datetime.datetime.fromtimestamp(millisec/1000)


def makeHistogramaTrials (touchs):
    
    import sys
    if not sys.version_info[:2] == (3, 4):
        print ('Sos un boludo!, pero uno previsor')
        print ('Este codigo esta pensado para correr en python 3.4')
    
    
    import pandas as pd
    
    #
    # Esta rutina encuentra un histograma de frecuencia de cantidad de opciones para elegir respuesta.
    # La idea es que con estos datos despues se puede calcular como es una distribucion de respuestas random y asi saber cual es la probabilidad de hipotesis nula
    # El histograma tiene que tener un largo igual al maximo de opciones posibles +1 porque el en casillero cero se guarda la cantidad con cero opciones
    # Esto no tiene mucho sentido conceptual aca pero si despues para las cuentas
    #
    
    # Filtramos un solo touch por cada trial (en teoria como son trials de tipo TEST hay uno solo pero podria ser que en el futuro no)
    trialInstances = touchs['trialInstance'].unique()
    infoTrials = pd.concat(pd.DataFrame(touchs[touchs['trialInstance']==trialInstance].iloc[0]).transpose() for trialInstance in trialInstances)
        
    # Extraemos la info del json del trial
    temp = pd.DataFrame(columns=['elementosId'])
    for (i,r) in infoTrials.iterrows():
        e = r['jsonTrial']
        temp.loc[i] = [e['elementosId']]
    infoTrials = pd.concat([infoTrials, temp], axis=1)
    
    histograma = []
    for index, trial in infoTrials.iterrows():
        if len(trial['elementosId']) > len (histograma): 
            ext = [0] * (len(trial['resourcesIdSort'])-len (histograma))
            histograma.extend(ext)
        histograma[len(trial['resourcesIdSort'])-1] = histograma[len(trial['resourcesIdSort'])-1] + 1
    
    return histograma

def findTrueFirstTouch (touchs):
    # Esta funcion asume que solo tiene sentido contar un touch como true si hay un solo touch por trial!
    aciertos = 0;
    trialInstances = touchs['trialInstance'].unique()
    for trialInstance in trialInstances:
        if len(touchs[touchs['trialInstance']==trialInstance].index) == 1:
            touchsAEvaluar = touchs[touchs['trialInstance']==trialInstance].iloc[0]
            if touchsAEvaluar['isTrue']==True:
                aciertos = aciertos + 1
    return aciertos

def significativos(distribucion):
    acumulado=0
    for i in range(len(distribucion)):
        acumulado = acumulado + distribucion[i]
        if acumulado > 0.95:
            return i
        
        
        
def resumen (reporteSignificancia):
    
    import pandas as pd
    
    reportePandas = pd.DataFrame(reporteSignificancia)
    reportePandas['Tag'] = "L:" + reportePandas['Level'].apply(str) +' \n D: '  + reportePandas['FiltroDificultad'].apply(str)

    
    # Reporte simplificado
    fig = plt.figure(figsize=(30,3))
    ax = fig.add_subplot(111)
    title = 'Resultados obtenidos y aciertos significativos vs nivel y dificultad'
    ax.set_title(title, fontsize=10, fontweight='bold')
    ax.set_xlabel('Numero de respuestas correctas')
    ax.set_ylabel('Nivel+Dificultad')
    ax.set_ylim([0,40]) # Aca hay que cambiarlo si se hacen levels de mas de 40 trials

    i=0
    tags = []
    for tag in reportePandas['Tag'].unique():
        reportes = reportePandas[reportePandas['Tag']==tag]
        # Filtramos solo donde hay mas de 10 preguntas.
        if len(reportes.iloc[0]['DistribucionRandom']) > 10:
            i = i + 1
            x=[i-0.25,i+0.25]        
            # Agregamos el label
            tags.append(tag)
            # Dibujamos todos los intentos
            for valor in reportes['RtasCorrectas'].tolist():
                if valor > reportes.iloc[0]['Significativo']:
                    color = 'green'
                else:
                    color = 'red'
                y=[valor,valor]
                ax.plot(x,y,color)
            # Dibujamos la significancia  
            x=[i-0.1,i+0.1]
            y=[reportes.iloc[0]['Significativo'],reportes.iloc[0]['Significativo']]
            color = 'yellow'
            ax.plot(x,y,color)
    # Agregamos el label
    plt.xticks(range(1,i+1), tags)
            
    plt.show()
    
    
def joinDB(touchs, sounds, tag, identificador):
    
    import os
    import pandas as pd
    from IPython.display import display

    # Creamos una base de datos vacia
    touchsToJoin = touchs.copy()
    soundsToJoin = sounds.copy()
    
    # Cargamos los datos ya guardados
    display ('Verificando datos guardados previamente')
    filenameTouchs = 'dbTouchs'
    filenameSounds = 'dbSounds'
    
    if os.path.isfile(filenameTouchs):
        touchsLoad = pd.read_pickle(filenameTouchs)
        display ('Datos de touchs previos cargados')
    else:
        display ('Datos de touchs previos inexistentes')
        touchsLoad = pd.DataFrame()

    if os.path.isfile(filenameSounds):
        soundsLoad = pd.read_pickle(filenameSounds)
        display ('Datos de sounds previos cargados')
    else:
        display ('Datos de sounds previos inexistentes')
        soundsLoad = pd.DataFrame()

        
    # Limpiamos de los touchs a almacenar los que ya estan almacenados
    if touchsLoad.index.size>0:
        for (i,r) in touchsLoad.iterrows():
            touchsToJoin.drop(touchsToJoin.index[touchsToJoin['touchInstance'] == r['touchInstance']], inplace=True)
    touchsToJoin['TagJoin'] = tag
    touchsToJoin['identificador'] = identificador
            
    # Limpiamos de los sounds a almacenar los que ya estan almacenados
    if soundsLoad.index.size>0:
        for (i,r) in soundsLoad.iterrows():
            soundsToJoin.drop(soundsToJoin.index[soundsToJoin['soundInstance'] == r['soundInstance']], inplace=True)
    soundsToJoin['TagJoin'] = tag
    soundsToJoin['identificador'] = identificador
    
    soundsLoad = soundsLoad.append(soundsToJoin, ignore_index=True)
    display ('Agregados '+str(soundsToJoin.index.size)+' entradas a los sounds')
    soundsLoad.to_pickle(filenameSounds)
    touchsLoad = touchsLoad.append(touchsToJoin, ignore_index=True)
    display ('Agregados '+str(touchsToJoin.index.size)+' entradas a los touchs')
    touchsLoad.to_pickle(filenameTouchs)
      
def loadFromDb(identificador):

    import sys
    if not sys.version_info[:2] == (3, 4):
        print ('Sos un boludo!, pero uno previsor')
        print ('Este codigo esta pensado para correr en python 3.4')
        
    import os
    import pandas as pd
    from IPython.display import display    
    
    display ('Verificando datos guardados previamente')
    filenameTouchs = 'dbTouchs'
    filenameSounds = 'dbSounds'
    
    if os.path.isfile(filenameTouchs):
        touchsLoad = pd.read_pickle(filenameTouchs)
        display ('Datos de touchs previos cargados')
    else:
        display ('Datos de touchs previos inexistentes')
        touchsLoad = pd.DataFrame()

    if os.path.isfile(filenameSounds):
        soundsLoad = pd.read_pickle(filenameSounds)
        display ('Datos de sounds previos cargados')
    else:
        display ('Datos de sounds previos inexistentes')
        soundsLoad = pd.DataFrame()
       
    if identificador!=0:
        touchsLoad = touchsLoad[touchsLoad['identificador']==identificador] 
        soundsLoad = soundsLoad[soundsLoad['identificador']==identificador]
        
    return touchsLoad, soundsLoad

def guardarComo (touchs, filename):
    import pandas as pd
    import os
    from IPython.display import display
    
    import sys
    if not sys.version_info[:2] == (3, 4):
        print ('Sos un boludo!, pero uno previsor')
        print ('Este codigo esta pensado para correr en python 3.4')
        
    if os.path.isfile(filename):
        display ('Ya existe una base de datos con ese nombre')
    else:
        display ('Archivo guardado')
        touchs.to_pickle(filename)
        
def cargarTouchs (filename):
    
    import sys
    if not sys.version_info[:2] == (3, 4):
        print ('Sos un boludo!, pero uno previsor')
        print ('Este codigo esta pensado para correr en python 3.4')
        
    import pandas as pd
    import os
    from IPython.display import display
    
    if os.path.isfile(filename):
        return pd.read_pickle (filename)
    else:
        display ('No existe una base de datos guardada con el nombre: '+filename)
    
    
    
def buscarUmbral (touchs):
    
    import pandas as pd    
    from IPython.display import display
    from Scripts import fechaLocal
    
    import numpy as np # importando numpy
    from scipy import stats # importando scipy.stats

    # Creamos un dataframe para guardar los datos
    resumen = pd.DataFrame(columns=['AnguloReferencia','MediaDeltaTita','DesviacionDeltaTita','CumpleCriterioCola','Session','Usuario','Level','LevelVersion'])
    
    for usuario in touchs['Alias'].unique():
        touchsUsuario = touchs[touchs['Alias']==usuario]
        for session in touchsUsuario['sessionInstance'].unique():
            touchsSession = touchsUsuario[touchsUsuario['sessionInstance']==session]

            for level in touchsSession['levelInstance'].unique():

                resumenToAppend = pd.DataFrame(columns=['AnguloReferencia','MediaDeltaTita','DesviacionDeltaTita','CumpleCriterioCola','Session','Usuario','Level','LevelVersion'])
                
                # Cargamos cosas en el resumen
                resumenToAppend['Session'] = [fechaLocal(session)]
                resumenToAppend['Usuario'] = [usuario]
                resumenToAppend['Level'] = [fechaLocal(level)]
                
                
                touchsLevel = touchsSession[touchsSession['levelInstance']==level]
                
                #filtramos la ultima mitad de los datos
                touchsLevelEnd = touchsLevel.iloc[-int(touchsLevel.index.size/2):,:]
            
                # Miramos si tiene algun tipo de sentido (que este en el fondo de la cola). Para eso revisamos que no haya mas false que true (Xq una vez q se estabiliza tiene q haber dos true x cada false (el codigo disminuye la señal despues de dos aciertos))
                # y ademas revisamos que no haya menos de 1/4 de falses xq eso indicaria que no esta rebotando
                
                levelInfo = touchsLevel.iloc[0]
                contadorTouchsLevelTrue = touchsLevelEnd[touchsLevelEnd['isTrue']==True].index.size
                contadorTouchsLevelFalse = touchsLevelEnd[touchsLevelEnd['isTrue']==False].index.size
                                
                if ((contadorTouchsLevelTrue < contadorTouchsLevelFalse) or (contadorTouchsLevelFalse*3<contadorTouchsLevelTrue)):
                    resumenToAppend['CumpleCriterioCola'] = [False]
                else:
                    resumenToAppend['CumpleCriterioCola'] = [True]
                        
            
                # Extraemos la info de del delta tita del estimulo de cada trial
                columnName = 'DeltaTita'
                if not columnName in touchsLevelEnd.columns:
                    temp = pd.DataFrame(columns=[columnName])
                    for (i,r) in touchsLevelEnd.iterrows():
                        e = r['jsonMetaDataRta']
                        temp.loc[i] = [e['infoConceptual']['deltaAngulo']]
                    touchsLevelEnd = pd.concat([touchsLevelEnd, temp], axis=1)
                else:
                    display ('Warning: Se encontraron datos ya cargados para: '+columnName)
                    
                # Extraemos la info del angulo de referencia
                columnName = 'AnguloDeReferencia'
                if not columnName in touchsLevelEnd.columns:
                    temp = pd.DataFrame(columns=[columnName])
                    for (i,r) in touchsLevelEnd.iterrows():
                        e = r['jsonMetaDataRta']
                        temp.loc[i] = [e['infoConceptual']['direccionAnguloReferencia']]
                    touchsLevelEnd = pd.concat([touchsLevelEnd, temp], axis=1)
                else:
                    display ('Warning: Se encontraron datos ya cargados para: '+columnName)
                    
                levelInfo = touchsLevelEnd.iloc[0]
                datos = touchsLevelEnd['DeltaTita'].tolist()
                
                resumenToAppend['AnguloReferencia'] = [levelInfo['AnguloDeReferencia']]
                resumenToAppend['MediaDeltaTita'] = [np.mean(datos)]
                resumenToAppend['DesviacionDeltaTita'] = [np.std(datos)]
                resumenToAppend['LevelVersion'] = [levelInfo['levelVersion']]
                resumen = pd.concat([resumen, resumenToAppend], axis=0, ignore_index=True)
    
    return resumen
                