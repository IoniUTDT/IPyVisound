def load (codeVersion):
    
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

    levels.drop(['class','exitTrialId','exitTrialId','idEnvio','levelLength','status','trialsVisited','exitTrialPosition','idUser','sortOfTrials'],inplace=True, axis=1)
    trials.drop(['class','distribucionEnPantalla','idEnvio','indexOfTrialInLevel','resourcesIdSelected','status','trialExitRecorded','trialsInLevel','userId','sessionId','soundLog','touchLog'],inplace=True, axis=1)
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
    if codeVersion != 0:
        touchs = touchs[touchs['codeVersion']==codeVersion]
        sounds = sounds[sounds['codeVersion']==codeVersion]
        
    print ('recursos cargados del archivo')
    return touchs, sounds
