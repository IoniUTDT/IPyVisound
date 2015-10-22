def graficarTimeline (data):

    import matplotlib.pyplot as plt
    import numpy as np
    import datetime
    
    sessions = data['sessions']
    levels = data['levels']
    trials = data['trials']
    touchs = data['touchs']
    sounds = data['sounds']
    usuarios = data['usuarios']
    
    juntar = False # Si es true, junta todos los levels de una misma sesion, sino separa por level

    for index, usuario in usuarios.iterrows():
        # Genera el plot
        fig = plt.figure(figsize=(20,5))

        ax = fig.add_subplot(111)
        ax.set_title('Informacion de eventos para el usuario {}'.format(usuario['Alias']), fontsize=10, fontweight='bold')
        ax.set_xlabel('Tiempo')
        ax.set_ylabel('')
        ax.get_yaxis().set_ticks([])
        ax.set_ylim([0,11])



        # Procesa la info de las sesiones
        sesionesUsuario = sessions[sessions['userID']==usuario['usuarios']]
        fechas = sesionesUsuario['sessionDate']
        altura = np.ones(fechas.size)*10
        ax.plot(fechas,altura,'ro')

        # ahora para este usuario va a hacer un grafico por sesion
        for index, session in sesionesUsuario.iterrows():

            #Carga los levels de la sesion
            levelsSesion = levels[levels['sessionId']==session['id']]

            if juntar: #Crea un grafico nuevo si esta configurado asi
                if levelsSesion.size > 0:
                    # Genera el plot si se va a usar
                    fig = plt.figure(figsize=(20,5))
                    ax = fig.add_subplot(111)
                    ax.set_title('Informacion de eventos para el usuario '+str(usuario['Alias'])+' sesion del '+str(session['sessionDate']), fontsize=14, fontweight='bold')
                    ax.set_xlabel('Tiempo')
                    ax.set_ylabel('')
                    ax.get_yaxis().set_ticks([])
                    ax.set_ylim([0,11])

            # Procesa la info de los levels
            for index, level in levelsSesion.iterrows():

                if not juntar: #Crea un grafico nuevo si esta configurado asi
                    # Genera el plot si se va a usar
                    fig = plt.figure(figsize=(20,5))
                    ax = fig.add_subplot(111)
                    ax.set_title('Informacion de eventos para el usuario '+str(usuario['Alias'])+' sesion del '+str(session['sessionDate']), fontsize=14, fontweight='bold')
                    ax.set_xlabel('Tiempo')
                    ax.set_ylabel('')
                    ax.get_yaxis().set_ticks([])
                    ax.set_ylim([0,11])

                # Configura el color segun este completado o no el nivel
                if level['levelCompleted'] == True:
                    color = 'blue'
                else:
                    color = 'red'
                # Grafica el segmento principal
                x = [datetime.datetime.fromtimestamp (level['timeStarts']/1000),datetime.datetime.fromtimestamp (level['timeExit']/1000)]
                y = [9,9]
                ax.plot(x,y,color=color)
                # Grafica dos bordes para remarcar los inicios y los finales
                ax.plot([datetime.datetime.fromtimestamp(level['timeStarts']/1000-0.01),datetime.datetime.fromtimestamp(level['timeStarts']/1000+0.01)],[y[0]+0.5,y[0]-0.5],color=color)
                ax.plot([datetime.datetime.fromtimestamp(level['timeExit']/1000-0.01),datetime.datetime.fromtimestamp(level['timeExit']/1000+0.01)],[y[0]+0.5,y[0]-0.5],color=color)
                # Agrega el id del nivel
                xCenter = datetime.datetime.fromtimestamp ((level['timeStarts']/1000+level['timeExit']/1000)/2)
                ax.text(xCenter, 8.5, level['levelId'])

                # Procesa la info de los trials del level en cuestion
                trialsSesion = trials[trials['levelInstance']==level['levelInstance']]
                for index, trial in trialsSesion.iterrows():
                    # Configura el color segun el tipo de trial
                    if trial['tipoDeTrial'] == 'ENTRENAMIENTO':
                        color = 'yellow'
                    else:
                        color = 'cyan'
                    # Grafica el segmento principal
                    x = [datetime.datetime.fromtimestamp (trial['timeTrialStart']/1000),datetime.datetime.fromtimestamp (trial['timeExitTrial']/1000)]
                    y = [7,7]
                    ax.plot(x,y,color=color)
                    # Grafica dos bordes para remarcar los inicios y los finales
                    ax.plot([datetime.datetime.fromtimestamp(trial['timeTrialStart']/1000-0.01),datetime.datetime.fromtimestamp(trial['timeTrialStart']/1000+0.01)],[y[0]+0.5,y[0]-0.5],color=color)
                    ax.plot([datetime.datetime.fromtimestamp(trial['timeExitTrial']/1000-0.01),datetime.datetime.fromtimestamp(trial['timeExitTrial']/1000+0.01)],[y[0]+0.5,y[0]-0.5],color=color)
                    # Agrega el id del trial
                    xCenter = datetime.datetime.fromtimestamp ((trial['timeTrialStart']/1000+trial['timeExitTrial']/1000)/2)
                    ax.text(xCenter, 6.5, trial['trialId'])

                    # Procesa los toques en cada trial
                    touchsTrial = touchs[touchs['trialInstance']==trial['trialInstance']]
                    for index, touch in touchsTrial.iterrows():

                        # Configura el color segun sea un acierto o no
                        if touch['isTrue'] == True: # Ojo que aca un Nan es un false!
                            color = 'green'
                        else:
                            color = 'red'

                        y = [3,3]
                        # Grafica el segmento cuasivertical
                        ax.plot([datetime.datetime.fromtimestamp(touch['touchInstance']/1000-0.01),datetime.datetime.fromtimestamp(touch['touchInstance']/1000+0.01)],[y[0]+0.5,y[0]-0.5],color=color)
                        # Agrega el id del elemento tocado
                        xCenter = datetime.datetime.fromtimestamp (touch['touchInstance']/1000+0.3)
                        ax.text(xCenter, 2.5, touch['idResourceTouched']['id'])

                    # Procesa los sounds en cada trial
                    soundsTrial = sounds[sounds['trialInstance']==trial['trialInstance']]
                    for index, sound in soundsTrial.iterrows():

                        # Configura el color
                        color = 'gray'
                        y = [5,5]
                        # Grafica el segmento cuasivertical
                        ax.plot([datetime.datetime.fromtimestamp(sound['soundInstance']/1000-0.01),datetime.datetime.fromtimestamp(sound['soundInstance']/1000+0.01)],[y[0]+0.5,y[0]-0.5],color=color)
                        # Agrega el id del elemento tocado
                        xCenter = datetime.datetime.fromtimestamp (sound['soundInstance']/1000+0.3)
                        ax.text(xCenter, 4.5, sound['soundId']['id'])
