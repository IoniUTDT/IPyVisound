def plotConvergenciaAngulos (levels, completos=True):
    """
        Esta función grafica el angulo en funcion del numero de trial para cada uno de los cuadrantes
    """
    import matplotlib.pyplot as plt
    from IPython.display import display
    from scripts.general import fechaLocal
    import json

    from scripts.general import chkVersion
    chkVersion()

    if completos:
        levels = levels[levels['levelCompleted']]

    for usuario in levels['Alias'].unique():
        display ('Se hara la estadistica del usuario: '+usuario)
        levelsUsuario = levels[levels['Alias']==usuario]
        display ('El usuario '+usuario+' jugo '+str(len(levelsUsuario['sessionInstance'].unique()))+' veces')
        for session in levelsUsuario['sessionInstance'].unique():
            levelSession = levelsUsuario[levelsUsuario['sessionInstance']==session]
            display ('En la session '+ str(fechaLocal(session))+ ' el usuario '+str(usuario)+' jugo '+str(len(levelSession['levelInstance'].unique())) + ' niveles')
            for level in levelSession['levelInstance'].unique():
                levelLevel = levelSession[levelSession['levelInstance']==level]
                # display (levelLevel)
                levelInfo = levelLevel.iloc[0]
                analisisJson = levelInfo['analisis']

                # Armamos el grafico de nivel
                fig1 = plt.figure(figsize=(10,3))
                ax1 = fig1.add_subplot(111)
                title = 'Evolucion de la dificultad en funcion del trial \n' + 'Usuario: '+str(usuario) + ' en el nivel ' + str(levelInfo['levelTitle'])+', levelVersion: '+str(levelInfo['levelVersion'])
                ax1.set_title(title, fontsize=10, fontweight='bold')
                ax1.set_xlabel('Numero de trial')
                ax1.set_ylabel('Nivel')

                # Armamos el grafico de angulo
                fig2 = plt.figure(figsize=(10,3))
                ax2 = fig2.add_subplot(111)
                title = 'Evolucion del angulo en funcion del trial \n' + 'Usuario: '+str(usuario) + ' en el nivel ' + str(levelInfo['levelTitle'])+', levelVersion: '+str(levelInfo['levelVersion'])
                ax2.set_title(title, fontsize=10, fontweight='bold')
                ax2.set_xlabel('Numero de trial')
                ax2.set_ylabel('Angulo')

                numeroDeCuadrante=0
                for cuadrante in analisisJson['cuadrantes']:
                    numeroDeCuadrante = numeroDeCuadrante + 1
                    #display(cuadrante)
                    aciertos=[]
                    angulosRef=[]
                    angulos=[]
                    angulosNivel = []
                    for historial in cuadrante['historial']:
                        # Extraemos la lista de aciertos o errores de la info del historial
                        if historial['acertado']:
                            aciertos=aciertos+[True]
                        else:
                            aciertos=aciertos+[False]
                        angulos = angulos + [historial['angulo']['angulo']]
                        angulosRef = angulosRef + [historial['angulo']['anguloRef']]
                        angulosNivel = angulosNivel + [historial['angulo']['nivel']]
                    #display (aciertos)
                    #display (angulosRef)
                    #display (angulos)
                    #display (angulosNivel)

                    # Dibujamos los niveles
                    x = range(len(angulosNivel))
                    y = angulosNivel
                    ax1.plot(x,y, label="Cuadrante "+str(numeroDeCuadrante))
                    # marcamos aciertos y errores
                    x = [i for i in range(len(aciertos)) if aciertos[i]]
                    y = [angulosNivel[i] for i in range(len(aciertos)) if aciertos[i]]
                    ax1.plot(x,y,'go')
                    x = [i for i in range(len(aciertos)) if not aciertos[i]]
                    y = [angulosNivel[i] for i in range(len(aciertos)) if not aciertos[i]]
                    ax1.plot(x,y,'ro')
                    # Marcamos el final si es convergencia o no.
                    if cuadrante['convergenciaAlcanzada']:
                        ax1.plot([len(angulosNivel)-1],angulosNivel[-1],'bs', markersize=10)
                    else:
                        if len(angulosNivel) > 0: # Esto es porque hay datos malos, no deberia hacer falta en gral
                            ax1.plot([len(angulosNivel)-1],angulosNivel[-1],'rs', markersize=10)
                    ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))

                    # Dibujamos los angulos
                    x = range(len(angulos))
                    y = angulos
                    ax2.plot(x,y, label="Cuadrante "+str(numeroDeCuadrante))
                    # marcamos aciertos y errores
                    x = [i for i in range(len(aciertos)) if aciertos[i]]
                    y = [angulos[i] for i in range(len(aciertos)) if aciertos[i]]
                    ax2.plot(x,y,'go')
                    x = [i for i in range(len(aciertos)) if not aciertos[i]]
                    y = [angulos[i] for i in range(len(aciertos)) if not aciertos[i]]
                    ax2.plot(x,y,'ro')
                    # Marcamos el final si es convergencia o no.
                    if cuadrante['convergenciaAlcanzada']:
                        ax2.plot([len(angulos)-1],angulos[-1],'bs', markersize=10)
                    else:
                        if len(angulos) > 0: # Esto es porque hay datos malos, no deberia hacer falta en gral
                            ax2.plot([len(angulos)-1],angulos[-1],'rs', markersize=10)
                    ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))
