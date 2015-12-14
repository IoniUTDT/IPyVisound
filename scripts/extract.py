def DownloadFile ():

    """
        Esta funcion descarga la base de datos en formato json del servidor y hace una backup del archivo anterior.
    """
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


def join ():
    """
    Este codigo sirve para ir acumulando los datos brutos tal cual salen de la base datos que se descarga, de forma de poder limpiar y reducir el tamaño del archivo online mas o menos seguid
    sin perder la coherencia de los datos. Esto es necesario porque el json-server no se banca bien manejar archivos muy grandes (empieza a tener delay) y el volumen de datos que se genera crece rapido.

    NOTA: este script esta a maedio hacer y compatibilizar
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





def load (settings):

    """
        Esta funcion extrae de la base de datos json dos dataframes uno para touchs y uno para sounds. Para eso mergea los sub json que hay en la db.json del servidor unificando por instancias de level, sesion y trial.
        Los formatos en que se guardan los json que vienen de la aplicacion resultaron ser muy poco practicos por esa razon es importante reordenarlos.
        La funcion recibe como parametros un dict settings, que le indica que filtros utilizar para leer los datos y evitar problemas de compatibilidad entre experimentos, versiones de datos, etc.
        La funcion devuelve dos dataframes uno de touchs y uno de sounds que son la base de la estructura de datos para procesamientos posteriores.
    """


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



def loadUmbral (settings):

    """
        Revisar diferencia entre este y el load general. Revisar si no esta obsoleto esto.
    """
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

    """
        Revisar diferencia entre este y el load general. Revisar si no esta obsoleto esto.
    """

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
