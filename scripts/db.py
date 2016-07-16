import scripts.constants as cts

from scripts.general import chkVersion
from IPython.display import display

chkVersion()


def downloadFile ():

    """
        Esta funcion descarga la base de datos en formato json del servidor y hace una backup del archivo anterior.
    """

    import datetime
    import time
    import urllib
    import os

    timestamp = time.time()
    st = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    filenameBackup = cts.PathDirDbBackUp + cts.FileNameLocalDb[:-5] + ' backup ' + st + '.json'

    print ('Starting download, please wait')

    # Bajamos el archivo
    urllib.request.urlretrieve(cts.URLserver, cts.FileNameLocalDbTemp)


    # Renombramos el archivo viejo y dejamos el descargado con el nombre que corresponde si se descargo bien
    if os.path.isfile(cts.FileNameLocalDbTemp):
        if os.path.isfile(cts.FileNameLocalDb):
            os.rename(cts.FileNameLocalDb,filenameBackup)
        os.rename(cts.FileNameLocalDbTemp,cts.FileNameLocalDb)

    print ('Donload finish')


def join (filename=cts.FileNameLocalDb):

    """
    Este codigo sirve para ir acumulando los datos brutos tal cual salen de la base datos que se descarga, de forma de poder limpiar y reducir el tamaño del archivo online mas o menos seguido
    sin perder la coherencia de los datos. Esto es necesario porque el json-server no se banca bien manejar archivos muy grandes (empieza a tener delay) y el volumen de datos que se genera crece rapido.

    La idea es que guarda en archivos separados las listas de registros segun la categoria de envio para que despues puedan ser procesados segun corresponda
    """

    import json
    import os
    import pickle

    # Transformamos el archivo en un json
    with open(filename) as data_file:
        db = json.load(data_file)

    # Seleccionamos los datos
    data = db[cts.Db_Envios_Key]

    # Buscamos la lista de todas las categorias de envios
    tiposDeEnvio = set([envio[cts.Db_Envios_TipoDeEnvioKey] for envio in data])

    # La info guardada en esta parte esta pensada como una lista de envios segun el tipo
    for tipoDeEnvio in tiposDeEnvio:
        filenameDatos = cts.PathDirDatosLocal + tipoDeEnvio
        enviosNuevos = [envio for envio in data if envio[cts.Db_Envios_TipoDeEnvioKey] == tipoDeEnvio]

        # Sacamos el formato json a los envios
        #for envio in enviosNuevos:
        #    envio['objeto'] = json.loads(envio['objeto'])

        if os.path.isfile(filenameDatos):
            with open(filenameDatos, 'rb') as f:
                enviosViejos = pickle.load(f)
            enviosExists = True
            display (tipoDeEnvio + ' tiene '+str(len(enviosViejos))+' entradas.')
        else:
            display ('Warning: no se encontro entradas previas para ' + tipoDeEnvio + ' se guardaran ' + str(len(enviosNuevos)) + ' entradas nuevas.')
            enviosExists = False

        if enviosExists:
            enviosUnificados = enviosViejos + [envioNuevo for envioNuevo in enviosNuevos if not envioNuevo[cts.Db_Envios_InstanceKey] in set([envioViejo[cts.Db_Envios_InstanceKey] for envioViejo in enviosViejos])]
        else:
            enviosUnificados = enviosNuevos

        display (tipoDeEnvio + ' paso a tener '+str(len(enviosUnificados))+' entradas.')

        with open(filenameDatos, 'wb+') as f:
            pickle.dump(enviosUnificados, f)

    joinUsers()

def joinUsers():

    """
        Esta funcion busca los usuarios nuevos en la lista de sessiones guardadas y compara con la lista de usuarios almacenada en la base de datos alias. Si encuentra que alguno no esta pregunta el alias y si ignorarlo o no y lo incluye
    """
    import os
    import pickle
    from scripts.general import fechaLocal

    if os.path.isfile(cts.PATHSESSSION):
        with open(cts.PATHSESSSION, 'rb') as f:
            sessiones = pickle.load(f)
    else:
        display ('ERROR! : No se encontro el archivo ' + cts.PATHSESSSION + ' con el registro de las sessiones.')
        return

    newUsersId = set([session[cts.Db_Envios_Contenido][cts.Db_Sesion_User][cts.Db_Sesion_User_Id] for session in sessiones])

    if os.path.isfile(cts.PATHALIAS):
        with open(cts.PATHALIAS, 'rb') as f:
            users= pickle.load(f)
    else:
        users = []

    usersId = [user[cts.Db_Users_id] for user in users]

    for newUserId in newUsersId:
        if not newUserId in usersId:
            # Creamos el usuario
            newUser = {}
            newUser[cts.Db_Users_id] = newUserId
            # Preguntamos datos del usuario
            display ('Usuario creado el '+str(fechaLocal(newUser[cts.Db_Users_id])))
            response = input("Ingrese un alias o enter para continuar:\n")
            if response != "":
                newUser[cts.Db_Users_Alias] = response
            else:
                newUser[cts.Db_Users_Alias] = str(newUser[cts.Db_Users_i])
            response = input("Presiones 'si' para descartar este usuario del procesamiento de datos:\n")
            if response == "si":
                newUser[cts.Db_Users_Ignore] = True
            else:
                newUser[cts.Db_Users_Ignore] = False
            users = users + [newUser]

    with open(cts.PATHALIAS, 'wb') as f:
        pickle.dump(users, f)

def updateUser (user):

    """
        Esta funcion sirve para modificar a mano algun usuario en particular
    """
    import os
    import pickle

    if os.path.isfile(cts.PATHALIAS):
        with open(cts.PATHALIAS, 'rb') as f:
            users = pickle.load(f)
    else:
        display ('ERROR : No se ha encontrado el archivo ' + cts.PATHALIAS)
    
    
    for eachuser in users:
        cambiar = False

        if isinstance(user, int):
            if eachuser[cts.Db_Users_id] == user:
                cambiar = True
        if isinstance (user , str):            
            if eachuser[cts.Db_Users_Alias] == user:
                cambiar = True

        if cambiar:
            display ("Se va a modificar el usuario: " + eachuser[cts.Db_Users_Alias])
            response = input("Ingrese el nuevo alias o presione enter para no cambiarlo:")
            if response != "":
                eachuser[cts.Db_Users_Alias] = response
            display ("Desea que el usuario " + eachuser[cts.Db_Users_Alias] + " sea ignorado.")
            response = input("(si/NO)")
            if response == "si":
                eachuser[cts.Db_Users_Ignore] = True
            else:
                eachuser[cts.Db_Users_Ignore] = False

    with open(cts.PATHALIAS, 'wb') as f:
        pickle.dump(users, f)

def listOfUsers ():

    """
        devuelve la lista de usuarios almacenada en el alias
    """
    import os
    import pickle
    
    if os.path.isfile(cts.PATHALIAS):
        with open(cts.PATHALIAS, 'rb') as f:
            users = pickle.load(f)
    else:
        display ('ERROR : No se ha encontrado el archivo ' + cts.PATHALIA)

    return users


def listOfUsersClean ():

    """
        devuelve la lista de usuarios almacenada en el alias solo si son de los utiles
    """
    users = listOfUsers()
    usersClean = [user for user in users if user[cts.Db_Users_Ignore]==False]
    return usersClean

def listOfUsersCleanAlias ():

    """
        devuelve la lista de alias almacenada en el alias solo si son de los utiles
    """
    usersClean = listOfUsersClean()
    return [user[cts.Db_Users_Alias] for user in usersClean]

def updateListOfUsers ():

    """
        Detecta que usuarios no tienen alias y propone modificarlo en forma semiautomartica
    """
    from scripts.general import fechaLocal
    import os
    import pickle
    
    users = listOfUsers()
    for user in users:
        if user[cts.Db_Users_Alias]==str(user[cts.Db_Sesion_User_Id]):
            display ('Usuario creado el '+str(fechaLocal(user[cts.Db_Sesion_User_Id])))
            response = input("Ingrese un alias o enter para continuar:")
            if response!= "":
                user[cts.Db_Users_Alias] = response
            response = input("Presiones 'si' para descartar este usuario del procesamiento de datos")
            if response=="si":
                user[cts.Db_Users_Ignore] = True

    with open(cts.PATHALIAS, 'wb') as f:
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
