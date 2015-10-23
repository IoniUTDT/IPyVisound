def LoadDataFromFile ():
    
    import json
    import pandas as pd
    import numpy as np
    
    filename = 'db.json'
        
    with open(filename) as data_file:    
        db = json.load(data_file)

    # Cargo la data de las sesiones en una tabla pandas
    sessions = pd.concat((pd.DataFrame(x) for x in db['SessionEnviables']), ignore_index=True)
    # Transformo la info de los logueos en formato unixtime a una fecha legible (en zona horaria GTM=0)
    sessions['sessionDate'] = pd.to_datetime(sessions['id'], unit='ms')
    # Cargo de los niveles
    levels = pd.concat((pd.DataFrame(x) for x in db['LevelEnviables']), ignore_index=True)
    # Carga las fechas en formato legible para todo lo que corresponda
    levels['fechaEnvio'] = pd.to_datetime(levels['idEnvio'], unit='ms')
    levels['fechaLevelStart'] = pd.to_datetime(levels['timeStarts'], unit='ms')
    levels['fechaLevelExit'] = pd.to_datetime(levels['timeExit'], unit='ms')
    # Carga la info de los trials
    trials = pd.concat((pd.DataFrame(x) for x in db['TrialEnviables']), ignore_index=True)
    # Convierte a fecha legible todo lo que tiene sentido
    trials['fechaEnvio'] = pd.to_datetime(trials['idEnvio'], unit='ms')
    trials['fechaTrialExit'] = pd.to_datetime(trials['timeExitTrial'], unit='ms')
    trials['fechaTrialStart'] = pd.to_datetime(trials['timeTrialStart'], unit='ms')
    # Ahora creamos la tabla con toda la info de cada toque y sound para lo que hay que buscar y concatenar la info fragmentada en cada trial
    touchs = pd.concat(pd.DataFrame(x) for x in list(trials['touchLog']) if x is not np.nan)
    sounds = pd.concat(pd.DataFrame(x) for x in list(trials['soundLog']) if x is not np.nan)
    # Crea una lista de usuario
    usuarios = pd.DataFrame(pd.unique(list(sessions['userID'])),columns=['usuarios'])
    usuarios = usuarios.reset_index()
    usuarios.rename(columns={'index': 'Alias'}, inplace=True)

    data = {}
    data['sessions'] = sessions
    data['levels'] = levels
    data['trials'] = trials
    data['touchs'] = touchs
    data['sounds'] = sounds
    data['usuarios'] = usuarios
    
    return data