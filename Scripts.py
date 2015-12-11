def distribucionDeProbabilidadRandom (histograma):
    """ 
    este es el help
    alskdfgklajdfgha   
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
        touchs.to_pickle('./Guardados/'+filename)
        
def guardarComoSounds (sounds, filename):
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
        sounds.to_pickle(filename)
        
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
    
    
    
def buscarUmbral (touchs, ordenado=False):
    
    import pandas as pd    
    from IPython.display import display
    from Scripts import fechaLocal
    
    import numpy as np # importando numpy
    from scipy import stats # importando scipy.stats

    # Creamos un dataframe para guardar los datos
    resumen = pd.DataFrame(columns=['AnguloReferencia','MediaDeltaTita','DesviacionDeltaTita','CumpleCriterioCola','Session','Usuario','Level','LevelVersion','Identificador'])

    #Procesamos solo los datos de niveles completos
    touchs = touchs[touchs['levelCompleted']==True]
    
    for usuario in touchs['Alias'].unique():
        touchsUsuario = touchs[touchs['Alias']==usuario]
        for session in touchsUsuario['sessionInstance'].unique():
            touchsSession = touchsUsuario[touchsUsuario['sessionInstance']==session]

            for level in touchsSession['levelInstance'].unique():

                resumenToAppend = pd.DataFrame(columns=['AnguloReferencia','MediaDeltaTita','DesviacionDeltaTita','CumpleCriterioCola','Session','Usuario','Level','LevelVersion','Identificador'])
                
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
                if 'appVersion' in touchsLevelEnd.columns:
                    resumenToAppend['AppVersion'] = [levelInfo['appVersion']]
                else:
                    resumenToAppend['AppVersion'] = 'Sin Dato'
                if 'identificador' in touchsLevelEnd.columns:
                    resumenToAppend['Identificador'] = [levelInfo['identificador']]
                else:
                    resumenToAppend['Identificador'] = 'Dato no cargado'
                resumen = pd.concat([resumen, resumenToAppend], axis=0, ignore_index=True)
    
    if ordenado:
        resumen = resumen.sort(['AnguloReferencia'], ascending=[True])
    
    return resumen



def plotResumen (resumen, zoom=2):
    
    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib.cm as cm
    
    resumen['ReferenciaEnRadianes'] = resumen['AnguloReferencia']/180*np.pi
    resumen['MediaDeltaTitaRad'] = resumen['MediaDeltaTita']/180*np.pi
    resumen['RefRadCorregida'] = resumen['ReferenciaEnRadianes'] - resumen['MediaDeltaTitaRad']/2
    resumen['Color'] = ['g' if x else 'r' for x in resumen['CumpleCriterioCola'].tolist() ] 
    resumen['Identificador'].fillna('SinDato',inplace=True)
    
    fig = plt.figure(num=None, figsize=(10, 10), dpi=180, facecolor='w', edgecolor='k')
    ax = plt.subplot(111, projection='polar')
    ax.set_title("Separacion angular minima (en º) que se puede detectar en funcion de la orientacion de las rectas \'pseudoparalelas\'. \n El color del punto representa si se considera que la medicion paso un test de confianza o no.", va='bottom')

    for user in resumen['Usuario'].unique():
        resumenFiltrado = resumen[resumen['Usuario']==user]
        resumenInfo = resumenFiltrado.iloc[0]
        
        x = resumenFiltrado['ReferenciaEnRadianes'].tolist()
        y = resumenFiltrado['MediaDeltaTita'].tolist()
        color = resumenFiltrado['Color'].tolist()
        size = resumenFiltrado['DesviacionDeltaTita']
    
        ax.set_xticks(np.pi/180. * np.linspace(180,  -180, 36, endpoint=False))
        ax.plot(x, y, label=resumenInfo['Usuario'])
        ax.scatter(x, y, marker='o', c=color)
        ax.legend()
        
        fig2, ax2 = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))

        ax2.set_title("Visualizacion del overlap para el usuario " + user, va='bottom')
        ax2.set_xticks(np.pi/180. * np.linspace(180,  -180, 36, endpoint=False))

        theta = resumenFiltrado['RefRadCorregida'].tolist()
        radii = resumenFiltrado['MediaDeltaTita'].tolist()
        width = resumenFiltrado['MediaDeltaTitaRad'].tolist()
        bars = ax2.bar(theta, radii, width=width, bottom=0.0)
        for r,bar in zip(radii, bars):
            bar.set_facecolor( cm.jet(r/10.))
            bar.set_alpha(0.5)
        
        
        
    
    # Repetimos el plot pero con zoom
    fig = plt.figure(num=None, figsize=(10, 10), dpi=180, facecolor='w', edgecolor='k')
    
    if not all(i >= zoom for i in resumen['MediaDeltaTita'].tolist()):
        
        ax = plt.subplot(111, projection='polar')
        ax.set_title("Separacion angular minima (en º) que se puede detectar en funcion de la orientacion de las rectas \'pseudoparalelas\'. \n El color del punto representa si se considera que la medicion paso un test de confianza o no.", va='bottom')
        ax.set_ylim(0,zoom)
         

        for user in resumen['Usuario'].unique():
            resumenFiltrado = resumen[resumen['Usuario']==user]

            x = resumenFiltrado['ReferenciaEnRadianes'].tolist()
            y = resumenFiltrado['MediaDeltaTita'].tolist()
            color = resumenFiltrado['Color'].tolist()
            size = resumenFiltrado['DesviacionDeltaTita']
            resumenInfo = resumenFiltrado.iloc[0]
            
            ax.plot(x, y, label=resumenInfo['Usuario'])
            ax.scatter(x, y, marker='o', c=color)
            ax.legend()
        
"""            
            fig3, ax3 = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))

            ax3.set_title("Visualizacion del overlap para el usuario " + user +" con zoom.", va='bottom')
            ax3.set_xticks(np.pi/180. * np.linspace(180,  -180, 36, endpoint=False))
            ax3.set_ylim(0,0.02)
            
            theta = resumenFiltrado['RefRadCorregida'].tolist()
            radii = resumenFiltrado['MediaDeltaTita'].tolist()
            width = resumenFiltrado['MediaDeltaTitaRad'].tolist()
            bars = ax3.bar(theta, radii, width=width, bottom=0.0)
            for r,bar in zip(radii, bars):
                bar.set_facecolor( cm.jet(r/10.))
                bar.set_alpha(0.5)
"""
                
                
                
                
def plotConvergencia (touchs):
    
    import matplotlib.pyplot as plt
    import pandas as pd
        
    from IPython.display import display
    from Scripts import fechaLocal
    
    #Procesamos solo los datos de niveles completos
    touchs = touchs[touchs['levelCompleted']==True]
       
    for usuario in touchs['Alias'].unique():
        display ('Se hara la estadistica del usuario: '+usuario)
        touchsUsuario = touchs[touchs['Alias']==usuario]
        display ('El usuario '+usuario+' jugo '+str(len(touchsUsuario['sessionInstance'].unique()))+' veces')
        for session in touchsUsuario['sessionInstance'].unique():
            touchsSession = touchsUsuario[touchsUsuario['sessionInstance']==session]

            # Analizamos los datos para dificultad generica
            display ('En la session '+ str(fechaLocal(session))+ ' el usuario '+str(usuario)+' jugo '+str(len(touchsSession['levelInstance'].unique())) + ' niveles')
            for level in touchsSession['levelInstance'].unique():

                touchsLevel = touchsSession[touchsSession['levelInstance']==level]
                
                # Extraemos la info de del delta tita del estimulo de cada trial
                columnName = 'DeltaTita'
                if not columnName in touchsLevel.columns:
                    temp = pd.DataFrame(columns=[columnName])
                    for (i,r) in touchsLevel.iterrows():
                        e = r['jsonMetaDataRta']
                        temp.loc[i] = [e['infoConceptual']['deltaAngulo']]
                    touchsLevel = pd.concat([touchsLevel, temp], axis=1)
                else:
                    display ('Warning: Se encontraron datos ya cargados para: '+columnName)
                    
                # Extraemos la info del angulo de referencia
                columnName = 'AnguloDeReferencia'
                if not columnName in touchsLevel.columns:
                    temp = pd.DataFrame(columns=[columnName])
                    for (i,r) in touchsLevel.iterrows():
                        e = r['jsonMetaDataRta']
                        temp.loc[i] = [e['infoConceptual']['direccionAnguloReferencia']]
                    touchsLevel = pd.concat([touchsLevel, temp], axis=1)
                else:
                    display ('Warning: Se encontraron datos ya cargados para: '+columnName)
                
                levelInfo = touchsLevel.iloc[0]
                touchsLevelTrue = touchsLevel[touchsLevel['isTrue']==True]
                touchsLevelFalse = touchsLevel[touchsLevel['isTrue']==False]
                
                # Armamos el grafico
                fig = plt.figure(figsize=(10,3))
                ax = fig.add_subplot(111)
                title = 'Evolucion de la dificultad en funcion del trial \n' + 'Usuario: '+str(usuario) + ' direccion de refrencia: ' + str(levelInfo['AnguloDeReferencia'])+' grados, ' + 'levelVersion '+str(levelInfo['levelVersion']) 
                ax.set_title(title, fontsize=10, fontweight='bold')
                ax.set_xlabel('Numero de trial')
                ax.set_ylabel('Delta Tita (grados)')
                x = touchsLevel.index
                y = touchsLevel['DeltaTita'].tolist()
                ax.plot(x,y)
                x = touchsLevelTrue.index
                y = touchsLevelTrue['DeltaTita'].tolist()
                ax.plot(x,y,'go')
                x = touchsLevelFalse.index
                y = touchsLevelFalse['DeltaTita'].tolist()
                ax.plot(x,y,'ro')
                
                
def DownloadFile ():
    import datetime
    import time
    import urllib
    import os
    
    url='http://turintur.dynu.com/db' 
    filenameTemp = 'temp.json'
    filename = 'db.json'
    timestamp = time.time()
    st = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    filenameBackup = './backups/' + filename[:-5] + ' backup ' + st + '.json'
    
    print ('Starting download, please wait')
    
    # Bajamos el archivo 
    urllib.request.urlretrieve(url, filenameTemp)


    # Renombramos el archivo viejo y dejamos el descargado con el nombre que corresponde si se descargo bien
    if os.path.isfile(filenameTemp):
        if os.path.isfile(filename):
            os.rename(filename,filenameBackup)
        os.rename(filenameTemp,filename)

    print ('Donload finish')

    
def load (settings):
    
    import sys
    if not sys.version_info[:2] == (3, 4):
        print ('Sos un boludo!, pero uno previsor')
        print ('Este codigo esta pensado para correr en python 3.4')
    
    
    import json
    import pandas as pd
    import numpy as np

    filename = 'db.json'

    with open(filename) as data_file:    
        db = json.load(data_file)

    # Voy a armar dos tablas gigantes, una con toda la info de los touchs y otra con toda la info de los sounds

    # Primero cargo la info de la estructura json (los otuchs y sounds vienen dentro de los trials)
    sessions = pd.concat((pd.DataFrame(x) for x in db['SessionEnviables']), ignore_index=True)
    levels = pd.concat((pd.DataFrame(x) for x in db['LevelEnviables']), ignore_index=True)
    trials = pd.concat((pd.DataFrame(x) for x in db['TrialEnviables']), ignore_index=True)
    touchs = pd.concat(pd.DataFrame(x) for x in list(trials['touchLog']) if x is not np.nan)
    sounds = pd.concat(pd.DataFrame(x) for x in list(trials['soundLog']) if x is not np.nan)

    # Borro info innecesaria para procesar los datos
    sessions.drop(['class','idEnvio','status'],inplace=True, axis=1)
    # agregamos un alias para que el nombre de usuario sea amigable
    name_map = {user_id: 'Usr'+str(alias) for alias, user_id in enumerate(sessions['userID'].unique())}
    sessions['Alias'] = sessions['userID'].map(name_map)

    levels.drop(['class','exitTrialId','idEnvio','levelLength','status','trialsVisited','exitTrialPosition','idUser','sortOfTrials','startTrialPosition'],inplace=True, axis=1)
    trials.drop(['class','distribucionEnPantalla','idEnvio','indexOfTrialInLevel','resourcesIdSelected','status','trialExitRecorded','trialsInLevel','userId','sessionId','soundLog','touchLog','timeInTrial','timeStopTrialInLevel','resourcesVersion'],inplace=True, axis=1)
    touchs.drop(['levelInstance','numberOfSoundLoops','sessionInstance','soundIdSecuenceInTrial','soundInstance','soundRunning','timeLastStartSound','timeSinceTrialStarts','tipoDeTrial','trialId','timeLastStopSound'],inplace=True, axis=1)
    # Para el sonidos solo extraigo lo que necesito
    sounds = sounds[['trialInstance','soundId','soundInstance']]


    # Renombre cosas para que sea mas facil de identificar despues
    sessions.rename(columns={'id':'sessionInstance'}, inplace=True)
    levels.rename(columns={'sessionId':'sessionInstance','timeExit':'timeLevelExit','timeStarts':'timeLevelStarts'}, inplace=True)
    trials.rename(columns={'timeExitTrial':'timeTrialExit'}, inplace=True)
    touchs.rename(columns={'categorias':'categoriasTouched'}, inplace=True)
    sounds.rename(columns={'soundId':'soundSourceId'}, inplace=True)


    # Con toda la info ya en tablas bien nombradas mergeo

    touchs = pd.merge(touchs, trials, on='trialInstance')
    touchs = pd.merge(touchs, levels, on='levelInstance')
    touchs = pd.merge(touchs, sessions, on='sessionInstance')

    sounds = pd.merge(sounds, trials, on='trialInstance')
    sounds = pd.merge(sounds, levels, on='levelInstance')
    sounds = pd.merge(sounds, sessions, on='sessionInstance')
    
    #Filtramos ahora por version del codigo:
    if settings['FilterCodeVersion'] != 0:
        touchs = touchs[touchs['codeVersion']==settings['FilterCodeVersion']]
        sounds = sounds[sounds['codeVersion']==settings['FilterCodeVersion']]
    
    if settings['FilterLevelVersion'] != 0:
        touchs = touchs[touchs['levelVersion']==settings['FilterLevelVersion']]
        sounds = sounds[sounds['levelVersion']==settings['FilterLevelVersion']]
    
    if settings['FilterResourcesVersion'] != 0:
        touchs = touchs[touchs['resourcesVersion']==settings['FilterResourcesVersion']]
        sounds = sounds[sounds['resourcesVersion']==settings['FilterResourcesVersion']]
        
    print ('recursos cargados del archivo')
    return touchs, sounds
    
    
    
    
def makeTimeline (touchs, sounds):

    import sys
    if not sys.version_info[:2] == (3, 4):
        print ('Sos un boludo!, pero uno previsor')
        print ('Este codigo esta pensado para correr en python 3.4')
    
    import matplotlib.pyplot as plt
    import numpy as np
    import datetime
    from Scripts import fechaLocal

    juntar = False # Si es true, junta todos los levels de una misma sesion, sino separa por level

    for usuario in touchs['Alias'].unique():
        # Genera el plot
        fig = plt.figure(figsize=(30,5))

        ax = fig.add_subplot(111)
        ax.set_title('Informacion de eventos para el usuario {}'.format(usuario), fontsize=10, fontweight='bold')
        ax.set_xlabel('Tiempo')
        ax.set_ylabel('')
        ax.get_yaxis().set_ticks([])
        ax.set_ylim([0,11])



        # Procesa la info para graficar las sesiones del usuario
        fechas = touchs[touchs['Alias']==usuario]['sessionInstance']
        fechasFormateadas = [fechaLocal(fecha) for fecha in fechas]
        altura = np.ones(fechas.size)*10
        ax.plot(fechasFormateadas,altura,'ro')

        touchsUsuario = touchs[touchs['Alias'] == usuario]
        soundsUsuario = sounds[sounds['Alias'] == usuario]

        # ahora para este usuario va a hacer un grafico por sesion
        for session in touchsUsuario['sessionInstance'].unique():

            #Carga los touchs de cada session
            touchsSession = touchsUsuario[touchsUsuario['sessionInstance']==session]
            soundsSession = soundsUsuario[soundsUsuario['sessionInstance']==session]

            if juntar: #Crea un grafico nuevo si esta configurado asi
                if touchsSession.size > 0:
                    # Genera el plot si se va a usar
                    fig = plt.figure(figsize=(30,5))
                    ax = fig.add_subplot(111)
                    ax.set_title('Informacion de eventos para el usuario '+str(usuario)+' sesion del '+str(fechaLocal(touchSession)), fontsize=14, fontweight='bold')
                    ax.set_xlabel('Tiempo')
                    ax.set_ylabel('')
                    ax.get_yaxis().set_ticks([])
                    ax.set_ylim([0,11])
         
            # Procesa la info de los levels
            for level in touchsSession['levelInstance'].unique():

                touchsLevel = touchsSession[touchsSession['levelInstance']==level]
                soundsLevel = soundsSession[soundsSession['levelInstance']==level]
                levelInfo = touchsLevel.iloc[0]

                if not juntar: #Crea un grafico nuevo si esta configurado asi
                    # Genera el plot si se va a usar
                    fig = plt.figure(figsize=(30,5))
                    ax = fig.add_subplot(111)
                    ax.set_title('Informacion de eventos para el usuario '+str(usuario)+', sesion del '+str(fechaLocal(session))+', nivel: '+str(levelInfo['levelId']), fontsize=14, fontweight='bold')
                    ax.set_xlabel('Tiempo')
                    ax.set_ylabel('')
                    ax.get_yaxis().set_ticks([])
                    ax.set_ylim([0,11])

                # Configura el color segun este completado o no el nivel
                if levelInfo['levelCompleted'] == True:
                    color = 'blue'
                else:
                    color = 'red'

                # Grafica el segmento principal
                x = [fechaLocal(levelInfo['timeLevelStarts']),fechaLocal(levelInfo['timeLevelExit'])]
                y = [9,9]
                ax.plot(x,y,color=color)
                # Grafica dos bordes para remarcar los inicios y los finales
                ax.plot([fechaLocal(levelInfo['timeLevelStarts']-0.01),fechaLocal(levelInfo['timeLevelStarts']+0.01)],[y[0]+0.5,y[0]-0.5],color=color)
                ax.plot([fechaLocal(levelInfo['timeLevelExit']-0.01),fechaLocal(levelInfo['timeLevelExit']+0.01)],[y[0]+0.5,y[0]-0.5],color=color)

                # Agrega el id del nivel
                xCenter = fechaLocal((levelInfo['timeLevelStarts']+levelInfo['timeLevelExit'])/2)
                ax.text(xCenter, 8.5, levelInfo['levelInstance'])


                # Procesa la info de los trials del level en cuestion
                for trial in touchsLevel['trialInstance'].unique():

                    touchsTrial = touchsLevel[touchsLevel['trialInstance']==trial]
                    soundsTrial = soundsLevel[soundsLevel['trialInstance']==trial]

                    trialInfo = touchsTrial.iloc[0]

                    # Configura el color segun el tipo de trial
                    if trialInfo['tipoDeTrial'] == 'TUTORIAL':
                        color = 'yellow'
                    else:
                        color = 'cyan'

                    # Grafica el segmento principal
                    x = [fechaLocal(trialInfo['timeTrialStart']),fechaLocal(trialInfo['timeTrialExit'])]
                    y = [7,7]
                    ax.plot(x,y,color=color)
                    # Grafica dos bordes para remarcar los inicios y los finales
                    ax.plot([fechaLocal(trialInfo['timeTrialStart']-0.01),fechaLocal(trialInfo['timeTrialStart']+0.01)],[y[0]+0.5,y[0]-0.5],color=color)
                    ax.plot([fechaLocal(trialInfo['timeTrialExit']-0.01),fechaLocal(trialInfo['timeTrialExit']+0.01)],[y[0]+0.5,y[0]-0.5],color=color)
                    # Agrega el id del trial
                    xCenter = fechaLocal ((trialInfo['timeTrialStart']+trialInfo['timeTrialExit'])/2)
                    ax.text(xCenter, 6.5, trialInfo['trialId'])

                    # Procesa la info de los touchs del trial en cuestion 
                    for touchInstance in touchsTrial['touchInstance'].unique():
                        touch = touchsTrial[touchsTrial['touchInstance']==touchInstance]
                        touch = touch.iloc[0]

                        # Configura el color segun sea un acierto o no
                        if touch['isTrue'] == True: # Ojo que aca un Nan es un false!
                            color = 'green'
                        else:
                            color = 'red'
                            

                        y = [3,3]
                        # Grafica el segmento cuasivertical
                        ax.plot([fechaLocal(touch['touchInstance']-0.01),fechaLocal(touch['touchInstance']+0.01)],[y[0]+0.5,y[0]-0.5],color=color)
                        # Agrega el id del elemento tocado
                        xCenter = fechaLocal(touch['touchInstance']+0.3)
                        ax.text(xCenter, 2.5, touch['idResourceTouched']['id'])


                    # Procesa los sounds en cada trial
                    for soundInstance in soundsTrial['soundInstance'].unique():

                        sound = soundsTrial[soundsTrial['soundInstance']==soundInstance]
                        sound = sound.iloc[0]

                        # Configura el color
                        color = 'gray'
                        y = [5,5]
                        # Grafica el segmento cuasivertical
                        ax.plot([fechaLocal(soundInstance-0.01),fechaLocal(soundInstance+0.01)],[y[0]+0.5,y[0]-0.5],color=color)
                        # Agrega el id del elemento tocado
                        xCenter = fechaLocal(soundInstance+0.3)
                        ax.text(xCenter, 4.5, sound['soundSourceId']['id'])
    
def loadUmbral (settings):
    
    import sys
    if not sys.version_info[:2] == (3, 4):
        print ('Sos un boludo!, pero uno previsor')
        print ('Este codigo esta pensado para correr en python 3.4')
    
    
    import json
    import pandas as pd
    import numpy as np

    filename = 'db.json'

    with open(filename) as data_file:    
        db = json.load(data_file)

    # Voy a armar dos tablas gigantes, una con toda la info de los touchs y otra con toda la info de los sounds

    # Primero cargo la info de la estructura json (los otuchs y sounds vienen dentro de los trials)
    sessions = pd.concat((pd.DataFrame(x) for x in db['SessionEnviables']), ignore_index=True)
    levels = pd.concat((pd.DataFrame(x) for x in db['LevelEnviables']), ignore_index=True)
    trials = pd.concat((pd.DataFrame(x) for x in db['TrialEnviables']), ignore_index=True)
    touchs = pd.concat(pd.DataFrame(x) for x in list(trials['touchLog']) if x is not np.nan)
    sounds = pd.concat(pd.DataFrame(x) for x in list(trials['soundLog']) if x is not np.nan)

    # Borro info innecesaria para procesar los datos
    sessions.drop(['class','idEnvio','status'],inplace=True, axis=1)
    # agregamos un alias para que el nombre de usuario sea amigable
    name_map = {user_id: 'Usr'+str(alias) for alias, user_id in enumerate(sessions['userID'].unique())}
    sessions['Alias'] = sessions['userID'].map(name_map)

    levels.drop(['class','exitTrialId','idEnvio','levelLength','status','trialsVisited','exitTrialPosition','idUser','sortOfTrials','startTrialPosition'],inplace=True, axis=1)
    trials.drop(['class','distribucionEnPantalla','idEnvio','indexOfTrialInLevel','resourcesIdSelected','status','trialExitRecorded','trialsInLevel','userId','sessionId','soundLog','touchLog','timeInTrial','timeStopTrialInLevel','resourcesVersion'],inplace=True, axis=1)
    touchs.drop(['levelInstance','numberOfSoundLoops','sessionInstance','soundIdSecuenceInTrial','soundInstance','soundRunning','timeLastStartSound','timeSinceTrialStarts','tipoDeTrial','trialId','timeLastStopSound'],inplace=True, axis=1)
    # Para el sonidos solo extraigo lo que necesito
    sounds = sounds[['trialInstance','soundId','soundInstance']]


    # Renombre cosas para que sea mas facil de identificar despues
    sessions.rename(columns={'id':'sessionInstance'}, inplace=True)
    levels.rename(columns={'sessionId':'sessionInstance','timeExit':'timeLevelExit','timeStarts':'timeLevelStarts'}, inplace=True)
    trials.rename(columns={'timeExitTrial':'timeTrialExit'}, inplace=True)
    touchs.rename(columns={'categorias':'categoriasTouched'}, inplace=True)
    sounds.rename(columns={'soundId':'soundSourceId'}, inplace=True)


    # Con toda la info ya en tablas bien nombradas mergeo

    touchs = pd.merge(touchs, trials, on='trialInstance')
    touchs = pd.merge(touchs, levels, on='levelInstance')
    touchs = pd.merge(touchs, sessions, on='sessionInstance')

    sounds = pd.merge(sounds, trials, on='trialInstance')
    sounds = pd.merge(sounds, levels, on='levelInstance')
    sounds = pd.merge(sounds, sessions, on='sessionInstance')
    
    #Filtramos ahora por version del codigo:
    if settings['FilterCodeVersion'] != 0:
        touchs = touchs[touchs['codeVersion']==settings['FilterCodeVersion']]
        sounds = sounds[sounds['codeVersion']==settings['FilterCodeVersion']]
    
    if settings['FilterLevelVersion'] != 0:
        touchs = touchs[touchs['levelVersion']==settings['FilterLevelVersion']]
        sounds = sounds[sounds['levelVersion']==settings['FilterLevelVersion']]
    
    if settings['FilterResourcesVersion'] != 0:
        touchs = touchs[touchs['resourcesVersion']==settings['FilterResourcesVersion']]
        sounds = sounds[sounds['resourcesVersion']==settings['FilterResourcesVersion']]
        
    print ('recursos cargados del archivo')
    return touchs, sounds
    

def loadUmbralLocal (settings):
    
    import sys
    if not sys.version_info[:2] == (3, 4):
        print ('Sos un boludo!, pero uno previsor')
        print ('Este codigo esta pensado para correr en python 3.4')
        
    import pandas as pd
    import numpy as np
    import os

    # Voy a armar dos tablas gigantes, una con toda la info de los touchs y otra con toda la info de los sounds

    # Primero cargo la info de la estructura json (los otuchs y sounds vienen dentro de los trials)
    if os.path.isfile('./Guardados/db.sessions'):
        sessions = pd.read_pickle ('./Guardados/db.sessions')        
    else:
        display ('Warning: no se encontro los session buscados')
        return
        
    if os.path.isfile('./Guardados/db.levels'):
        levels = pd.read_pickle ('./Guardados/db.levels')
    else:
        display ('Warning: no se encontro los levels buscados')
        return
            
    if os.path.isfile('./Guardados/db.trials'):
        trials = pd.read_pickle ('./Guardados/db.trials')
    else:
        display ('Warning: no se encontro los trials buscados')
        return
    
    prueba = pd.DataFrame(trials.iloc[0]['touchsLog'])
    display (prueba)
    touchs = pd.concat(pd.DataFrame(x) for x in trials['touchLog'].tolist() if x is not np.nan)
    sounds = pd.concat(pd.DataFrame(x) for x in trials['soundLog'].tolist() if x is not np.nan)

    # Borro info innecesaria para procesar los datos
    sessions.drop(['class','idEnvio','status'],inplace=True, axis=1)
    # agregamos un alias para que el nombre de usuario sea amigable
    name_map = {user_id: 'Usr'+str(alias) for alias, user_id in enumerate(sessions['userID'].unique())}
    sessions['Alias'] = sessions['userID'].map(name_map)

    levels.drop(['class','exitTrialId','idEnvio','levelLength','status','trialsVisited','exitTrialPosition','idUser','sortOfTrials','startTrialPosition'],inplace=True, axis=1)
    trials.drop(['class','distribucionEnPantalla','idEnvio','indexOfTrialInLevel','resourcesIdSelected','status','trialExitRecorded','trialsInLevel','userId','sessionId','soundLog','touchLog','timeInTrial','timeStopTrialInLevel','resourcesVersion'],inplace=True, axis=1)
    touchs.drop(['levelInstance','numberOfSoundLoops','sessionInstance','soundIdSecuenceInTrial','soundInstance','soundRunning','timeLastStartSound','timeSinceTrialStarts','tipoDeTrial','trialId','timeLastStopSound'],inplace=True, axis=1)
    # Para el sonidos solo extraigo lo que necesito
    sounds = sounds[['trialInstance','soundId','soundInstance']]


    # Renombre cosas para que sea mas facil de identificar despues
    sessions.rename(columns={'id':'sessionInstance'}, inplace=True)
    levels.rename(columns={'sessionId':'sessionInstance','timeExit':'timeLevelExit','timeStarts':'timeLevelStarts'}, inplace=True)
    trials.rename(columns={'timeExitTrial':'timeTrialExit'}, inplace=True)
    touchs.rename(columns={'categorias':'categoriasTouched'}, inplace=True)
    sounds.rename(columns={'soundId':'soundSourceId'}, inplace=True)


    # Con toda la info ya en tablas bien nombradas mergeo

    touchs = pd.merge(touchs, trials, on='trialInstance')
    touchs = pd.merge(touchs, levels, on='levelInstance')
    touchs = pd.merge(touchs, sessions, on='sessionInstance')

    sounds = pd.merge(sounds, trials, on='trialInstance')
    sounds = pd.merge(sounds, levels, on='levelInstance')
    sounds = pd.merge(sounds, sessions, on='sessionInstance')
    
    #Filtramos ahora por version del codigo:
    if settings['FilterCodeVersion'] != 0:
        touchs = touchs[touchs['codeVersion']==settings['FilterCodeVersion']]
        sounds = sounds[sounds['codeVersion']==settings['FilterCodeVersion']]
    
    if settings['FilterLevelVersion'] != 0:
        touchs = touchs[touchs['levelVersion']==settings['FilterLevelVersion']]
        sounds = sounds[sounds['levelVersion']==settings['FilterLevelVersion']]
    
    if settings['FilterResourcesVersion'] != 0:
        touchs = touchs[touchs['resourcesVersion']==settings['FilterResourcesVersion']]
        sounds = sounds[sounds['resourcesVersion']==settings['FilterResourcesVersion']]
        
    print ('recursos cargados del archivo')
    return touchs, sounds


def guardarPickle (touchs, sounds, filename):
    import pandas as pd
    import os
    from IPython.display import display
    
    import sys
    if not sys.version_info[:2] == (3, 4):
        print ('Sos un boludo!, pero uno previsor')
        print ('Este codigo esta pensado para correr en python 3.4')
        
    if os.path.isfile('./Guardados/'+filename+'.touch'):
        display ('Ya existe una base de datos con ese nombre')
    else:
        display ('Archivo guardado')
        touchs.to_pickle('./Guardados/'+filename+'.touch')
        sounds.to_pickle('./Guardados/'+filename+'.sounds')

def cargarPickle (filename):
    import pandas as pd
    import os
    from IPython.display import display
    
    import sys
    if not sys.version_info[:2] == (3, 4):
        print ('Sos un boludo!, pero uno previsor')
        print ('Este codigo esta pensado para correr en python 3.4')
        
    if os.path.isfile('./Guardados/'+filename+'.touch'):
        touchs = pd.read_pickle ('./Guardados/'+filename+'.touch')
    else:
        display ('Error, no se encontro los touchs buscados')
        return
        
    if os.path.isfile('./Guardados/'+filename+'.sounds'):
        sounds = pd.read_pickle ('./Guardados/'+filename+'.touch')
    else:
        display ('Error, no se encontro los sounds buscados')
        return
        
    return touchs, sounds    
    
    
def join ():
    """ 
    Este codigo sirve para ir acumulando los datos brutos tal cual salen de la base datos que se descarga, de forma de poder limpiar y reducir el tamaño del archivo online mas o menos seguid
    sin perder la coherencia de los datos. Esto es necesario porque el json-server no se banca bien manejar archivos muy grandes (empieza a tener delay) y el volumen de datos que se genera crece rapido.
    """
    import sys
    if not sys.version_info[:2] == (3, 4):
        print ('Sos un boludo!, pero uno previsor')
        print ('Este codigo esta pensado para correr en python 3.4')
    
    import json
    import pandas as pd
    import numpy as np
    import os

    filename = 'db.json'

    with open(filename) as data_file:    
        db = json.load(data_file)

    sessionsNuevos = pd.concat((pd.DataFrame(x) for x in db['SessionEnviables']), ignore_index=True)
    levelsNuevos = pd.concat((pd.DataFrame(x) for x in db['LevelEnviables']), ignore_index=True)
    trialsNuevos = pd.concat((pd.DataFrame(x) for x in db['TrialEnviables']), ignore_index=True)
    
    if os.path.isfile('./Guardados/db.sessions'):
        sessions = pd.read_pickle ('./Guardados/db.sessions')
        sessionsExists = True
        display ('Sessions tiene '+str(sessions.index.size)+' entradas')
    else:
        display ('Warning: no se encontro los session buscados')
        sessionsExists = False
        
    if os.path.isfile('./Guardados/db.levels'):
        levels = pd.read_pickle ('./Guardados/db.levels')
        levelsExists = True
        display ('Levels tiene '+str(levels.index.size)+' entradas')
    else:
        display ('Warning: no se encontro los levels buscados')
        levelsExists = False
            
    if os.path.isfile('./Guardados/db.trials'):
        trials = pd.read_pickle ('./Guardados/db.trials')
        trialsExists = True
        display ('Trials tiene '+str(trials.index.size)+' entradas')
    else:
        display ('Warning: no se encontro los trials buscados')
        trialsExists = False
    
    contador = 0
    if sessionsNuevos.index.size > 0:
        if sessionsExists:
            for index, row in sessionsNuevos.iterrows():
                if not row['id'] in sessions['id'].tolist():
                    sessions = pd.concat([sessions, sessionsNuevos.iloc[index]], axis=0, ignore_index=True)
                    contador = contador + 1
        else:
            sessions = sessionsNuevos
            display ('Se ha creado una nueva lista de sessiones')

    display ('Se agregaron '+str(contador)+' registros al registro de sesiones')
    sessions.to_pickle('./Guardados/db.sessions')
    
    contador = 0
    if levelsNuevos.index.size > 0:
        if levelsExists:
            for index, row in levelsNuevos.iterrows():
                if not row['levelInstance'] in levels['levelInstance'].tolist():
                    levels = pd.concat([levels, levelsNuevos.iloc[index]], axis=0, ignore_index=True)
                    contador = contador + 1
        else:
            levels = levelsNuevos
            display ('Se ha creado una nueva lista de levels')

    display ('Se agregaron '+str(contador)+' registros al registro de niveles')
    levels.to_pickle('./Guardados/db.levels')
    
    contador = 0
    if trialsNuevos.index.size > 0:
        if trialsExists:
            for index, row in trialsNuevos.iterrows():
                if not row['trialInstance'] in trials['trialInstance'].tolist():
                    trials = pd.concat([trials, trialsNuevos.iloc[index]], axis=0, ignore_index=True)
                    contador = contador + 1
        else:
            trials = trialsNuevos
            display ('Se ha creado una nueva lista de trials')
    
    display ('Se agregaron '+str(contador)+' registros al registro de trials')
    trials.to_pickle('./Guardados/db.trials')
        
    

    
    
    
    
    
    
    
    
    
    