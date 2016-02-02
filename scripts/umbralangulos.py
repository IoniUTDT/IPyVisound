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

    mostrarReferencia = True
    mostrarNivel = False
    mostrarAngulo = False

    if completos:
        levels = levels[levels['levelCompleted']]

    for usuario in levels['Alias'].unique():
        display ('Se hara la estadistica del usuario: '+usuario)
        levelsUsuario = levels[levels['Alias']==usuario]
        display ('El usuario '+usuario+' jugo '+str(len(levelsUsuario['sessionInstance'].unique()))+' veces')

        if mostrarReferencia:
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
            figC.set_size_inches(10, 18)
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
            axC2.set_color_cycle(tableau20)
            axC3.set_title("Cuadrante 3")
            axC3.set_xlabel('Numero de trial')
            axC3.set_ylabel('Delta angulo')
            axC3.set_color_cycle(tableau20)
            axC4.set_title("Cuadrante 4")
            axC4.set_xlabel('Numero de trial')
            axC4.set_ylabel('Delta angulo')
            axC4.set_color_cycle(tableau20)

        for session in levelsUsuario['sessionInstance'].unique():
            levelSession = levelsUsuario[levelsUsuario['sessionInstance']==session]
            display ('En la session '+ str(fechaLocal(session))+ ' el usuario '+str(usuario)+' jugo '+str(len(levelSession['levelInstance'].unique())) + ' niveles')
            for level in levelSession['levelInstance'].unique():
                levelLevel = levelSession[levelSession['levelInstance']==level]
                # display (levelLevel)
                levelInfo = levelLevel.iloc[0]
                convergencias = levelInfo['advance']['convergencias']

                for convergencia in convergencias:

                    if mostrarNivel:
                        # Armamos el grafico de nivel
                        fig1 = plt.figure(figsize=(10,3))
                        ax1 = fig1.add_subplot(111)
                        title = 'Evolucion de la dificultad en funcion del trial \n' + 'Usuario: '+str(usuario) + ' en la referencia: ' + str(convergencia['anguloDeReferencia'])
                        ax1.set_title(title, fontsize=10, fontweight='bold')
                        ax1.set_xlabel('Numero de trial')
                        ax1.set_ylabel('Nivel')

                    if mostrarAngulo:
                        # Armamos el grafico de angulo
                        fig2 = plt.figure(figsize=(10,3))
                        ax2 = fig2.add_subplot(111)
                        title = 'Evolucion del angulo en funcion del trial \n' + 'Usuario: '+str(usuario) + ' en la referencia: ' + str(convergencia['anguloDeReferencia'])
                        ax2.set_title(title, fontsize=10, fontweight='bold')
                        ax2.set_xlabel('Numero de trial')
                        ax2.set_ylabel('Angulo')




                    # Extraemos la info en forma de lista
                    aciertos=[]
                    angulosReferido=[]
                    angulos=[]
                    angulosNivel = []
                    for historial in convergencia['historial']:
                        # Extraemos la lista de aciertos o errores de la info del historial
                        if historial['acertado']:
                            aciertos=aciertos+[True]
                        else:
                            aciertos=aciertos+[False]
                        angulos = angulos + [historial['angulo']]
                        # Corregimos el tema de cuadrante para que se vea mas lindo.
                        if angulos[-1] < historial['anguloDeReferencia']:
                            angulos[-1] = angulos[-1] + 360
                        angulosReferido = angulosReferido + [historial['anguloReferido']]
                        angulosNivel = angulosNivel + [historial['nivel']]

                    if mostrarNivel:
                        # Dibujamos los niveles
                        x = range(len(angulosNivel))
                        y = angulosNivel
                        ax1.plot(x,y, label=convergencia['nombreDelCuadrante'])
                        # marcamos aciertos y errores
                        x = [i for i in range(len(aciertos)) if aciertos[i]]
                        y = [angulosNivel[i] for i in range(len(aciertos)) if aciertos[i]]
                        ax1.plot(x,y,'go')
                        x = [i for i in range(len(aciertos)) if not aciertos[i]]
                        y = [angulosNivel[i] for i in range(len(aciertos)) if not aciertos[i]]
                        ax1.plot(x,y,'ro')
                        # Marcamos el final si es convergencia o no.
                        if convergencia['convergenciaAlcanzada']:
                            ax1.plot([len(angulosNivel)-1],angulosNivel[-1],'bs', markersize=10)
                        else:
                            if len(angulosNivel) > 0: # Esto es porque hay datos malos, no deberia hacer falta en gral
                                ax1.plot([len(angulosNivel)-1],angulosNivel[-1],'rs', markersize=10)
                        ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))

                    if mostrarAngulo:
                        # Dibujamos los angulos
                        x = range(len(angulos))
                        y = angulos
                        ax2.plot(x,y, label=convergencia['nombreDelCuadrante'])
                        # marcamos aciertos y errores
                        x = [i for i in range(len(aciertos)) if aciertos[i]]
                        y = [angulos[i] for i in range(len(aciertos)) if aciertos[i]]
                        ax2.plot(x,y,'go')
                        x = [i for i in range(len(aciertos)) if not aciertos[i]]
                        y = [angulos[i] for i in range(len(aciertos)) if not aciertos[i]]
                        ax2.plot(x,y,'ro')
                        # Marcamos el final si es convergencia o no.
                        if convergencia['convergenciaAlcanzada']:
                            ax2.plot([len(angulos)-1],angulos[-1],'bs', markersize=10)
                        else:
                            if len(angulos) > 0: # Esto es porque hay datos malos, no deberia hacer falta en gral
                                ax2.plot([len(angulos)-1],angulos[-1],'rs', markersize=10)
                        ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))

                    if mostrarReferencia:
                        # Dibujamos los angulos referenciados
                        if convergencia['numeroCuadrante']==1:
                                axC=axC1
                        if convergencia['numeroCuadrante']==2:
                                axC=axC2
                        if convergencia['numeroCuadrante']==3:
                                axC=axC3
                        if convergencia['numeroCuadrante']==4:
                                axC=axC4

                        x = range(len(angulos))
                        y = angulosReferido
                        if 'ultimoMEANAngulo' in convergencia:
                            Label = "Referencia "+str(convergencia['anguloDeReferencia']) + " mean(Angulo): " + str(convergencia['ultimoMEANAngulo'])
                        else:
                            Label = "Referencia "+str(convergencia['anguloDeReferencia']) + " mean(Level): " + str(convergencia['ultimoMEAN'])
                        axC.plot(x,y,label=Label, lw=(convergencia['anguloDeReferencia']+45)/90*5)
                        # marcamos aciertos y errores
                        #x = [i for i in range(len(aciertos)) if aciertos[i]]
                        #y = [angulosRef[i] for i in range(len(aciertos)) if aciertos[i]]
                        #axC.plot(x,y,'go')
                        #x = [i for i in range(len(aciertos)) if not aciertos[i]]
                        #y = [angulosRef[i] for i in range(len(aciertos)) if not aciertos[i]]
                        #axC.plot(x,y,'ro')
                        # Marcamos el final si es convergencia o no.
                        if convergencia['convergenciaAlcanzada']:
                            axC.plot([len(angulosReferido)-1],angulosReferido[-1],'bs', markersize=10)
                        else:
                            if len(angulos) > 0: # Esto es porque hay datos malos, no deberia hacer falta en gral
                                axC.plot([len(angulos)-1],angulosReferido[-1],'rs', markersize=10)
                        axC.legend(loc='center left', bbox_to_anchor=(1, 0.5),prop={'size':10})


def levelsToDF (levels, completo=True):

    import pandas as pd
    from IPython.display import display

    # Tiramos cosas que no nos interesan
    # levels.drop(['setup','timeLevelStarts','timeLevelExit'],inplace=True,axis=0)

    # Creamos el formato basico del data frame
    dfCreado = False
    # Iteramos sobre todas las entradas de niveles jugados
    for (i,row) in levels.iterrows():

        # Buscamos la info de las convergencias (por alguna razon hay dos capas de datos anidadas para nada pero vienen asi los datos)
        advance = row['advance']
        convergencias = advance['convergencias']

        # Iteramos sobre cada una de las convergencias
        for convergencia in convergencias:

            # Recatamos la info de los historiales (lo que el usuario fue respondiendo dentro de cada convergencia)
            historial = convergencia['historial']
            # Creamos un dataframe con la lista de angulos respondidos
            angulosDF = pd.DataFrame(historial)
            # Numeramos los angulos segun esta en el historial (para que las secuenciacis de graficos queden bien)
            angulosDF['indiceEnHistorial'] = angulosDF.index

            # Agregamos toa la info de la convergencia en gral.
            angulosDF['ultimaSD']=convergencia['ultimaSD']
            angulosDF['cuadranteNumero']=convergencia['numeroCuadrante']
            angulosDF['ultimoMEANNivel']=convergencia['ultimoMEAN']
            if 'ultimoMEANAngulo' in convergencia.keys():
                angulosDF['ultimoMEANAngulo']=convergencia['ultimoMEANAngulo']
            angulosDF['convergenciaAlcanzada']=convergencia['convergenciaAlcanzada']
            angulosDF['anguloDeReferencia_C']=convergencia['anguloDeReferencia'] # Mantenemos un nombre diferente para no sobreescribir la info que viene de cada angulo. Deberian coincidir, peor es bueno poider chequearlo.
            angulosDF['nombreDelCuadrante']=convergencia['nombreDelCuadrante']

            # Agregamos toda la info de la convergencia
            angulosDF['levelCompleted'] = row['levelCompleted']
            angulosDF['levelInstance'] = row['levelInstance']
            angulosDF['levelTitle'] = row['levelTitle']
            angulosDF['sessionInstance'] = row['sessionInstance']
            angulosDF['appVersion'] = row['appVersion']
            angulosDF['codeVersion'] = row['codeVersion']
            angulosDF['levelVersion'] = row['levelVersion']
            angulosDF['resourcesVersion'] = row['resourcesVersion']
            angulosDF['userID'] = row['userID']
            angulosDF['Alias'] = row['Alias']


            # agregamos la lista extraida de cada convergencia en el dataframe principal
            if dfCreado:
                analisisUmbralAngulosDF = pd.concat([analisisUmbralAngulosDF, angulosDF], ignore_index=True)
            else:
                analisisUmbralAngulosDF = angulosDF
                dfCreado = True

    return analisisUmbralAngulosDF


def plotConvergenciaXCuadrantes (dataframe, agruparXusuario=False) :

    """
        Este script grafica cada convergencia uniendo todas las convergencias correspondientes a un mismo cuadrante
    """
    import matplotlib.pyplot as plt
    from scripts.general import fechaLocal
    from IPython.display import display

    from scripts.general import chkVersion
    chkVersion()

    # Creamos una lista de colores linda
    # These are the "Tableau 20" colors as RGB.
    tableau20 = [(31, 119, 180), (174, 199, 232), (255, 187, 120),
        (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
        (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
        (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
        (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229), (255, 127, 14)]
    # Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
    for i in range(len(tableau20)):
        r, g, b = tableau20[i]
        tableau20[i] = (r / 255., g / 255., b / 255.)

    for usuario in dataframe['Alias'].unique():
        # Limitamos el dataframe al usuarios
        dataframeUsuario = dataframe[dataframe['Alias']==usuario]

        # Retocamos la info para que se adecue a los graficos que queremos
        dataframeUsuario[dataframeUsuario['angulo']<dataframeUsuario['anguloDeReferencia']]['angulo'] = dataframeUsuario['angulo'] + 360

        # Creamos los graficos
        figC, (axC1, axC2, axC3, axC4) = plt.subplots(nrows=4)
        figC.set_size_inches(10, 18)
        title = 'Comparacion de la evolucion del delta angulo en funcion del trial\n' + 'Usuario: '+str(usuario)
        figC.suptitle (title, fontsize=10, fontweight='bold')
        figC.subplots_adjust(hspace=0.5)

        # Reportamos un resumen
        display ('Se hara la estadistica del usuario: '+usuario)
        display ('El usuario '+usuario+' jugo '+str(len(dataframeUsuario['sessionInstance'].unique()))+' veces')

        # Repetimos la secuencia para cada cuadrante
        for i in [1,2,3,4]:
            # filtramos los datos correspondientes al cuadrante
            dfUserCuadrante = dataframeUsuario[dataframeUsuario['cuadranteNumero']==i]

            # Preparamos el grafico del cuadrante
            if i==1:
                ax = axC1
            if i==2:
                ax = axC2
            if i==3:
                ax = axC3
            if i==4:
                ax = axC4

            ax.set_title("Cuadrante " + str(i))
            ax.set_xlabel('Numero de trial')
            ax.set_ylabel('Delta angulo')
            ax.set_color_cycle(tableau20)


            # Armamos una lista de todas las orientaciones ordenadas
            listaReferencias = dfUserCuadrante['anguloDeReferencia'].unique()
            listaReferencias.sort()
            listaReferencias[:] = listaReferencias[::-1]

            # Agregamos las lineas que corresponden a cada referencia
            for referencia in listaReferencias:
                # filtramos x referencia
                dfUserCuadranteReferencia = dfUserCuadrante[dfUserCuadrante['anguloDeReferencia']==referencia]
                # Revisamos si hay mas de una linea xq se jugo mas de una vez el nivel
                for levelintance in dfUserCuadranteReferencia['levelInstance'].unique():
                    # Filtramos por intancia de nivel
                    dfUserCuadranteReferenciaInstance = dfUserCuadranteReferencia[dfUserCuadranteReferencia['levelInstance']==levelintance]
                    # Nos aseguramos que esten bien ordenados los datos
                    dfUserCuadranteReferenciaInstance.sort(['indiceEnHistorial'])

                    # Cargamos las x y las y
                    x = dfUserCuadranteReferenciaInstance['indiceEnHistorial']
                    y = dfUserCuadranteReferenciaInstance['anguloReferido']

                    # Agregamos la linea
                    Label = "Referencia "+str(dfUserCuadranteReferenciaInstance['anguloDeReferencia'].iloc[0]) + " mean(Angulo): " + str(dfUserCuadranteReferenciaInstance['ultimoMEANAngulo'].iloc[0])
                    ax.plot(x,y,label=Label, lw=(dfUserCuadranteReferenciaInstance['anguloDeReferencia'].iloc[0]+45)/90*5)
                    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),prop={'size':8})
