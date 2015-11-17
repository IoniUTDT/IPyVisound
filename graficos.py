def makeTimeline (touchs, sounds):

    import sys
    if not sys.version_info[:2] == (3, 4):
        print ('Sos un boludo!, pero uno previsor')
        print ('Este codigo esta pensado para correr en python 3.4')
    
    import matplotlib.pyplot as plt
    import numpy as np
    import datetime
    from Scripts import fechaLocal

    juntar = False # Si es true, junta todos los levels de una misma sesion, sino separa por level

    for usuario in touchs['Alias'].unique():
        # Genera el plot
        fig = plt.figure(figsize=(30,5))

        ax = fig.add_subplot(111)
        ax.set_title('Informacion de eventos para el usuario {}'.format(usuario), fontsize=10, fontweight='bold')
        ax.set_xlabel('Tiempo')
        ax.set_ylabel('')
        ax.get_yaxis().set_ticks([])
        ax.set_ylim([0,11])



        # Procesa la info para graficar las sesiones del usuario
        fechas = touchs[touchs['Alias']==usuario]['sessionInstance']
        fechasFormateadas = [fechaLocal(fecha) for fecha in fechas]
        altura = np.ones(fechas.size)*10
        ax.plot(fechasFormateadas,altura,'ro')

        touchsUsuario = touchs[touchs['Alias'] == usuario]
        soundsUsuario = sounds[sounds['Alias'] == usuario]

        # ahora para este usuario va a hacer un grafico por sesion
        for session in touchsUsuario['sessionInstance'].unique():

            #Carga los touchs de cada session
            touchsSession = touchsUsuario[touchsUsuario['sessionInstance']==session]
            soundsSession = soundsUsuario[soundsUsuario['sessionInstance']==session]

            if juntar: #Crea un grafico nuevo si esta configurado asi
                if touchsSession.size > 0:
                    # Genera el plot si se va a usar
                    fig = plt.figure(figsize=(30,5))
                    ax = fig.add_subplot(111)
                    ax.set_title('Informacion de eventos para el usuario '+str(usuario)+' sesion del '+str(fechaLocal(touchSession)), fontsize=14, fontweight='bold')
                    ax.set_xlabel('Tiempo')
                    ax.set_ylabel('')
                    ax.get_yaxis().set_ticks([])
                    ax.set_ylim([0,11])
         
            # Procesa la info de los levels
            for level in touchsSession['levelInstance'].unique():

                touchsLevel = touchsSession[touchsSession['levelInstance']==level]
                soundsLevel = soundsSession[soundsSession['levelInstance']==level]
                levelInfo = touchsLevel.iloc[0]

                if not juntar: #Crea un grafico nuevo si esta configurado asi
                    # Genera el plot si se va a usar
                    fig = plt.figure(figsize=(30,5))
                    ax = fig.add_subplot(111)
                    ax.set_title('Informacion de eventos para el usuario '+str(usuario)+', sesion del '+str(fechaLocal(session))+', nivel: '+str(levelInfo['levelId']), fontsize=14, fontweight='bold')
                    ax.set_xlabel('Tiempo')
                    ax.set_ylabel('')
                    ax.get_yaxis().set_ticks([])
                    ax.set_ylim([0,11])

                # Configura el color segun este completado o no el nivel
                if levelInfo['levelCompleted'] == True:
                    color = 'blue'
                else:
                    color = 'red'

                # Grafica el segmento principal
                x = [fechaLocal(levelInfo['timeLevelStarts']),fechaLocal(levelInfo['timeLevelExit'])]
                y = [9,9]
                ax.plot(x,y,color=color)
                # Grafica dos bordes para remarcar los inicios y los finales
                ax.plot([fechaLocal(levelInfo['timeLevelStarts']-0.01),fechaLocal(levelInfo['timeLevelStarts']+0.01)],[y[0]+0.5,y[0]-0.5],color=color)
                ax.plot([fechaLocal(levelInfo['timeLevelExit']-0.01),fechaLocal(levelInfo['timeLevelExit']+0.01)],[y[0]+0.5,y[0]-0.5],color=color)

                # Agrega el id del nivel
                xCenter = fechaLocal((levelInfo['timeLevelStarts']+levelInfo['timeLevelExit'])/2)
                ax.text(xCenter, 8.5, levelInfo['levelInstance'])


                # Procesa la info de los trials del level en cuestion
                for trial in touchsLevel['trialInstance'].unique():

                    touchsTrial = touchsLevel[touchsLevel['trialInstance']==trial]
                    soundsTrial = soundsLevel[soundsLevel['trialInstance']==trial]

                    trialInfo = touchsTrial.iloc[0]

                    # Configura el color segun el tipo de trial
                    if trialInfo['tipoDeTrial'] == 'TUTORIAL':
                        color = 'yellow'
                    else:
                        color = 'cyan'

                    # Grafica el segmento principal
                    x = [fechaLocal(trialInfo['timeTrialStart']),fechaLocal(trialInfo['timeTrialExit'])]
                    y = [7,7]
                    ax.plot(x,y,color=color)
                    # Grafica dos bordes para remarcar los inicios y los finales
                    ax.plot([fechaLocal(trialInfo['timeTrialStart']-0.01),fechaLocal(trialInfo['timeTrialStart']+0.01)],[y[0]+0.5,y[0]-0.5],color=color)
                    ax.plot([fechaLocal(trialInfo['timeTrialExit']-0.01),fechaLocal(trialInfo['timeTrialExit']+0.01)],[y[0]+0.5,y[0]-0.5],color=color)
                    # Agrega el id del trial
                    xCenter = fechaLocal ((trialInfo['timeTrialStart']+trialInfo['timeTrialExit'])/2)
                    ax.text(xCenter, 6.5, trialInfo['trialId'])

                    # Procesa la info de los touchs del trial en cuestion 
                    for touchInstance in touchsTrial['touchInstance'].unique():
                        touch = touchsTrial[touchsTrial['touchInstance']==touchInstance]
                        touch = touch.iloc[0]

                        # Configura el color segun sea un acierto o no
                        if touch['isTrue'] == True: # Ojo que aca un Nan es un false!
                            color = 'green'
                        else:
                            color = 'red'
                            

                        y = [3,3]
                        # Grafica el segmento cuasivertical
                        ax.plot([fechaLocal(touch['touchInstance']-0.01),fechaLocal(touch['touchInstance']+0.01)],[y[0]+0.5,y[0]-0.5],color=color)
                        # Agrega el id del elemento tocado
                        xCenter = fechaLocal(touch['touchInstance']+0.3)
                        ax.text(xCenter, 2.5, touch['idResourceTouched']['id'])


                    # Procesa los sounds en cada trial
                    for soundInstance in soundsTrial['soundInstance'].unique():

                        sound = soundsTrial[soundsTrial['soundInstance']==soundInstance]
                        sound = sound.iloc[0]

                        # Configura el color
                        color = 'gray'
                        y = [5,5]
                        # Grafica el segmento cuasivertical
                        ax.plot([fechaLocal(soundInstance-0.01),fechaLocal(soundInstance+0.01)],[y[0]+0.5,y[0]-0.5],color=color)
                        # Agrega el id del elemento tocado
                        xCenter = fechaLocal(soundInstance+0.3)
                        ax.text(xCenter, 4.5, sound['soundSourceId']['id'])
