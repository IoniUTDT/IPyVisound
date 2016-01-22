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

    mostrarRefrencia = True
    mostrarNivel = False
    mostrarAngulo = False

    if completos:
        levels = levels[levels['levelCompleted']]

    for usuario in levels['Alias'].unique():
        display ('Se hara la estadistica del usuario: '+usuario)
        levelsUsuario = levels[levels['Alias']==usuario]
        display ('El usuario '+usuario+' jugo '+str(len(levelsUsuario['sessionInstance'].unique()))+' veces')

        if mostrarRefrencia:
            # Armamos el grafico de angulos refrenciados (esta aca porque queremos comparar entre todos los levels de todas las sesiones de un mismo usuario)

            # Armamos los colores
            # These are the "Tableau 20" colors as RGB.
            tableau20 = [(31, 119, 180), (174, 199, 232), (255, 187, 120),
                (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
                (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
                (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
                (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229), (255, 127, 14)]

            Color2 = ['0F3FFF','190EFE','530DFD','8D0CFD','C80BFC','FC0AF5','FB0AB9',
                'FB097D','FA0841','FA0A07','F94506','F98006','F8BB05','F8F604','BCF703',
                '80F703','43F602','06F601','00F537','00F572']



            # Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
            for i in range(len(tableau20)):
                r, g, b = tableau20[i]
                tableau20[i] = (r / 255., g / 255., b / 255.)


            figC, (axC1, axC2, axC3, axC4) = plt.subplots(nrows=4)
            figC.set_size_inches(10, 14)
            title = 'Comparacion de la evolucion del delta angulo en funcion del trial\n' + 'Usuario: '+str(usuario)
            figC.suptitle (title, fontsize=10, fontweight='bold')
            figC.subplots_adjust(hspace=0.5)
            axC1.set_title("Cuadrante 1")
            axC1.set_xlabel('Numero de trial')
            axC1.set_ylabel('Delta angulo')
            axC1.set_color_cycle(tableau20)
            axC2.set_title("Cuadrante 2")
            axC2.set_xlabel('Numero de trial')
            axC2.set_ylabel('Delta angulo')
            axC3.set_title("Cuadrante 3")
            axC3.set_xlabel('Numero de trial')
            axC3.set_ylabel('Delta angulo')
            axC4.set_title("Cuadrante 4")
            axC4.set_xlabel('Numero de trial')
            axC4.set_ylabel('Delta angulo')

        for session in levelsUsuario['sessionInstance'].unique():
            levelSession = levelsUsuario[levelsUsuario['sessionInstance']==session]
            display ('En la session '+ str(fechaLocal(session))+ ' el usuario '+str(usuario)+' jugo '+str(len(levelSession['levelInstance'].unique())) + ' niveles')
            for level in levelSession['levelInstance'].unique():
                levelLevel = levelSession[levelSession['levelInstance']==level]
                # display (levelLevel)
                levelInfo = levelLevel.iloc[0]
                analisisJsonList = levelInfo['analisis']

                for analisisJson in analisisJsonList:

                    if mostrarNivel:
                        # Armamos el grafico de nivel
                        fig1 = plt.figure(figsize=(10,3))
                        ax1 = fig1.add_subplot(111)
                        title = 'Evolucion de la dificultad en funcion del trial \n' + 'Usuario: '+str(usuario) + ' en la referencia: ' + str(analisisJson['anguloDeReferencia']) + ', levelVersion: '+str(levelInfo['levelVersion'])
                        ax1.set_title(title, fontsize=10, fontweight='bold')
                        ax1.set_xlabel('Numero de trial')
                        ax1.set_ylabel('Nivel')

                    if mostrarAngulo:
                        # Armamos el grafico de angulo
                        fig2 = plt.figure(figsize=(10,3))
                        ax2 = fig2.add_subplot(111)
                        title = 'Evolucion del angulo en funcion del trial \n' + 'Usuario: '+str(usuario) + ' en la referencia: ' + str(analisisJson['anguloDeReferencia']) + ', levelVersion: '+str(levelInfo['levelVersion'])
                        ax2.set_title(title, fontsize=10, fontweight='bold')
                        ax2.set_xlabel('Numero de trial')
                        ax2.set_ylabel('Angulo')

                    numeroDeCuadrante=0
                    for cuadrante in analisisJson['cuadrantes']:

                        # Extraemos la info en forma de lista
                        numeroDeCuadrante = numeroDeCuadrante + 1
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
                            # Corregimos el tema de cuadrante para que se vea mas lindo.
                            if angulos[-1] < analisisJson['anguloDeReferencia']:
                                angulos[-1] = angulos[-1] + 360
                            angulosRef = angulosRef + [historial['angulo']['anguloRef']]
                            angulosNivel = angulosNivel + [historial['angulo']['nivel']]

                        if mostrarNivel:
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

                        if mostrarAngulo:
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

                        if mostrarRefrencia:
                            # Dibujamos los angulos referenciados
                            if numeroDeCuadrante==1:
                                    axC=axC1
                            if numeroDeCuadrante==2:
                                    axC=axC2
                            if numeroDeCuadrante==3:
                                    axC=axC3
                            if numeroDeCuadrante==4:
                                    axC=axC4

                            if numeroDeCuadrante == 1:
                                ax = axC1

                            x = range(len(angulos))
                            y = angulosRef
                            axC.plot(x,y, label="Referencia "+str(analisisJson['anguloDeReferencia']))
                            # marcamos aciertos y errores
                            #x = [i for i in range(len(aciertos)) if aciertos[i]]
                            #y = [angulosRef[i] for i in range(len(aciertos)) if aciertos[i]]
                            #axC.plot(x,y,'go')
                            #x = [i for i in range(len(aciertos)) if not aciertos[i]]
                            #y = [angulosRef[i] for i in range(len(aciertos)) if not aciertos[i]]
                            #axC.plot(x,y,'ro')
                            # Marcamos el final si es convergencia o no.
                            if cuadrante['convergenciaAlcanzada']:
                                axC.plot([len(angulosRef)-1],angulosRef[-1],'bs', markersize=10)
                            else:
                                if len(angulos) > 0: # Esto es porque hay datos malos, no deberia hacer falta en gral
                                    axC.plot([len(angulos)-1],angulosRef[-1],'rs', markersize=10)
                            axC.legend(loc='center left', bbox_to_anchor=(1, 0.5))
