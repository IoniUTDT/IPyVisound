def analizarSesion (sesion, data):
    #Carga los datos
    levels=data['levels']
    trials=data['trials']
    
    print ('Se analizara la sesion del '+ str(fechaLocal(sesion['id'])))
    levelsSesion = levels[levels['sessionId']==sesion['id']]

    print ('Numero de niveles jugados en esta sesion: '+str(len(levelsSesion.index)))
    print ('')
    
    for index, level in levelsSesion.iterrows():
        print ('Detalles del nivel: '+str(level['levelId']))
        print ('Titulo del nivel: ' + level['levelTitle'])
        print ('Horario de juego: ' + str(fechaLocal(level['levelInstance'])))
        print ('Duracion del nivel: ' + str((level['timeExit']-level['timeStarts'])/1000 * 1/60)[:-12] + ' minutos')
        
        if not level['levelCompleted']:
            print ('Nivel incompleto')
        
        print ('')
        print ('Detalle de los trials del nivel '+str(level['levelId'])+':')
        trialsLevel = trials[trials['levelInstance']==level['levelInstance']]
        trialsLevelTest = trialsLevel[trialsLevel['tipoDeTrial']=='TEST']
        histograma = makeHistogramaTrials(trialsLevelTest)
        print (histograma)
        
        
        print ('')
        print ('')

def analizarUsuario (usuario, data):
    #Carga los datos necesarios
    sessions = data['sessions']
    
    print ('Se analizara las estadisticas del usuario '+ str(usuario['Alias'])+':')
    sesionesUsuario = sessions[sessions['userID']==usuario['usuarios']]
    
    print ('Cantidad de veces que se logueo el usuario: '+str(len(sesionesUsuario.index)))
    print ('Fechas:')
    
    for fecha in sesionesUsuario['id']:
        print (str(fechaLocal(fecha)))
    
    print ('')
    
    for index, session in sesionesUsuario.iterrows():
        analizarSesion(session,data)

def fechaLocal (millisec):
    import datetime
    
    return datetime.datetime.fromtimestamp(millisec/1000)
