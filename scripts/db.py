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
    import filecmp

    timestamp = time.time()
    st = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    filenameBackup = cts.PathDirDbBackUp + cts.FileNameLocalDb[:-5] + ' backup ' + st + '.json'

    print ('Starting download, please wait')

    # Bajamos el archivo
    urllib.request.urlretrieve(cts.URLserver, cts.FileNameLocalDbTemp)
    print ('Donload finish')

    if filecmp.cmp(cts.FileNameLocalDbTemp,cts.FileNameLocalDb):
        print ('El archivo descargado es identico al existente')

    # Renombramos el archivo viejo y dejamos el descargado con el nombre que corresponde si se descargo bien
    if os.path.isfile(cts.FileNameLocalDbTemp):
        if os.path.isfile(cts.FileNameLocalDb):
            os.rename(cts.FileNameLocalDb,filenameBackup)
        os.rename(cts.FileNameLocalDbTemp,cts.FileNameLocalDb)

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

    # Se me filtro envios de un aversion vieja de la app!
    dataFiltrada=[]
    for envio in data:
        if cts.Db_Envios_TipoDeEnvioKey in envio:
            dataFiltrada = dataFiltrada + [envio]
    data = dataFiltrada

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
        #if user[cts.Db_Users_Alias]==str(user[cts.Db_Sesion_User_Id]):
            display ('Usuario creado el '+str(fechaLocal(user[cts.Db_Sesion_User_Id])) + ' Alias actual: ' +  user[cts.Db_Users_Alias])
            response = input("Ingrese un alias o enter para continuar:")
            if response!= "":
                user[cts.Db_Users_Alias] = response
            response = input("Presiones 'si' para descartar este usuario del procesamiento de datos")
            if response=="si":
                user[cts.Db_Users_Ignore] = True

    with open(cts.PATHALIAS, 'wb') as f:
        pickle.dump(users, f)

def pandasTransferencia(completos=True):

    import os
    import pickle
    import pandas

    # Cargamos los usuarios
    users = listOfUsers()

    # Cargamos la base de datos de sessiones
    if os.path.isfile(cts.PATHSESSSION):
        with open(cts.PATHSESSSION, 'rb') as f:
            sessions = pickle.load(f)
    else:
        display ('ERROR! : No se encontro el archivo ' + cts.PATHSESSSION)
        return

    # Cargamos la base de datos de convergencias
    if os.path.isfile(cts.PATHRESULTS):
        with open(cts.PATHRESULTS, 'rb') as f:
            resultados_db = pickle.load(f)
    else:
        display ('ERROR! : No se encontro el archivo ' + cts.PATHRESULTS)
        return

    # Extraemos la info util de cada tabla

    # Creamos una lista de usuarios
    users_df = pandas.DataFrame (users)
    users_df.rename(columns={cts.Db_Users_id: cts.P_UserId}, inplace=True)
    users_df = users_df[users_df[cts.Db_Users_Ignore]==False]

    # Para cada sesion agregamos la lista de resultados
    resultados = []
    respuestas = []
    for resultado_db in resultados_db:
        resultado = {}
        # Recuperamos la info del nivel:
        # resultado[cts.P_LevelIdentificador] = resultado_db[cts.Db_Envios_Contenido][cts.Db_Resultados_NivelLog][cts.Db_Resultados_NivelLog_LevelIdentificador] (Esto no conviene hacerlo aca porque si llega a mezclar niveles o algo no es info que venga del nivel posta)
        resultado[cts.P_EnvioInstance] = resultado_db[cts.Db_Envios_InstanceKey]
        resultado[cts.P_LevelInstance] = resultado_db[cts.Db_Envios_Contenido][cts.Db_Resultados_NivelLog][cts.Db_Resultados_NivelLog_LevelInstance]
        # Recuperamos la info de la sesion
        sessionData = resultado_db[cts.Db_Envios_Contenido][cts.Db_Resultados_NivelLog][cts.Db_Resultados_NivelLog_Sesion]
        resultado[cts.P_SessionInstance] = sessionData[cts.Db_Sesion_Instance]
        resultado[cts.P_UserId] = sessionData[cts.Db_Sesion_User][cts.Db_Sesion_User_Id]
        resultado[cts.P_FaseActiva] = sessionData[cts.Db_Sesion_User][cts.Db_Sesion_User_Fase]
        resultado[cts.P_OrientacionEntrenamiento] = sessionData[cts.Db_Sesion_User][cts.Db_Sesion_User_Eleccion]
        resultado[cts.P_CodeVersion]  = sessionData[cts.Db_Sesion_CodeVersion]
        # Recuperamos la info util de los resultados
        resultadosData = resultado_db[cts.Db_Envios_Contenido][cts.Db_Resultados_Dinamica]
        resultado[cts.P_LevelIdentificador] = resultadosData[cts.Db_Resultados_Dinamica_IdentificadorLevel]
        resultado[cts.P_LevelFinalizado] = resultadosData[cts.Db_Resultados_Dinamica_Finalizado]
        resultado[cts.P_Referencia] = resultadosData[cts.Db_Resultados_Dinamica_Referencia]

        # Buscamos y creamos una entrada por cada elemento del historial y lo agregamos

        historial = resultado_db[cts.Db_Envios_Contenido][cts.Db_Resultados_Dinamica][cts.Db_Resultados_Dinamica_Historial]
        for entrada in historial:
            respuesta = {}
            respuesta[cts.P_LevelInstance] = resultado[cts.P_LevelInstance]
            respuesta[cts.P_RtaCorrecta] = entrada[cts.Db_Historial_RtaCorrecta]
            respuesta[cts.P_NivelConfianza] = entrada[cts.Db_Historial_Confianza]
            respuesta[cts.P_NivelEstimuloDinamica] = entrada[cts.Db_Historial_EstimuloDinamica]
            respuesta[cts.P_TiempoRespuesta] = entrada[cts.Db_Historial_TiempoRta]
            respuesta[cts.P_TiempoRespuestaConfianza] = entrada[cts.Db_Historial_TiempoConfianza]
            respuesta[cts.P_NumeroDeLoopsAudio] = entrada[cts.Db_Historial_loops]
            respuesta[cts.P_TipoDeTrial] = entrada[cts.Db_Historial_TipoDeTrial]
            respuesta[cts.P_AnguloFijo] = entrada[cts.Db_Historial_Recurso][cts.Db_Historial_Recurso_AnguloFijo]
            respuesta[cts.P_Desviacion] = entrada[cts.Db_Historial_Recurso][cts.Db_Historial_Recurso_Desviacion]
            respuesta[cts.P_NivelEstimuloEstimulo] = entrada[cts.Db_Historial_Recurso][cts.Db_Historial_Recurso_Estimulo]
            respuesta[cts.P_IdEstimulos] = entrada[cts.Db_Historial_Recurso][cts.Db_Historial_Recurso_Id]


            respuestas = respuestas + [respuesta]

        resultados = resultados + [resultado]

    resultados_pandas = pandas.DataFrame(resultados)
    respuestas_pandas = pandas.DataFrame(respuestas)

    df = pandas.merge(users_df,resultados_pandas, on=cts.P_UserId)
    df = pandas.merge(df,respuestas_pandas, on=cts.P_LevelInstance)

    return df
