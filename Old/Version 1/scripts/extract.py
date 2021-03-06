def downloadFile ():

    """
        Esta funcion descarga la base de datos en formato json del servidor y hace una backup del archivo anterior.
    """

    import datetime
    import time
    import urllib
    import os

    from scripts.general import chkVersion
    chkVersion()

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


def join (filename='db.json'):

    from scripts.general import chkVersion
    chkVersion()

    """
    Este codigo sirve para ir acumulando los datos brutos tal cual salen de la base datos que se descarga, de forma de poder limpiar y reducir el tamaño del archivo online mas o menos seguid
    sin perder la coherencia de los datos. Esto es necesario porque el json-server no se banca bien manejar archivos muy grandes (empieza a tener delay) y el volumen de datos que se genera crece rapido.

    """
    from IPython.display import display
    import json
    import pandas as pd
    import numpy as np
    import os

    with open(filename) as data_file:
        db = json.load(data_file)

    if db['SessionEnviables']!=[]:
        sessionsNuevos = pd.concat((pd.DataFrame(x) for x in db['SessionEnviables']), ignore_index=True)

        if os.path.isfile('./Guardados/db.sessions'):
            sessions = pd.read_pickle ('./Guardados/db.sessions')
            sessionsExists = True
            display ('Sessions tiene '+str(sessions.index.size)+' entradas')
        else:
            display ('Warning: no se encontro los session buscados')
            sessionsExists = False

        if sessionsExists:
            sessionsJoin = pd.concat([sessions, sessionsNuevos], axis=0, ignore_index=True)
            sessionsJoin.drop_duplicates(cols='id', inplace=True)
            display ('Se agregaron '+ str(sessionsJoin.index.size - sessions.index.size)+' registros al registro de sesiones.')
        else:
            sessionsJoin = sessionsNuevos
            display ('Se creo un archivo nuevo con registro de sesiones')

        sessionsJoin.to_pickle('./Guardados/db.sessions')

    if db['LevelEnviables']!=[]:
        levelsNuevos = pd.concat((pd.DataFrame(x) for x in db['LevelEnviables']), ignore_index=True)

        if os.path.isfile('./Guardados/db.levels'):
            levels = pd.read_pickle ('./Guardados/db.levels')
            levelsExists = True
            display ('Levels tiene '+str(levels.index.size)+' entradas')
        else:
            display ('Warning: no se encontro los levels buscados')
            levelsExists = False

        if levelsExists:
            levelsJoin = pd.concat([levels, levelsNuevos], axis=0, ignore_index=True)
            levelsJoin.drop_duplicates(cols='levelInstance', inplace=True)
            display ('Se agregaron '+ str(levelsJoin.index.size - levels.index.size)+' registros al registro de levels.')
        else:
            levelsJoin = levelsNuevos
            display ('Se creo un archivo nuevo con registro de levels')

        levelsJoin.to_pickle('./Guardados/db.levels')

    if db['TrialEnviables']!=[]:
        trialsNuevos = pd.concat((pd.DataFrame(x) for x in db['TrialEnviables']), ignore_index=True)

        if os.path.isfile('./Guardados/db.trials'):
            trials = pd.read_pickle ('./Guardados/db.trials')
            trialsExists = True
            display ('Trials tiene '+str(trials.index.size)+' entradas')
        else:
            display ('Warning: no se encontro los trials buscados')
            trialsExists = False

        if trialsExists:
            trialsJoin = pd.concat([trials, trialsNuevos], axis=0, ignore_index=True)
            trialsJoin.drop_duplicates(cols='trialInstance', inplace=True)
            display ('Se agregaron '+ str(trialsJoin.index.size - trials.index.size)+' registros al registro de trials.')
        else:
            trialsJoin = trialsNuevos
            display ('Se creo un archivo nuevo con registro de trials')

        trialsJoin.to_pickle('./Guardados/db.trials')

    display ('Datos del json cargados')


def loadLevels ():
    """
        Esta funcion carga la info de las sesiones y levels pero sin cargar la de los trials y touchs. Sirve para cuando
        la info ya viene preprocesada en el programa online. Por ejemplo los analisis de umbral.
    """
    import os
    import pandas as pd

    from scripts.settings import makeSettings
    from scripts.general import chkVersion
    chkVersion()

    makeSettings(basic=True,levels=True)


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

    sessions = estetizarTabla(sessions,'sessions')
    levels = estetizarTabla(levels,'levels')

    levels = pd.merge(levels, sessions, on='sessionInstance')

    # Creamos los alias
    levels = renombrarUsuarios(levels)
    # Aplicamos los filtros level, code, etc
    levels = aplicarFiltros(levels)


    return levels


def loadTouchs ():

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

    from scripts.general import chkVersion
    chkVersion()

    import pandas as pd
    import os
    import numpy as np
    from IPython.display import display

    makeSettings(basic=True,levels=False)

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

    display ('Numero de sesiones totales encontradas:: ' + str(sessions.index.size))
    display ('Numero de levels totales encontrados: ' + str(levels.index.size))

    if os.path.isfile('./Guardados/db.trials'):
        trials = pd.read_pickle ('./Guardados/db.trials')
    else:
        display ('Warning: no se encontro los trials buscados')
        return

    display ('Numero de sesiones totales encontradas:: ' + str(sessions.index.size))
    display ('Numero de levels totales encontrados: ' + str(levels.index.size))
    display ('Numero de trials totales encontrados: ' + str(trials.index.size))
    display ('Filtrando datos...')

    # Extraemos los datos de los touchs y sounds de dentro de los json de los trials
    touchs = pd.concat(pd.DataFrame(x) for x in list(trials['touchLog']) if type(x)==list) # NOTA! : revisar que pasa si vienen mas de un json en un trial
    sounds = pd.concat(pd.DataFrame(x) for x in list(trials['soundLog']) if type(x)==list) # NOTA! : revisar que pasa si vienen mas de un json en un trial


    # Procesamos un poco los datos para eliminar info redundante o innecesaria, o para unificar nombres. Para eso se usan los filtros prefijados y configurables.
    sessions = estetizarTabla(sessions,'sessions')
    levels = estetizarTabla(levels,'levels')
    trials = estetizarTabla(trials,'trials')
    touchs = estetizarTabla(touchs,'touchs')
    sounds = estetizarTabla(sounds,'sounds')

    # una vez bien formateada todas las tablas se mergean a travez de las instancias de sesion, level y trial

    touchs = pd.merge(touchs, trials, on='trialInstance')
    touchs = pd.merge(touchs, levels, on='levelInstance')
    touchs = pd.merge(touchs, sessions, on='sessionInstance')
    sounds = pd.merge(sounds, trials, on='trialInstance')
    sounds = pd.merge(sounds, levels, on='levelInstance')
    sounds = pd.merge(sounds, sessions, on='sessionInstance')

    # Creamos los alias
    touchs = renombrarUsuarios(touchs)
    sounds = renombrarUsuarios(sounds)
    # Aplicamos los filtros level, code, etc
    touchs = aplicarFiltros(touchs)
    sounds = aplicarFiltros(sounds)

    display ('Recursos cargados del archivo')
    display ('Touchs seleccionados: ' + str(touchs.index.size))
    display ('Sounds seleccionados: ' + str(sounds.index.size))
    return touchs, sounds


def recreateDb ():
    """
        Funcion que reconstruye la base de datos acumulada en el tiempo a partir de los archivos de backup
    """
    from scripts.general import chkVersion
    chkVersion()

    from scripts.extract import join
    from IPython.display import display
    import glob, os, time
    from os import path
    from datetime import datetime, timedelta

    #os.chdir('/backups/')
    for file in glob.glob("./backups/*.json"):
        display (file)
        fileCreation = datetime.fromtimestamp(path.getctime(file))
        tiempolimite = datetime.now() - timedelta(days=14)
        display (fileCreation > tiempolimite)
        if fileCreation > tiempolimite:
            join(file)

    Display ('FIN!')

def aplicarFiltros (tabla):
    import json
    # Se arman archivos de configuracion
    settings = json.load(open("./Settings/settings"))
    filtros = settings['filtrosxVersion']
    listaUsuarios = settings['listaUsuarios']
    sessionsExcluidas = settings['sessionsExcluidas']
    usersExcluidos = settings['usersExcluidos']

    #Filtramos por usuarios si hay alguno determinado
    if filtros['usuario']:
        if filtros['usuario'] in listaUsuarios.values():
            tabla = tabla[tabla['Alias']==filtros['usuario']]
        else:
            tabla = tabla[tabla['userID']==filtros['usuario']]

    #Filtramos ahora por version del codigo:
    if not filtros['codeVersion'] == 0:
        tabla = tabla[tabla['codeVersion']==filtros['codeVersion']]

    if not filtros['levelVersion'] == 0:
        tabla = tabla[tabla['levelVersion']==filtros['levelVersion']]

    if not filtros['resourcesVersion'] == 0:
        tabla = tabla[tabla['resourcesVersion']==filtros['resourcesVersion']]

    if filtros['filtrarXUsuarioRegistrado']:
        tabla = tabla[tabla['Alias'].isin(list(listaUsuarios.values()))]

    # Excluimos la sessiones o usuarios que no son datos buenos.
    for sessionAExcluir in sessionsExcluidas:
        tabla = tabla[tabla['sessionInstance'] != sessionAExcluir]
    for userAexcluir in usersExcluidos:
        tabla = tabla[tabla['userID'] != userAexcluir]


    return tabla

def renombrarUsuarios (tabla):

    import json
    # Se arman archivos de configuracion
    settings = json.load(open("./Settings/settings"))
    listaUsuarios = settings['listaUsuarios']

    # Agregamos los alias para identificar a los usuarios.
    tabla['Alias'] = tabla['userID'].apply(str).map(listaUsuarios)
    # Completamos los usuarios sin dato con el userID
    tabla.Alias.fillna(tabla.userID, inplace=True)
    tabla['Alias'] = tabla['Alias'].astype(str)
    return tabla

def estetizarTabla (tabla, nombreTabla):

    import json
    # Se arman archivos de configuracion
    settings = json.load(open("./Settings/settings"))
    filtros = settings['filtros']
    renames = settings['renames']

    for column in tabla.columns:
        if column in renames[nombreTabla].keys():
            tabla.rename(columns={column:renames[nombreTabla][column]}, inplace=True)
        if column in filtros[nombreTabla]:
            tabla.drop([column],inplace=True,axis=1)
    return tabla
