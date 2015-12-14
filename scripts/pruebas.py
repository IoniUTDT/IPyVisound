

def prueba():

    from IPython.display import display

    display ("Hola! Esto esta modificado.")


def load (filtrarDatos='estandar', levelVersion=0, resourcesVersion=0, codeVersion=0):

    """
    Esta funcion extrae de la base de datos ya separada en registros de sesion,
    level y trials, y acumulada en archivos locales en formato json dos
    dataframes uno para touchs y uno para sounds. Para eso mergea los sub json
    que hay en la db.json del servidor unificando por instancias de level,
    sesion y trial.
    Los formatos en que se guardan los json que vienen de la aplicacion
    resultaron ser muy poco practicos por esa razon es importante reordenarlos.
    La funcion recibe como parametros un dict settings, que le indica que
    filtros utilizar para leer los datos y evitar problemas de compatibilidad
    entre experimentos, versiones de datos, etc.
    La funcion devuelve dos dataframes uno de touchs y uno de sounds que son la
    base de la estructura de datos para procesamientos posteriores.
    """

    import sys
    if not sys.version_info[:2] == (3, 4):
        print ('Sos un boludo!, pero uno previsor')
        print ('Este codigo esta pensado para correr en python 3.4')

    import pandas as pd
    import os
    import numpy as np
    from IPython.display import display
    import math

    # Se arman archivos de configuracion
    filtros = {}
    if filtrarDatos == 'estandar':
        filtros['sessions']=['class','idEnvio','status']
        filtros['levels']=['class','exitTrialId','idEnvio','levelLength','status','trialsVisited','exitTrialPosition','idUser','sortOfTrials','startTrialPosition']
        filtros['trials']=['class','distribucionEnPantalla','idEnvio','indexOfTrialInLevel','resourcesIdSelected','status','trialExitRecorded','trialsInLevel','userId','sessionId','soundLog','touchLog','timeInTrial','timeStopTrialInLevel','resourcesVersion', 0]
        filtros['touchs']=['levelInstance','numberOfSoundLoops','sessionInstance','soundIdSecuenceInTrial','soundInstance','soundRunning','timeLastStartSound','timeSinceTrialStarts','tipoDeTrial','trialId','timeLastStopSound']
        filtros['sounds']=['categorias', 'fromStimuli', 'levelInstance', 'numberOfLoop', 'numberOfSoundInTrial', 'soundSecuenceInTrial', 'startTimeSinceTrial', 'stopByEnd', 'stopByExit', 'stopByUnselect', 'stopTime', 'tipoDeTrial', 'trialId', 'sessionInstance']

    renames = {}
    if filtrarDatos == 'estandar':
        renames['sessions'] = {'id':'sessionInstance'}
        renames['levels'] = {'sessionId':'sessionInstance','timeExit':'timeLevelExit','timeStarts':'timeLevelStarts'}
        renames['trials'] = {'timeExitTrial':'timeTrialExit'}
        renames['touchs'] = {'categorias':'categoriasTouched'}
        renames['sounds'] = {'soundId':'soundSourceId'}

    listaUsuarios = {1449524935331:'Usuario1'}

    # Primero se carga la info de la estructura json (los touchs y sounds vienen dentro de los trials)
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

    display ('Numero de sesiones cargadas: ' + str(sessions.index.size))
    display ('Numero de sesiones levels: ' + str(levels.index.size))
    display ('Numero de sesiones trials: ' + str(trials.index.size))

    # Extraemos los datos de los touchs y sounds de dentro de los json de los trials
    touchs = pd.concat(pd.DataFrame(x) for x in list(trials['touchLog']) if type(x)==list) # NOTA! : revisar que pasa si vienen mas de un json en un trial
    sounds = pd.concat(pd.DataFrame(x) for x in list(trials['soundLog']) if type(x)==list) # NOTA! : revisar que pasa si vienen mas de un json en un trial


    # Procesamos un poco los datos para eliminar info redundante o innecesaria, o para unificar nombres. Para eso se usan los filtros prefijados y configurables.
    for column in sessions.columns:
        if column in renames['sessions'].keys():
            sessions.rename(columns={column:renames['sessions'][column]}, inplace=True)
        if column in filtros['sessions']:
            sessions.drop([column],inplace=True,axis=1)
    for column in levels.columns:
        if column in renames['levels'].keys():
            levels.rename(columns={column:renames['levels'][column]}, inplace=True)
        if column in filtros['levels']:
            levels.drop([column],inplace=True,axis=1)
    for column in trials.columns:
        if column in renames['trials'].keys():
            trials.rename(columns={column:renames['trials'][column]}, inplace=True)
        if column in filtros['trials']:
            trials.drop([column],inplace=True,axis=1)
    for column in touchs.columns:
        if column in renames['touchs'].keys():
            touchs.rename(columns={column:renames['touchs'][column]}, inplace=True)
        if column in filtros['touchs']:
            touchs.drop([column],inplace=True,axis=1)
    for column in sounds.columns:
        if column in renames['sounds'].keys():
            sounds.rename(columns={column:renames['sounds'][column]}, inplace=True)
        if column in filtros['sounds']:
            sounds.drop([column],inplace=True,axis=1)

    # una vez bien formateada todas las tablas se mergean a travez de las instancias de sesion, level y trial

    touchs = pd.merge(touchs, trials, on='trialInstance')
    touchs = pd.merge(touchs, levels, on='levelInstance')
    touchs = pd.merge(touchs, sessions, on='sessionInstance')
    sounds = pd.merge(sounds, trials, on='trialInstance')
    sounds = pd.merge(sounds, levels, on='levelInstance')
    sounds = pd.merge(sounds, sessions, on='sessionInstance')

    # Agregamos los alias para identificar a los usuarios.
    touchs['Alias'] = touchs['userID'].map(listaUsuarios)
    sounds['Alias'] = sounds['userID'].map(listaUsuarios)
    # Completamos los usuarios sin dato con el userID
    touchs.Alias.fillna(touchs.userID, inplace=True)
    sounds.Alias.fillna(sounds.userID, inplace=True)

    #Filtramos ahora por version del codigo:
    if not codeVersion == 0:
        touchs = touchs[touchs['codeVersion']==codeVersion]
        sounds = sounds[sounds['codeVersion']==codeVersion]

    if not levelVersion == 0:
        touchs = touchs[touchs['levelVersion']==levelVersion]
        sounds = sounds[sounds['levelVersion']==levelVersion]

    if not resourcesVersion == 0:
        touchs = touchs[touchs['resourcesVersion']==resourcesVersion]
        sounds = sounds[sounds['resourcesVersion']==resourcesVersion]

    print ('recursos cargados del archivo')
    return touchs, sounds

"""
    # agregamos un alias para que el nombre de usuario sea amigable
    name_map = {user_id: 'Usr'+str(alias) for alias, user_id in enumerate(sessions['userID'].unique())}
    sessions['Alias'] = sessions['userID'].map(name_map)
"""
