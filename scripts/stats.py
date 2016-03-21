def sessionStats():

    from scripts.db import listOfUsers
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
        return

    sessionsDB = [json.loads(session['contenido']) for session in sessiones]

    usersDict = listOfUsers()
    for userId in usersDict:
        userInfo = usersDict[userId]
        for session in sessionsDB:
            pass
            if userInfo['id'] == session['session']['user']['id']:
                display ('El usuario '+userInfo['alias']+' ha iniciado sesion el '+str(session['session']['sessionInstance'])+' en el experimento '+session['expName'])
            #display(userInfo)
    display (sessionsDB)
