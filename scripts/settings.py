def makeSettings (basic=True,levels=False):

    import json

    filtros = {}

    filtros['sessions']=[]
    filtros['levels']=[]
    filtros['trials']=[]
    filtros['touchs']=[]
    filtros['sounds']=[]

    if basic:
        filtros['sessions']=filtros['sessions']+['class','idEnvio','status']
        filtros['levels']=filtros['levels']+['class','exitTrialId','idEnvio','levelLength','status','trialsVisited','exitTrialPosition','idUser','sortOfTrials','startTrialPosition']
        filtros['trials']=filtros['trials']+['class','distribucionEnPantalla','idEnvio','indexOfTrialInLevel','resourcesIdSelected','status','trialExitRecorded','trialsInLevel','userId','sessionId','soundLog','touchLog','timeInTrial','timeStopTrialInLevel','resourcesVersion', 0]
        filtros['touchs']=filtros['touchs']+['levelInstance','numberOfSoundLoops','sessionInstance','soundIdSecuenceInTrial','soundInstance','soundRunning','timeLastStartSound','timeSinceTrialStarts','tipoDeTrial','trialId','timeLastStopSound']
        filtros['sounds']=filtros['sounds']+['categorias', 'fromStimuli', 'levelInstance', 'numberOfLoop', 'numberOfSoundInTrial', 'soundSecuenceInTrial', 'startTimeSinceTrial', 'stopByEnd', 'stopByExit', 'stopByUnselect', 'stopTime', 'tipoDeTrial', 'trialId', 'sessionInstance']

    if not levels:
        filtros['levels']=filtros['levels']+['analisis']

    renames = {}

    renames['sessions'] = {'id':'sessionInstance'}
    renames['levels'] = {'sessionId':'sessionInstance','timeExit':'timeLevelExit','timeStarts':'timeLevelStarts'}
    renames['trials'] = {'timeExitTrial':'timeTrialExit','jsonMetaDataRta':'jsonMetaDataEstimulo'}
    renames['touchs'] = {'categorias':'categoriasTouched'}
    renames['sounds'] = {'soundId':'soundSourceId'}

    listaUsuarios = {1449588595132:'Ioni2', 1449175277519:'Ioni1', 1449524935330:'Iael', 1450205094190:'RieraPruebas',1450227329559:'Lizaso',1450352899438:'Dario17del12'}
    filtrosxVersion = {'levelVersion':0, 'resourcesVersion':0, 'codeVersion':0, 'filtrarXUsuarioRegistrado':False, 'usuario':False}

    settings = {}
    settings['filtros']=filtros
    settings['renames']=renames
    settings['listaUsuarios']=listaUsuarios
    settings['filtrosxVersion']=filtrosxVersion

    json.dump(settings, open("./Settings/settings",'w'))
