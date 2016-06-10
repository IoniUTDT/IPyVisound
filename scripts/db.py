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
    import scripts.constants
    chkVersion()

    """
    Este codigo sirve para ir acumulando los datos brutos tal cual salen de la base datos que se descarga, de forma de poder limpiar y reducir el tamaño del archivo online mas o menos seguido
    sin perder la coherencia de los datos. Esto es necesario porque el json-server no se banca bien manejar archivos muy grandes (empieza a tener delay) y el volumen de datos que se genera crece rapido.

    La idea es que guarda en archivos separados las listas de registros segun la categoria de envio para que despues puedan ser procesados segun corresponda
    """

    from IPython.display import display
    import json
    import os
    import pickle

    # Transformamos el archivo en un json
    with open(filename) as data_file:
        db = json.load(data_file)

    # Seleccionamos los datos
    data = db['Envio']

    # Buscamos la lista de todas las categorias de envios
    tiposDeEnvio = set([envio['tipoDeEnvio'] for envio in data])



    # La info guardada en esta parte esta pensada como una lista de envios segun el tipo
    for tipoDeEnvio in tiposDeEnvio:
        filename = './Guardados/db.' + tipoDeEnvio
        enviosNuevos = [envio for envio in data if envio['tipoDeEnvio'] == tipoDeEnvio]

        # Sacamos el formato json a los envios
        for envio in enviosNuevos:
            envio['contenido'] = json.loads(envio['contenido'])

        if os.path.isfile(filename):
            with open(filename, 'rb') as f:
                enviosViejos = pickle.load(f)
            enviosExists = True
            display (tipoDeEnvio + ' tiene '+str(len(enviosViejos))+' entradas.')
        else:
            display ('Warning: no se encontro entradas previas para ' + tipoDeEnvio + ' se guardaran ' + str(len(enviosNuevos)) + ' entradas nuevas.')
            enviosExists = False

        if enviosExists:
            enviosUnificados = enviosViejos + [envioNuevo for envioNuevo in enviosNuevos if not envioNuevo['instance'] in set([envioViejo['instance'] for envioViejo in enviosViejos])]
        else:
            enviosUnificados = enviosNuevos

        display (tipoDeEnvio + ' paso a tener '+str(len(enviosUnificados))+' entradas.')

        with open(filename, 'wb+') as f:
            pickle.dump(enviosUnificados, f)

    joinUsers()

def joinUsers():

    """
        Esta funcion busca los usuarios nuevos en la lista de sessiones guardadas y compara con la lista de usuarios almacenada en la base de datos alias. Si encuentra que alguno no esta pregunta el alias y si ignorarlo o no y lo incluye
    """
    from IPython.display import display
    import os
    import pickle
    from scripts.constants import PATHALIAS, PATHSESSSION
    from scripts.general import fechaLocal

    filename = PATHSESSSION
    if os.path.isfile(filename):
        with open(filename, 'rb') as f:
            sessiones = pickle.load(f)
    else:
        display ('ERROR! : No se encontro el archivo ' + filename + ' con el registro de las sessiones.')
        return

    newUsersId = set([session['contenido']['userId'] for session in sessiones])

    filename = PATHALIAS

    if os.path.isfile(filename):
        with open(filename, 'rb') as f:
            users= pickle.load(f)
    else:
        users = []

    usersId = [user['id'] for user in users]

    for newUserId in newUsersId:
        if not newUserId in usersId:
            # Creamos el usuario
            newUser = {}
            newUser['id'] = newUserId
            # Preguntamos datos del usuario
            display ('Usuario creado el '+str(fechaLocal(newUser['id'])))
            response = input("Ingrese un alias o enter para continuar:\n")
            if response != "":
                newUser['alias'] = response
            else:
                newUser['alias'] = str(newUser['id'])
            response = input("Presiones 'si' para descartar este usuario del procesamiento de datos:\n")
            if response == "si":
                newUser['ignore'] = True
            else:
                newUser['ignore'] = False
            users = users + [newUser]

    with open(filename, 'wb') as f:
        pickle.dump(users, f)

def updateUser (user):

    """
        Esta funcion sirve para modificar a mano algun usuario en particular
    """
    from IPython.display import display
    import os
    import pickle
    from scripts.constants import PATHALIAS

    filename = PATHALIAS

    if os.path.isfile(filename):
        with open(filename, 'rb') as f:
            users = pickle.load(f)
    else:
        display ('ERROR : No se ha encontrado el archivo ' + filename)
    #display(users)
    #display(type(user))
    if isinstance(user, int):
        for eachuser in users:
            if eachuser['id'] == user:
                display ("Se va a modificar el usuario: " + eachuser['alias'])
                response = input("Ingrese el nuevo alias o presione enter para no cambiarlo:")
                if response != "":
                    eachuser['alias'] = response
                display ("Desea que el usuario " + eachuser['alias'] + " sea ignorado.")
                response = input("(si/NO)")
                if response == "si":
                    eachuser['ignore'] = True
                else:
                    eachuser['ignore'] = False
    if isinstance (user , str):
        for eachuser in users:
            if eachuser['alias'] == user:
                display ("Se va a modificar el usuario: " + eachuser['alias'])
                response = input("Ingrese el nuevo alias o presione enter para no cambiarlo:")
                if response != "":
                    eachuser['alias'] = response
                display ("Desea que el usuario " + eachuser['alias'] + " sea ignorado.")
                response = input("(si/NO)")
                if response == "si":
                    eachuser['ignore'] = True
                else:
                    eachuser['ignore'] = False

    with open(filename, 'wb') as f:
        pickle.dump(users, f)

def listOfUsers ():

    """
        devuelve la lista de usuarios almacenada en el alias
    """
    from IPython.display import display
    import os
    import pickle
    from scripts.constants import PATHALIAS

    filename = PATHALIAS

    if os.path.isfile(filename):
        with open(filename, 'rb') as f:
            users = pickle.load(f)
    else:
        display ('ERROR : No se ha encontrado el archivo ' + filename)

    return users


def listOfUsersClean ():

    """
        devuelve la lista de usuarios almacenada en el alias solo si son de los utiles
    """
    from IPython.display import display

    users = listOfUsers()
    usersClean = [user for user in users if user['ignore']==False]
    return usersClean

def listOfUsersCleanAlias ():

    """
        devuelve la lista de alias almacenada en el alias solo si son de los utiles
    """
    from IPython.display import display

    usersClean = listOfUsersClean()
    return [user['alias'] for user in usersClean]

def updateListOfUsers ():

    """
        Detecta que usuarios no tienen alias y propone modificarlo en forma semiautomartica
    """
    from IPython.display import display
    from scripts.general import fechaLocal
    import os
    import pickle
    from scripts.constants import PATHALIAS

    users = listOfUsers()
    for user in users:
        if user['alias']==str(user['id']):
            display ('Usuario creado el '+str(fechaLocal(user['id'])))
            response = input("Ingrese un alias o enter para continuar:")
            if response!= "":
                user['alias'] = response
            response = input("Presiones 'si' para descartar este usuario del procesamiento de datos")
            if response=="si":
                user['ignore'] = True

    filename = PATHALIAS
    with open(filename, 'wb') as f:
        pickle.dump(users, f)

def pandasUtilPiloto(completos=True):

    from IPython.display import display
    from scripts.constants import PATHSESSSION, PATHCONVERGENCIAS
    import os
    import pickle
    import pandas

    # Cargamos los usuarios
    users = listOfUsers()

    # Cargamos la base de datos de sessiones
    filename = PATHSESSSION
    if os.path.isfile(filename):
        with open(filename, 'rb') as f:
            sessions = pickle.load(f)
    else:
        display ('ERROR! : No se encontro el archivo ' + filename)
        return

    # Cargamos la base de datos de convergencias
    filename = PATHCONVERGENCIAS
    if os.path.isfile(filename):
        with open(filename, 'rb') as f:
            dinamicas = pickle.load(f)
    else:
        display ('ERROR! : No se encontro el archivo ' + filename)
        return

    # Extraemos la info util de cada tabla

    # Users...
    users_df = pandas.DataFrame (users)
    users_df.rename(columns={'id': 'userId'}, inplace=True)
    users_df = users_df[users_df['ignore']==False]

    # Sessiones...
    newSessions = []
    for session in sessions:
        newSession = {}
        newSession['sessionInstance'] = session ['contenido']['sessionInstance']
        newSession['userId'] = session['contenido']['userId']
        if 'plataforma' in session['contenido'].keys():
            newSession['plataforma'] = session['contenido']['plataforma']
        newSessions = newSessions + [newSession]
    sessions_df = pandas.DataFrame (newSessions)

    df = pandas.merge(users_df, sessions_df, on='userId')

    # Dinamicas...
    newDinamicas = []
    for dinamica in dinamicas:
        newDinamica = {}
        newDinamica['sessionInstance'] = dinamica['contenido']['expLog']['session']['sessionInstance']
        newDinamica['levelInstance'] = dinamica['contenido']['expLog']['levelInstance']
        newDinamica['expName'] = dinamica['contenido']['expLog']['expName']
        # newDinamica['convergenciaAlcanzada'] = dinamica['contenido']['dinamica']['convergenciaAlcanzada']    // Esta linea quedo obsoltea con el nuevo formato
        # newDinamica['tipoDeTrial'] = dinamica['contenido']['dinamica']['trialType']
        newDinamica['levelFinalizadoCorrectamente'] = dinamica['contenido']['dinamica']['levelFinalizadoCorrectamente']
        newDinamica['historial'] = dinamica['contenido']['dinamica']['historial']
        newDinamica['identificador'] = dinamica['contenido']['dinamica']['identificador']
        newDinamica['referencia'] = dinamica['contenido']['dinamica']['referencia']
        #newDinamica['tamanoVentanaAnalisisConvergencia'] = dinamica['contenido']['dinamica']['tamanoVentanaAnalisisConvergencia']
        #newDinamica['ultimaSD'] = dinamica['contenido']['dinamica']['ultimaSD']
        #newDinamica['ultimoMEAN'] = dinamica['contenido']['dinamica']['ultimoMEAN']
        newDinamicas = newDinamicas + [newDinamica]
    dinamicas_df = pandas.DataFrame(newDinamicas)

    df = pandas.merge(df,dinamicas_df, on='sessionInstance')

    return df
