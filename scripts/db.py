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
    Este codigo sirve para ir acumulando los datos brutos tal cual salen de la base datos que se descarga, de forma de poder limpiar y reducir el tamaño del archivo online mas o menos seguido
    sin perder la coherencia de los datos. Esto es necesario porque el json-server no se banca bien manejar archivos muy grandes (empieza a tener delay) y el volumen de datos que se genera crece rapido.

    La idea es que separa en archivos separados las listas de registros separados por categoria para que despues puedan ser procesados segun corresponda
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

    updateUsers()

def updateUsers():

    from IPython.display import display
    import os
    import pickle
    import json



    filename = './Guardados/db.' + 'NEWSESION'
    if os.path.isfile(filename):
        with open(filename, 'rb') as f:
            sessiones = pickle.load(f)
    else:
        display ('ERROR! : No se encontro el archivo ' + filename + ' con el registro de las sessiones.')
        # return


    newUsersId = set([json.loads(session['contenido'])['session']['user']['id'] for session in sessiones])

    filename = './Guardados/db.' + 'Alias'

    if os.path.isfile(filename):
        with open(filename, 'rb') as f:
            alias = pickle.load(f)
    else:
        alias = {}

    for aliaKey, alis in alias.items():
        pass

    usersId = [alia['id'] for aliaKey, alia in alias.items()]

    for newUserId in newUsersId:
        if not newUserId in usersId:
            newUser = {}
            newUser['id'] = newUserId
            newUser['alias'] = str(newUserId)
            newUser['ignore'] = False
            alias[newUserId] = newUser

    with open(filename, 'wb') as f:
        pickle.dump(alias, f)

def updateUser (userId, newAlias, ignore = False):

    from IPython.display import display
    import os
    import pickle

    filename = './Guardados/db.' + 'Alias'

    if os.path.isfile(filename):
        with open(filename, 'rb') as f:
            alias = pickle.load(f)
    else:
        display ('ERROR : No se ha encontrado el archivo ' + filename)

    user = alias[userId]

    user['alias'] = newAlias
    user['ignore'] = ignore

    with open(filename, 'wb') as f:
        pickle.dump(alias, f)

def listOfUsers ():

    from IPython.display import display
    import os
    import pickle

    filename = './Guardados/db.' + 'Alias'

    if os.path.isfile(filename):
        with open(filename, 'rb') as f:
            alias = pickle.load(f)
    else:
        display ('ERROR : No se ha encontrado el archivo ' + filename)

    display (alias)
