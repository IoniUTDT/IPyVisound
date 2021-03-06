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



def plotConvergenciaXReferencia (dataframe) :
    """
        este script grafica como evoluciona la aproximacion a los angulos rectos en funcion de la referencia
    """

    import matplotlib.pyplot as plt
    from scripts.general import fechaLocal
    from IPython.display import display

    from scripts.general import chkVersion
    chkVersion()

    # Cargamos una tabla de colores
    tableau20 = [(31, 119, 180), (255, 187, 120),
        (152, 223, 138), (255, 152, 150),
        (197, 176, 213), (196, 156, 148),
        (247, 182, 210), (199, 199, 199),
        (219, 219, 141), (158, 218, 229)]
    # Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
    for i in range(len(tableau20)):
        r, g, b = tableau20[i]
        tableau20[i] = (r / 255., g / 255., b / 255.)

    colores = []
    for color in tableau20:
        colores = colores + [color] + [color] + [color] + [color]


    # Se hace un grafico para cada referencia donde se juntan las cuadro convergencias de todos los usuarios
    listaReferencias = dataframe['anguloDeReferencia'].unique()
    listaReferencias.sort()
    for referencia in listaReferencias:
        # Filtramos los datos correspondientes a una referencia
        dfRef = dataframe[dataframe['anguloDeReferencia']==referencia]
        # Creamos el grafico
        fig = plt.figure(figsize=(10,3))
        ax = fig.add_subplot(111)
        title = 'Evolucion del angulo en funcion del trial \n' + ' en la referencia: ' + str(referencia)
        ax.set_title(title, fontsize=10, fontweight='bold')
        ax.set_xlabel('Numero de trial')
        ax.set_ylabel('Angulo')
        ax.set_color_cycle(colores)


        # Buscamos el conjunto de las cuatro convergencias para cada levelInstance
        for i,instance in enumerate(dfRef['levelInstance'].unique()) :
            # filtramos los datos x intancia
            dfRefInst = dfRef[dfRef['levelInstance'] == instance]

            # Buscamos la info de cada cuadrante
            for cuadrante in [1,2,3,4]:
                dfRefInstCuad = dfRefInst[dfRefInst['cuadranteNumero']==cuadrante]
                # nos asegurmos que esten ordenados los datos
                dfRefInstCuad.sort(['indiceEnHistorial'])

                # correjimos los numeros para que quede todo centrado alrededor del 90
                if cuadrante == 1:
                    #dfRefInstCuad['anguloReferidoPlot'] = dfRefInstCuad['anguloReferido']
                    dfRefInstCuad['ultimoMEANAnguloPlot'] = 90 - dfRefInstCuad['ultimoMEANAngulo']
                if cuadrante == 2:
                    #dfRefInstCuad['anguloReferidoPlot'] = dfRefInstCuad['anguloReferido']
                    dfRefInstCuad['ultimoMEANAnguloPlot'] = dfRefInstCuad['ultimoMEANAngulo'] - 90
                if cuadrante == 3:
                    #dfRefInstCuad['anguloReferidoPlot'] = dfRefInstCuad['anguloReferido'] - 180
                    dfRefInstCuad['ultimoMEANAnguloPlot'] = 270 - dfRefInstCuad['ultimoMEANAngulo']
                if cuadrante == 4:
                    #dfRefInstCuad['anguloReferidoPlot'] = dfRefInstCuad['anguloReferido'] - 180
                    dfRefInstCuad['ultimoMEANAnguloPlot'] = dfRefInstCuad['ultimoMEANAngulo'] - 270

                # Cargamos los datos a graficar
                x = dfRefInstCuad['indiceEnHistorial']
                y = dfRefInstCuad['anguloReferido']
                Label = "Cuadrante: " + str(cuadrante) + " User: " + dfRefInstCuad['Alias'].iloc[0]
                tamano = (dfRef['levelInstance'].unique().size - i) / (0.25 * dfRef['levelInstance'].unique().size)

                ax.plot(x,y,label=Label, lw=tamano)
                # Agregamos la marca de la convergencia
                x = dfRefInstCuad['indiceEnHistorial'].iloc[-1]
                y = dfRefInstCuad['anguloReferido'].iloc[-1]
                if dfRefInstCuad['convergenciaAlcanzada'].iloc[-1]:
                    ax.plot(x,y,'bs', markersize=10)
                else:
                    ax.plot(x,y,'rs', markersize=10)
                ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))


        # Graficamos una linea roja
        xmin, xmax = ax.get_xlim()
        ax.plot ([0,xmax] , [90,90] , 'r-')
        ax.plot ([0,xmax] , [270,270] , 'r-')


def plotUmbralVsReferencia (dataframe) :
    """
        Muestra cuanto vale el umbral en funcion de la orientacion del angulo (toma como referencia el lado fijo)
        El cuadrante 1 se complementa con el 3 y el 2 con el 4.
    """

    import matplotlib.pyplot as plt
    from scripts.general import fechaLocal
    from IPython.display import display
    import pandas as pd
    import numpy as np

    from scripts.general import chkVersion
    chkVersion()

    display(dataframe.keys())

    # Iteramos sobre los usuarios
    for user in dataframe['Alias'].unique():

        # Armamos los graficos
        fig, graficos = plt.subplots(2, 1, subplot_kw=dict(projection='polar'))
        fig.set_size_inches(10,20)
        graficos[0].set_title('Aproximacion desde angulos agudos')
        graficos[1].set_title('Aproximacion desde angulos obtusos')
        fig.suptitle('Nivel de umbral (en grados) de deteccion de angulos rectos\n en funcion de la oriertacion del lado fijo \n usuario: '+user)

        dataByUser=dataframe[dataframe['Alias']==user]
        # Iteramos sobre las referencias
        referencias = dataByUser['anguloDeReferencia'].unique()
        referencias.sort()
        umbralC1 = []
        umbralC2 = []
        umbralC3 = []
        umbralC4 = []
        for referencia in referencias:
            dataByUserByRef = dataByUser[dataByUser['anguloDeReferencia']==referencia]
            #display (dataByUserByRef[dataByUserByRef['cuadranteNumero']==3])
            umbralC1 = umbralC1 + [90 - float(dataByUserByRef[dataByUserByRef['cuadranteNumero']==1]['anguloReferido'].tail(1))]
            umbralC2 = umbralC2 + [float(dataByUserByRef[dataByUserByRef['cuadranteNumero']==2]['anguloReferido'].tail(1)) - 90]
            umbralC3 = umbralC3 + [270 - float(dataByUserByRef[dataByUserByRef['cuadranteNumero']==3]['anguloReferido'].tail(1))]
            umbralC4 = umbralC4 + [float(dataByUserByRef[dataByUserByRef['cuadranteNumero']==4]['anguloReferido'].tail(1)) - 270]

        referenciasRadianes = [value * np.pi / 180 + np.pi/2 for value in referencias]
        referenciasRadianes2 = [value * np.pi / 180 + np.pi + np.pi/2 for value in referencias]
        graficos[0].plot(referenciasRadianes,umbralC1)
        graficos[0].plot(referenciasRadianes2,umbralC4)
        graficos[1].plot(referenciasRadianes,umbralC2)
        graficos[1].plot(referenciasRadianes2,umbralC3)

        fig.savefig('AngulosUmbral'+user+'.png')
        plt.show()

def plotConvergenciaXCuadrantes (dataframe) :

    """
        Este script grafica cada convergencia uniendo todas las convergencias correspondientes a un mismo cuadrante
    """
    import matplotlib.pyplot as plt
    from scripts.general import fechaLocal
    from IPython.display import display
    import numpy as np

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
        figC, (ax) = plt.subplots(nrows=1)
        figC.set_size_inches(10, 18)
        title = 'Comparacion de la evolucion del delta angulo en funcion del trial\n' + 'Usuario: '+str(usuario)
        figC.suptitle (title, fontsize=10, fontweight='bold')
        figC.subplots_adjust(hspace=0.5)

        # Reportamos un resumen
        display ('Se hara la estadistica del usuario: '+usuario)
        display ('El usuario '+usuario+' jugo '+str(len(dataframeUsuario['sessionInstance'].unique()))+' veces')

        # Repetimos la secuencia para cada cuadrante
        for i in [4,3,2,1]:
            # filtramos los datos correspondientes al cuadrante
            dfUserCuadrante = dataframeUsuario[dataframeUsuario['cuadranteNumero']==i]

            ax.set_xlabel('Numero de trial')
            ax.set_ylabel('Angulo')
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
                    if i == 1:
                        mean = 90 - dfUserCuadranteReferenciaInstance['ultimoMEANAngulo'].iloc[-1]
                    if i == 2:
                        mean = dfUserCuadranteReferenciaInstance['ultimoMEANAngulo'].iloc[-1] - 90
                    if i == 3:
                        mean = 270 - dfUserCuadranteReferenciaInstance['ultimoMEANAngulo'].iloc[-1]
                    if i == 4:
                        mean = dfUserCuadranteReferenciaInstance['ultimoMEANAngulo'].iloc[-1] - 270

                    Label = "Referencia "+str(dfUserCuadranteReferenciaInstance['anguloDeReferencia'].iloc[0]) + " media al objetivo (grados): " + str(mean)
                    ax.plot(x,y,label=Label, lw=(dfUserCuadranteReferenciaInstance['anguloDeReferencia'].iloc[0]+45)/90*5, alpha=0.2)
                    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),prop={'size':8})

                    # Agregamos la marca de la convergencia
                    x = dfUserCuadranteReferenciaInstance['indiceEnHistorial'].iloc[-1]
                    y = dfUserCuadranteReferenciaInstance['anguloReferido'].iloc[-1]
                    if dfUserCuadranteReferenciaInstance['convergenciaAlcanzada'].iloc[-1]:
                        ax.plot(x,y,'bs', markersize=10, alpha=0.2)
                    else:
                        ax.plot(x,y,'rs', markersize=10, alpha=0.2)

            # Agregamos una linea que sea el valor medio de todos las referenciados

            x = []
            y = []
            colores = ['gray', 'blue', 'gray', 'blue']
            #display (dfUserCuadrante['indiceEnHistorial'].unique())
            #display (dfUserCuadrante[dfUserCuadrante['indiceEnHistorial']==0]['anguloReferido'].mean())
            for indice in dfUserCuadrante['indiceEnHistorial'].unique():
                if len (dfUserCuadrante[dfUserCuadrante['indiceEnHistorial']==indice].index) > 5:
                    x = x + [indice]
                    y = y + [dfUserCuadrante[dfUserCuadrante['indiceEnHistorial']==indice]['anguloReferido'].mean()]
            if len(y) > 10 :
                media = np.mean(y[10::])
                if i == 1: media = 90 - media
                if i == 2: media = media - 90
                if i == 3: media = 270 - media
                if i == 4: media = media - 270
                Label = " Valor medio de todas las curvas (cuadrante: " + str(i) + ")" + "\n Distancia media (a partir del trial 10) al objetivo: " + str(media)
                ax.plot(x,y,label=Label, lw=3, color = colores[i-1])
                lgd = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),prop={'size':8})

        # Agregamos una linea de referencia
        xmin, xmax = ax.get_xlim()
        ax.plot ([0,xmax] , [90,90] , 'r-')
        ax.plot ([0,xmax] , [270,270] , 'r-')

        # Agregamos cartelitos que indiquen el cuadrante
        ax.annotate('Cuadrante 1', xy=(xmax/2, 45))
        ax.annotate('Cuadrante 2', xy=(xmax/2, 135))
        ax.annotate('Cuadrante 3', xy=(xmax/2, 225))
        ax.annotate('Cuadrante 4', xy=(xmax/2, 315))

        figC.savefig('XCuadrante'+usuario, bbox_extra_artists=(lgd,), bbox_inches='tight')

def plotHistogramas (dataframe, agruparUsuarios=True):
    import matplotlib.pyplot as plt
    from scripts.general import fechaLocal
    from IPython.display import display
    import numpy as np
    import pandas as pd

    from scripts.general import chkVersion
    chkVersion()

    # Agregamos la info de que categoria es el angulo que va a ser necesaria para las cuentas.
    display (dataframe.columns)
    dataframe[dataframe['anguloReferido']==5]['Categoria'] = "Grande"
    display (dataframe['anguloReferido'].unique())
    display (dataframe.columns)
    # Armamos la lista de dataframes separados por usuario o no segun corresponda
    datos = []
    if agruparUsuarios:
        datos = [dataframe]
    else:
        for usuario in dataframe['Alias'].unique():
            datos = datos + [dataframe[dataframe['Alias']==usuario]]

    # Ahora procesamos los datos
    estadistica = pd.DataFrame()
    for dato in datos:
        # Para cada angulo referido (unificando en todas las referencias y en todas las intancias) hacemos la estadistica
        # Angulo referido es el "x" de este grafico
        for anguloReferido in dato['anguloReferido'].unique():
            pass
