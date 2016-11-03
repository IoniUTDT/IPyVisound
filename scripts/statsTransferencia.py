import scripts.constants as cts

from IPython.display import display
from scripts.db import dataProcesada


def filtroEtapaUno(data):
    listaDeTrialsARemover = []
    for levelInstance in data[cts.P_LevelInstance].unique():
        dataParcial = data[data[cts.P_LevelInstance] == levelInstance]
        if dataParcial[cts.P_LevelIdentificador].iloc[0] in cts.expListToCut:
            nivelAAlcanzar = dataParcial[cts.P_NivelEstimuloDinamica].iget(-1)
            for index in dataParcial.index:
                if dataParcial.ix[index][cts.P_NivelEstimuloDinamica] >= nivelAAlcanzar:
                    listaDeTrialsARemover = listaDeTrialsARemover + [index]
                else:
                    break
    return data[-data.index.isin(listaDeTrialsARemover)]


def significanciaAciertos(data):

    import scipy
    import scipy.stats
    import pylab

    n = len(data.index)
    display(n)
    p = 2/3
    x = scipy.linspace(0, n, n+1)
    distribucion = scipy.stats.binom.pmf(x, n, p)
    numeroAciertos = len(data[data[cts.P_RtaCorrecta]])
    display('Respuestas correctas:' + str(numeroAciertos))
    display('Probabilidad para el numero de respuestas correctas: ' + str(distribucion[numeroAciertos]))
    pylab.plot(x, distribucion)

"""
def filtroSignificanciaDesdeAtras (data):

    pValueLimite = 0.05
    validezEstadistica = pandas.DataFrame()

    for levelInstance in data[cts.P_LevelInstance].unique():
        validezEstadistica['levelInstance'] = levelInstance
        dataInstance = data[data[cts.P_LevelInstance]==levelInstance]
        for largo in range(len(dataInstance.index)):
            #display (largo)
"""


def lastTrialsOfLevels(data=None):

    if not data:
        users, data = dataProcesada()

    listOfIndex = []
    for levelInstance in data[cts.P_LevelInstance].unique():
        listOfIndex += [data[data[cts.P_LevelInstance] == levelInstance].index[-1]]
    data = data.loc[listOfIndex]
    data = data[[cts.P_UserId, cts.P_Alias, cts.P_LevelIdentificador, cts.P_FaseActiva, cts.P_OrientacionEntrenamiento, cts.P_NivelEstimuloDinamica, cts.P_LevelInstance, cts.P_SessionInstance]]

    return data

def filterData (data=None):

    if not data:
        data = lastTrialsOfLevels(data)

    # Agregamos los valores que faltan porque se cerro la app a mano.

    # Datos Carolina
    entrada = {cts.P_UserId : 1472735163595, cts.P_Alias : 'ExpT_Carolina', cts.P_LevelIdentificador : 'ENTRENAMIENTOA30INICIAL', cts.P_FaseActiva : 'Entrenamiento1', cts.P_OrientacionEntrenamiento : 'A30', cts.P_NivelEstimuloDinamica : 50, cts.P_LevelInstance : 1473262953600, cts.P_SessionInstance : 1473263015372}
    data = data.append(entrada, ignore_index=True)
    data.set_value(data[data[cts.P_SessionInstance] == 1473428568035].index[0], cts.P_FaseActiva, 'Entrenamiento3') # Ojo que esta linea es sensible a que se reordenen los rows!
    data.set_value(data[data[cts.P_LevelInstance] == 1472736027552].index[0], cts.P_FaseActiva, 'Tutorial') # Ojo que esta linea es sensible a que se reordenen los rows!

    # Datos Magdalena
    entrada = {cts.P_UserId : 1473080810935, cts.P_Alias : 'ExpT_Magdalena', cts.P_LevelIdentificador : 'ENTRENAMIENTOP30INICIAL', cts.P_FaseActiva : 'Entrenamiento4', cts.P_OrientacionEntrenamiento : 'P30', cts.P_NivelEstimuloDinamica : 37, cts.P_LevelInstance : 1473860983609, cts.P_SessionInstance : 1473861042758}
    data = data.append(entrada, ignore_index=True)

    # Datos Enzo
    entrada = {cts.P_UserId : 1473271930369, cts.P_Alias : 'ExpT_Enzo', cts.P_LevelIdentificador : 'ENTRENAMIENTOP30INICIAL', cts.P_FaseActiva : 'Entrenamiento2', cts.P_OrientacionEntrenamiento : 'P30', cts.P_NivelEstimuloDinamica : 31, cts.P_LevelInstance : 1473708413322, cts.P_SessionInstance : 1473708454534}
    data = data.append(entrada, ignore_index=True)

    # Datos Andres
    data.set_value(data[data[cts.P_SessionInstance] == 1474925502990].index[8], cts.P_FaseActiva, 'TestInicial') # Ojo que esta linea es sensible a que se reordenen los rows!

    # Datos CaroG
    data.set_value(data[data[cts.P_LevelInstance] == 1475071684887].index[0], cts.P_FaseActiva, 'TestInicial') # Ojo que esta linea es sensible a que se reordenen los rows!
    data.set_value(data[data[cts.P_LevelInstance] == 1475071227020].index[0], cts.P_FaseActiva, 'TestInicial') # Ojo que esta linea es sensible a que se reordenen los rows!
    data.set_value(data[data[cts.P_LevelInstance] == 1475071488650].index[0], cts.P_FaseActiva, 'TestInicial') # Ojo que esta linea es sensible a que se reordenen los rows!
    data.set_value(data[data[cts.P_LevelInstance] == 1475069748509].index[0], cts.P_FaseActiva, 'Tutorial') # Ojo que esta linea es sensible a que se reordenen los rows!
    data.set_value(data[data[cts.P_LevelInstance] == 1475069872252].index[0], cts.P_FaseActiva, 'Tutorial') # Ojo que esta linea es sensible a que se reordenen los rows!

    # Datos Julieta
    data.set_value(data[data[cts.P_LevelInstance] == 1473953334128].index[0], cts.P_FaseActiva, 'Tutorial') # Ojo que esta linea es sensible a que se reordenen los rows!

    return data

def resumeByUsers(data=None,escalaEnAngulos = False, diferencias=False):

    from matplotlib.backends.backend_pdf import PdfPages
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import datetime

    if data:
        resumen = dataNumerica(data)
    else:
        resumen = dataNumerica()

    # Generamos las etiquetas
        etiquetasTest = ['P30', 'P60', 'P120', 'P150', 'A30', 'A60', 'A120', 'A150']
        etiquetasEntrenamiento = ['Dia1', 'Dia2', 'Dia3', 'Dia4']

    # Creamos el pdf con todos los graficoados
    #pp = PdfPages("./Images/TransferenciaResultados ("+ datetime.date.today().strftime("%B %d, %Y") +").pdf")

    # Creamos un lienzo con todos los graficoados
    f, axarr = plt.subplots(len (resumen.keys()),2)
    f.set_size_inches(20, 2.5 * len (resumen.keys()))
    #f.tight_layout()
    f.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.4, hspace=0.4)
    f.subplots_adjust(top=1)
    i = 0
    for alias, resultado in resumen.items():

        valoresTestInicial = resultado['TestInicial']
        valoresTestFinal = resultado['TestFinal']
        valoresTestDiferencia = resultado['Evolucion']

        valoresTestInicialEnAngulos = resultado['TestInicialAngulos']
        valoresTestFinalEnAngulos = resultado['TestFinalAngulos']
        valoresTestDiferenciaEnAngulo = resultado['EvolucionAngulos']

        valoresEntrenamientoInicial = resultado['EntrenamientoInicial']
        valoresEntrenamientoIntermedio = resultado['EntrenamientoMedio']
        valoresEntrenamientoFinal = resultado['EntrenamientoFinal']

        valoresEntrenamientoInicialEnAngulos = resultado['EntrenamientoInicialEnAngulos']
        valoresEntrenamientoIntermedioEnAngulos = resultado['EntrenamientoMedioEnAngulos']
        valoresEntrenamientoFinalEnAngulos = resultado['EntrenamientoFinalEnAngulos']

        # Creamos las dos figuras para el usuario
        # fig = axarr[i]
        # fig = plt.figure(figsize=(20,2))
        # fig.set_title("Usuario: " + cts.mapNames[alias] + ". Entrenamiento: " + resultado['Orientacion'], fontsize=12)
        # fig.subplots_adjust(top=0.85)


        if escalaEnAngulos:
            valoresTestInicialUnificado = valoresTestInicialEnAngulos
            valoresTestFinalUnificado = valoresTestFinalEnAngulos
            valoresTestDiferenciaUnificado = valoresTestDiferenciaEnAngulo
        else:
            valoresTestInicialUnificado = valoresTestInicial
            valoresTestFinalUnificado = valoresTestFinal
            valoresTestDiferenciaUnificado = valoresTestDiferencia

        valoresTestDiferenciaUnificadoPos = valoresTestDiferenciaUnificado
        valoresTestDiferenciaUnificadoNeg = [- value for value in valoresTestDiferenciaUnificado]

        # Creamos el grafico de test
        #figuraTest = plt.subplot(121)
        figuraTest = axarr[i,0]
        #figuraTest.set_title("Usuario: " + cts.mapNames[alias], fontsize=12)
        n_groups = 8
        index = np.arange(n_groups)
        if diferencias:
            bar_width = 0.25
        else:
            bar_width = 0.4
        opacity = 0.4
        rects1 = figuraTest.bar(index, valoresTestInicialUnificado, bar_width,
                 alpha=opacity * 0.5,
                 color='b',
                 label='Test Inicial')
        rects2 = figuraTest.bar(index + bar_width, valoresTestFinalUnificado, bar_width,
                 alpha=opacity * 2,
                 color='b',
                 label='TestFinal')
        if diferencias:
            rects3 = figuraTest.bar(index + bar_width*2, valoresTestDiferenciaUnificadoPos, bar_width,
                     alpha=opacity * 2,
                     color='g',
                     label='Evolucion positiva')
            rects4 = figuraTest.bar(index + bar_width*2, valoresTestDiferenciaUnificadoNeg, bar_width,
                     alpha=opacity * 2,
                     color='r',
                     label='Evolucion negativa')
        figuraTest.set_xlabel('Orientacion')

        if escalaEnAngulos:
            figuraTest.set_ylabel('Umbral de detección (angulo)')
        else:
            figuraTest.set_ylabel('Performance (estimulos)')
        figuraTest.set_title('Comparacion test inicial y final ' + '('+"Usuario: " + alias+')')
        plt.sca(axarr[i, 0])
        plt.xticks(index + bar_width, etiquetasTest)
        figuraTest.legend(bbox_to_anchor=(0.95, 1), loc=2, borderaxespad=0.)
        if escalaEnAngulos:
            figuraTest.set_ylim([0,100])
        else:
            figuraTest.set_ylim([0,200])

        # Remarcamos el entrenamiento
        MaxA = 80
        MaxP = 100
        pasos = 200
        if escalaEnAngulos:
            MaxCuadraditoA = MaxA
            MaxCuadraditoP = MaxP
        else:
            MaxCuadraditoA = pasos
            MaxCuadraditoP = pasos

        if diferencias:
            ancho = 0.75
        else:
            ancho = 0.8

        if resultado['Orientacion'] == 'P30':
            figuraTest.add_patch(
                patches.Rectangle(
                    (0, 0),
                    ancho,
                    MaxCuadraditoP,
                    fill=False,      # remove background
                    edgecolor="red"
                )
            )
        if resultado['Orientacion'] == 'A30':
            figuraTest.add_patch(
                patches.Rectangle(
                    (4, 0),
                    ancho,
                    MaxCuadraditoA,
                    fill=False,      # remove background
                    edgecolor="red"
                )
            )



        # Grafico de entreamiento
        figuraEntrenamiento = axarr[i,1]
        # figuraEntrenamiento = plt.subplot(122)
        n_groups = 4
        index = np.arange(n_groups)
        bar_width = 0.25
        opacity = 0.4

        if escalaEnAngulos:
            valoresEntrenamientoInicial = valoresEntrenamientoInicialEnAngulos
            valoresEntrenamientoIntermedio = valoresEntrenamientoIntermedioEnAngulos
            valoresEntrenamientoFinal = valoresEntrenamientoFinalEnAngulos
        else:
            valoresEntrenamientoInicial = valoresEntrenamientoInicial
            valoresEntrenamientoIntermedio = valoresEntrenamientoIntermedio
            valoresEntrenamientoFinal = valoresEntrenamientoFinal

        rects1 = figuraEntrenamiento.bar(index, valoresEntrenamientoInicial, bar_width,
                 alpha=opacity*0.5,
                 color='b',
                 label='Entrenamiento inicial con feedback (100 trials)')
        rects2 = figuraEntrenamiento.bar(index + bar_width, valoresEntrenamientoIntermedio, bar_width,
                 alpha=opacity,
                 color='b',
                 label='Entrenamiento intermedio sin feedback (50 trials)')
        rects3 = figuraEntrenamiento.bar(index + bar_width*2, valoresEntrenamientoFinal, bar_width,
                alpha=opacity*2,
                color='b',
                label='Entrenamiento final con feedback (100 trials)')

        figuraEntrenamiento.set_xlabel('Sesion')
        if escalaEnAngulos:
            figuraEntrenamiento.set_ylabel('Umbral de detección (angulo)')
        else:
            figuraEntrenamiento.set_ylabel('Performance (estimulos)')
        #plt.ylabel('Performance')

        figuraEntrenamiento.set_title('Evolucion de performance en entrenamiento' + '('+"Usuario: " + alias+')')
        plt.sca(axarr[i, 1])
        plt.xticks(index + 1.5 * bar_width, etiquetasEntrenamiento)
        #figuraEntrenamiento.set_xticklabels(index + 1.5 * bar_width, etiquetasEntrenamiento)
        figuraEntrenamiento.legend(bbox_to_anchor=(0.95, 1), loc=2, borderaxespad=0.)
        if escalaEnAngulos:
            figuraEntrenamiento.set_ylim([0,100])
        else:
            figuraEntrenamiento.set_ylim([0,200])

        # pp.savefig(fig, dpi = 300, transparent = True)
        i += 1

    if escalaEnAngulos:
        f.savefig('./Images/TransferenciaResultadosEnAngulos', bbox_inches='tight')
    else:
        f.savefig('./Images/TransferenciaResultados', bbox_inches='tight')
    #pp.close()


def resumeByUsersNuevo(data=None, escalaEnAngulos = True, diferencias=False):

    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import datetime

    if data:
        resumen = dataNumerica(data)
    else:
        resumen = dataNumerica()

    # Generamos las etiquetas
        etiquetasTest = ['P30', 'P60', 'P120', 'P150', 'A30', 'A60', 'A120', 'A150']
        etiquetasEntrenamiento = ['Test Inicial', 'Dia1', 'Dia2', 'Dia3', 'Dia4', 'TestFinal']

    # Creamos un lienzo con todos los graficoados
    f, axarr = plt.subplots(nrows=len(resumen.keys()),ncols=2,sharex=True, sharey=True,
                           figsize=(20,2.5 * len (resumen.keys())))

    #f.tight_layout()
    f.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0, hspace=0)

    # Variables que permiten ordenar las figuras

    par=0
    ang=3
    sin=5

    for alias, resultado in resumen.items():

        if resultado['Orientacion'] == 'CONTROL':
            i = sin
            print ('CONTROL' + str(i))
            sin = sin + 1
        if resultado['Orientacion'] == 'P30':
            i = par
            print ('P30' + str(i))
            par = par + 1
        if resultado['Orientacion'] == 'A30':
            i = ang
            print ('A30' + str(i))
            ang = ang + 1


        valoresTestInicial = resultado['TestInicial']
        valoresTestFinal = resultado['TestFinal']

        valoresTestInicialEnAngulos = resultado['TestInicialAngulos']
        valoresTestFinalEnAngulos = resultado['TestFinalAngulos']

        valoresEntrenamientoInicial = resultado['EntrenamientoInicial']
        valoresEntrenamientoIntermedio = resultado['EntrenamientoMedio']
        valoresEntrenamientoFinal = resultado['EntrenamientoFinal']

        valoresEntrenamientoInicialEnAngulos = resultado['EntrenamientoInicialEnAngulos']
        valoresEntrenamientoIntermedioEnAngulos = resultado['EntrenamientoMedioEnAngulos']
        valoresEntrenamientoFinalEnAngulos = resultado['EntrenamientoFinalEnAngulos']

        if escalaEnAngulos:
            valoresTestInicialUnificado = valoresTestInicialEnAngulos
            valoresTestFinalUnificado = valoresTestFinalEnAngulos
        else:
            valoresTestInicialUnificado = valoresTestInicial
            valoresTestFinalUnificado = valoresTestFinal

        #figuraTest = plt.subplot(121)
        figuraTest = axarr[i,0]
        n_groups = 8
        index = np.arange(n_groups)
        bar_width = 0.4
        opacity = 0.4

        rects1 = figuraTest.bar(index, valoresTestInicialUnificado, bar_width,
                 alpha=opacity * 0.5,
                 color='b',
                 label='Test Inicial')
        rects2 = figuraTest.bar(index + bar_width, valoresTestFinalUnificado, bar_width,
                 alpha=opacity * 2,
                 color='b',
                 label='TestFinal')
        figuraTest.set_xlabel('Categoría y orientación')

        if escalaEnAngulos:
            figuraTest.set_ylabel('Umbral de detección (ángulo)')
        else:
            figuraTest.set_ylabel('Performance (estímulos)')

        if i==0:
            figuraTest.set_title('Comparacion test inicial y final según categoria y orientación')
            figuraTest.legend(bbox_to_anchor=(0.95, 1), loc=1, borderaxespad=0.)

        # plt.sca(axarr[i, 0])
        if i==10:
            figuraTest.xticks(index + bar_width, etiquetasTest)

        if escalaEnAngulos:
            figuraTest.set_ylim([80,0])
        else:
            figuraTest.set_ylim([0,200])

        # Remarcamos el entrenamiento
        Max = 80
        pasos = 200
        if escalaEnAngulos:
            MaxCuadradito = Max
        else:
            MaxCuadradito = pasos

        ancho = 0.8

        if resultado['Orientacion'] == 'P30':
            figuraTest.add_patch(
                patches.Rectangle(
                    (0, 0),
                    ancho,
                    MaxCuadradito,
                    fill=False,      # remove background
                    edgecolor="red"
                )
            )
        if resultado['Orientacion'] == 'A30':
            figuraTest.add_patch(
                patches.Rectangle(
                    (4, 0),
                    ancho,
                    MaxCuadradito,
                    fill=False,      # remove background
                    edgecolor="red"
                )
            )
"""
        # Grafico de entreamiento
        figuraEntrenamiento = axarr[i,1]
        # figuraEntrenamiento = plt.subplot(122)
        n_groups = 4
        index = np.arange(n_groups)
        bar_width = 0.25
        opacity = 0.4

        if escalaEnAngulos:
            valoresEntrenamientoInicial = valoresEntrenamientoInicialEnAngulos
            valoresEntrenamientoIntermedio = valoresEntrenamientoIntermedioEnAngulos
            valoresEntrenamientoFinal = valoresEntrenamientoFinalEnAngulos
        else:
            valoresEntrenamientoInicial = valoresEntrenamientoInicial
            valoresEntrenamientoIntermedio = valoresEntrenamientoIntermedio
            valoresEntrenamientoFinal = valoresEntrenamientoFinal

        rects1 = figuraEntrenamiento.bar(index, valoresEntrenamientoInicial, bar_width,
                 alpha=opacity*0.5,
                 color='b',
                 label='Entrenamiento inicial con feedback (100 trials)')
        rects2 = figuraEntrenamiento.bar(index + bar_width, valoresEntrenamientoIntermedio, bar_width,
                 alpha=opacity,
                 color='b',
                 label='Entrenamiento intermedio sin feedback (50 trials)')
        rects3 = figuraEntrenamiento.bar(index + bar_width*2, valoresEntrenamientoFinal, bar_width,
                alpha=opacity*2,
                color='b',
                label='Entrenamiento final con feedback (100 trials)')

        figuraEntrenamiento.set_xlabel('Sesion')
        if escalaEnAngulos:
            figuraEntrenamiento.set_ylabel('Umbral de detección (angulo)')
        else:
            figuraEntrenamiento.set_ylabel('Performance (estimulos)')
        #plt.ylabel('Performance')

        figuraEntrenamiento.set_title('Evolucion de performance en entrenamiento' + '('+"Usuario: " + alias+')')
        plt.sca(axarr[i, 1])
        plt.xticks(index + 1.5 * bar_width, etiquetasEntrenamiento)
        #figuraEntrenamiento.set_xticklabels(index + 1.5 * bar_width, etiquetasEntrenamiento)
        figuraEntrenamiento.legend(bbox_to_anchor=(0.95, 1), loc=2, borderaxespad=0.)
        if escalaEnAngulos:
            figuraEntrenamiento.set_ylim([0,100])
        else:
            figuraEntrenamiento.set_ylim([0,200])

        # pp.savefig(fig, dpi = 300, transparent = True)
        i += 1
"""
#    if escalaEnAngulos:
#        f.savefig('./Images/TransferenciaResultadosEnAngulos', bbox_inches='tight')
#    else:
#        f.savefig('./Images/TransferenciaResultados', bbox_inches='tight')


def dataNumerica(data=None):

    import numpy as np
    import datetime

    if not data:
        data = filterData()

    resultados = {}

    for alias in data[cts.P_Alias].unique():
        dataByAlias = data[data[cts.P_Alias] == alias]

        resultado = {}

        # Corregimos errores en a generacion de datos
        if alias == "ExpT_Magdalena":
            dataByAlias[cts.P_OrientacionEntrenamiento].replace('A30', 'P30', inplace=True)
        if alias == "ExpT_Julieta":
            dataByAlias[cts.P_OrientacionEntrenamiento].replace('P30', 'CONTROL', inplace=True)

        # Generamos las etiquetas
        etiquetasTest = ['P30', 'P60', 'P120', 'P150', 'A30', 'A60', 'A120', 'A150']
        etiquetasEntrenamiento = ['Dia1', 'Dia2', 'Dia3', 'Dia4']

        # y las series de datos
        dataTestInicial = dataByAlias[dataByAlias[cts.P_FaseActiva] == 'TestInicial']
        dataTestInicial = dataTestInicial[dataTestInicial[cts.P_LevelIdentificador]!='AngulosTutorial']
        if len (dataTestInicial.index) == 8:
            valoresTestInicial = []
            valoresTestInicial += [dataTestInicial[dataTestInicial[cts.P_LevelIdentificador]=='TESTP30'].iloc[0][cts.P_NivelEstimuloDinamica]]
            valoresTestInicial += [dataTestInicial[dataTestInicial[cts.P_LevelIdentificador]=='TESTP60'].iloc[0][cts.P_NivelEstimuloDinamica]]
            valoresTestInicial += [dataTestInicial[dataTestInicial[cts.P_LevelIdentificador]=='TESTP120'].iloc[0][cts.P_NivelEstimuloDinamica]]
            valoresTestInicial += [dataTestInicial[dataTestInicial[cts.P_LevelIdentificador]=='TESTP150'].iloc[0][cts.P_NivelEstimuloDinamica]]
            valoresTestInicial += [dataTestInicial[dataTestInicial[cts.P_LevelIdentificador]=='TESTA30'].iloc[0][cts.P_NivelEstimuloDinamica]]
            valoresTestInicial += [dataTestInicial[dataTestInicial[cts.P_LevelIdentificador]=='TESTA60'].iloc[0][cts.P_NivelEstimuloDinamica]]
            valoresTestInicial += [dataTestInicial[dataTestInicial[cts.P_LevelIdentificador]=='TESTA120'].iloc[0][cts.P_NivelEstimuloDinamica]]
            valoresTestInicial += [dataTestInicial[dataTestInicial[cts.P_LevelIdentificador]=='TESTA150'].iloc[0][cts.P_NivelEstimuloDinamica]]
            valoresTestInicial = [200 - x for x in valoresTestInicial]
        else:
            continue

        resultado['TestInicial'] = valoresTestInicial

        # Corregimos etiquetas mal generadas
        dataByAlias[cts.P_FaseActiva].replace('ExperimentoCompleto', 'TestFinal', inplace=True)

        dataTestFinal = dataByAlias[dataByAlias[cts.P_FaseActiva] == 'TestFinal']
        if len (dataTestFinal.index) == 8:
            valoresTestFinal = []
            valoresTestFinal += [dataTestFinal[dataTestFinal[cts.P_LevelIdentificador]=='TESTP30'].iloc[0][cts.P_NivelEstimuloDinamica]]
            valoresTestFinal += [dataTestFinal[dataTestFinal[cts.P_LevelIdentificador]=='TESTP60'].iloc[0][cts.P_NivelEstimuloDinamica]]
            valoresTestFinal += [dataTestFinal[dataTestFinal[cts.P_LevelIdentificador]=='TESTP120'].iloc[0][cts.P_NivelEstimuloDinamica]]
            valoresTestFinal += [dataTestFinal[dataTestFinal[cts.P_LevelIdentificador]=='TESTP150'].iloc[0][cts.P_NivelEstimuloDinamica]]
            valoresTestFinal += [dataTestFinal[dataTestFinal[cts.P_LevelIdentificador]=='TESTA30'].iloc[0][cts.P_NivelEstimuloDinamica]]
            valoresTestFinal += [dataTestFinal[dataTestFinal[cts.P_LevelIdentificador]=='TESTA60'].iloc[0][cts.P_NivelEstimuloDinamica]]
            valoresTestFinal += [dataTestFinal[dataTestFinal[cts.P_LevelIdentificador]=='TESTA120'].iloc[0][cts.P_NivelEstimuloDinamica]]
            valoresTestFinal += [dataTestFinal[dataTestFinal[cts.P_LevelIdentificador]=='TESTA150'].iloc[0][cts.P_NivelEstimuloDinamica]]
            valoresTestFinal = [200 - x for x in valoresTestFinal]
        else:
            valoresTestFinal = [0]*8

        resultado['TestFinal'] = valoresTestFinal

        # Creamos las diferencias
        valoresTestDiferencia = [y-x for y,x in zip (valoresTestFinal, valoresTestInicial)]

        resultado['Evolucion'] = valoresTestDiferencia

        # Pasamos los valores a angulos reales
        pasosLineal = True
        pasos = 200
        Min = 0
        MaxA = 80
        MaxP = 100

        valoresTestInicialEnAngulos = [(200-value)/pasos*(MaxP-Min) for value in valoresTestInicial[0:4]]
        valoresTestInicialEnAngulos = valoresTestInicialEnAngulos + [(200-value)/pasos*(MaxA-Min) for value in valoresTestInicial[4:8]]
        valoresTestFinalEnAngulos = [(200-value)/pasos*(MaxA-Min) for value in valoresTestFinal[0:4]]
        valoresTestFinalEnAngulos = valoresTestFinalEnAngulos + [(200-value)/pasos*(MaxA-Min) for value in valoresTestFinal[4:8]]
        valoresTestDiferenciaEnAngulo = [y-x for y,x in zip (valoresTestFinalEnAngulos, valoresTestInicialEnAngulos)]

        resultado['TestInicialAngulos'] = valoresTestInicialEnAngulos
        resultado['TestFinalAngulos'] = valoresTestFinalEnAngulos
        resultado['EvolucionAngulos'] = valoresTestDiferenciaEnAngulo

        # Recopilamos los datos del entrenamiento
        valoresEntrenamientoInicial = []
        valoresEntrenamientoIntermedio = []
        valoresEntrenamientoFinal = []

        # Datos de entrenamiento en paralelismo
        dataInicial = dataByAlias[dataByAlias[cts.P_LevelIdentificador] == 'ENTRENAMIENTOP30INICIAL']
        if len(dataInicial.index) == 4:
            valoresEntrenamientoInicial += [dataInicial[dataInicial[cts.P_FaseActiva]=='Entrenamiento1'][cts.P_NivelEstimuloDinamica].values[0]]
            valoresEntrenamientoInicial += [dataInicial[dataInicial[cts.P_FaseActiva]=='Entrenamiento2'][cts.P_NivelEstimuloDinamica].values[0]]
            valoresEntrenamientoInicial += [dataInicial[dataInicial[cts.P_FaseActiva]=='Entrenamiento3'][cts.P_NivelEstimuloDinamica].values[0]]
            valoresEntrenamientoInicial += [dataInicial[dataInicial[cts.P_FaseActiva]=='Entrenamiento4'][cts.P_NivelEstimuloDinamica].values[0]]
        else:
            if len(dataInicial.index) == 1:
                valoresEntrenamientoInicial = valoresEntrenamientoInicial + [dataInicial[dataInicial[cts.P_FaseActiva]=='Entrenamiento1'][cts.P_NivelEstimuloDinamica].values[0]]

        dataInter = dataByAlias[dataByAlias[cts.P_LevelIdentificador] == 'ENTRENAMIENTOP30MEDIO']
        if len(dataInter.index) == 4:
            valoresEntrenamientoIntermedio += [dataInter[dataInter[cts.P_FaseActiva]=='Entrenamiento1'][cts.P_NivelEstimuloDinamica].values[0]]
            valoresEntrenamientoIntermedio += [dataInter[dataInter[cts.P_FaseActiva]=='Entrenamiento2'][cts.P_NivelEstimuloDinamica].values[0]]
            valoresEntrenamientoIntermedio += [dataInter[dataInter[cts.P_FaseActiva]=='Entrenamiento3'][cts.P_NivelEstimuloDinamica].values[0]]
            valoresEntrenamientoIntermedio += [dataInter[dataInter[cts.P_FaseActiva]=='Entrenamiento4'][cts.P_NivelEstimuloDinamica].values[0]]

        else:
            if len(dataInter.index) == 1:
                valoresEntrenamientoIntermedio = valoresEntrenamientoIntermedio + [dataInter[dataInter[cts.P_FaseActiva]=='Entrenamiento1'][cts.P_NivelEstimuloDinamica].values[0]]

        dataFinal = dataByAlias[dataByAlias[cts.P_LevelIdentificador] == 'ENTRENAMIENTOP30FINAL']
        if len(dataFinal.index) == 4:
            valoresEntrenamientoFinal += [dataFinal[dataFinal[cts.P_FaseActiva]=='Entrenamiento1'][cts.P_NivelEstimuloDinamica].values[0]]
            valoresEntrenamientoFinal += [dataFinal[dataFinal[cts.P_FaseActiva]=='Entrenamiento2'][cts.P_NivelEstimuloDinamica].values[0]]
            valoresEntrenamientoFinal += [dataFinal[dataFinal[cts.P_FaseActiva]=='Entrenamiento3'][cts.P_NivelEstimuloDinamica].values[0]]
            valoresEntrenamientoFinal += [dataFinal[dataFinal[cts.P_FaseActiva]=='Entrenamiento4'][cts.P_NivelEstimuloDinamica].values[0]]

        else:
            if len(dataFinal.index) == 1:
                valoresEntrenamientoFinal = valoresEntrenamientoFinal + [dataFinal[dataFinal[cts.P_FaseActiva]=='Entrenamiento1'][cts.P_NivelEstimuloDinamica].values[0]]

        # Datos de entrenamiento en angulos
        dataInicial = dataByAlias[dataByAlias[cts.P_LevelIdentificador] == 'ENTRENAMIENTOA30INICIAL']
        if len(dataInicial.index) == 4:
            valoresEntrenamientoInicial += [dataInicial[dataInicial[cts.P_FaseActiva]=='Entrenamiento1'][cts.P_NivelEstimuloDinamica].values[0]]
            valoresEntrenamientoInicial += [dataInicial[dataInicial[cts.P_FaseActiva]=='Entrenamiento2'][cts.P_NivelEstimuloDinamica].values[0]]
            valoresEntrenamientoInicial += [dataInicial[dataInicial[cts.P_FaseActiva]=='Entrenamiento3'][cts.P_NivelEstimuloDinamica].values[0]]
            valoresEntrenamientoInicial += [dataInicial[dataInicial[cts.P_FaseActiva]=='Entrenamiento4'][cts.P_NivelEstimuloDinamica].values[0]]


        dataInter = dataByAlias[dataByAlias[cts.P_LevelIdentificador] == 'ENTRENAMIENTOA30MEDIO']
        if len(dataInter.index) == 4:
            valoresEntrenamientoIntermedio += [dataInter[dataInter[cts.P_FaseActiva]=='Entrenamiento1'][cts.P_NivelEstimuloDinamica].values[0]]
            valoresEntrenamientoIntermedio += [dataInter[dataInter[cts.P_FaseActiva]=='Entrenamiento2'][cts.P_NivelEstimuloDinamica].values[0]]
            valoresEntrenamientoIntermedio += [dataInter[dataInter[cts.P_FaseActiva]=='Entrenamiento3'][cts.P_NivelEstimuloDinamica].values[0]]
            valoresEntrenamientoIntermedio += [dataInter[dataInter[cts.P_FaseActiva]=='Entrenamiento4'][cts.P_NivelEstimuloDinamica].values[0]]


        dataFinal = dataByAlias[dataByAlias[cts.P_LevelIdentificador] == 'ENTRENAMIENTOA30FINAL']
        if len(dataFinal.index) == 4:
            valoresEntrenamientoFinal += [dataFinal[dataFinal[cts.P_FaseActiva]=='Entrenamiento1'][cts.P_NivelEstimuloDinamica].values[0]]
            valoresEntrenamientoFinal += [dataFinal[dataFinal[cts.P_FaseActiva]=='Entrenamiento2'][cts.P_NivelEstimuloDinamica].values[0]]
            valoresEntrenamientoFinal += [dataFinal[dataFinal[cts.P_FaseActiva]=='Entrenamiento3'][cts.P_NivelEstimuloDinamica].values[0]]
            valoresEntrenamientoFinal += [dataFinal[dataFinal[cts.P_FaseActiva]=='Entrenamiento4'][cts.P_NivelEstimuloDinamica].values[0]]

        valoresEntrenamientoInicial = [200 - x for x in valoresEntrenamientoInicial]
        valoresEntrenamientoIntermedio = [200 - x for x in valoresEntrenamientoIntermedio]
        valoresEntrenamientoFinal = [200 - x for x in valoresEntrenamientoFinal]

        if valoresEntrenamientoInicial == []:
            valoresEntrenamientoInicial = [0] * 4
            valoresEntrenamientoIntermedio = [0] * 4
            valoresEntrenamientoFinal = [0] * 4
        # if len(valoresEntrenamientoInicial) == 1:
        #     valoresEntrenamientoInicial = valoresEntrenamientoInicial + [0] * 3
        #     valoresEntrenamientoIntermedio = valoresEntrenamientoIntermedio + [0] * 3
        #     valoresEntrenamientoFinal = valoresEntrenamientoFinal + [0] * 3

        if dataByAlias[cts.P_OrientacionEntrenamiento].iloc[0] == 'P30':
            valoresEntrenamientoInicialEnAngulos = [(200-value)/pasos*(MaxP-Min) for value in valoresEntrenamientoInicial]
            valoresEntrenamientoIntermedioEnAngulos = [(200-value)/pasos*(MaxP-Min) for value in valoresEntrenamientoIntermedio]
            valoresEntrenamientoFinalEnAngulos = [(200-value)/pasos*(MaxP-Min) for value in valoresEntrenamientoFinal]
        if dataByAlias[cts.P_OrientacionEntrenamiento].iloc[0] == 'A30':
            valoresEntrenamientoInicialEnAngulos = [(200-value)/pasos*(MaxA-Min) for value in valoresEntrenamientoInicial]
            valoresEntrenamientoIntermedioEnAngulos = [(200-value)/pasos*(MaxA-Min) for value in valoresEntrenamientoIntermedio]
            valoresEntrenamientoFinalEnAngulos = [(200-value)/pasos*(MaxA-Min) for value in valoresEntrenamientoFinal]
        if dataByAlias[cts.P_OrientacionEntrenamiento].iloc[0] == 'CONTROL':
            valoresEntrenamientoInicialEnAngulos = [0]*4
            valoresEntrenamientoIntermedioEnAngulos = [0]*4
            valoresEntrenamientoFinalEnAngulos = [0]*4

        # corregimos los datos para Ivan que no hizo entrenamiento 2, 3, y 4
        if valoresEntrenamientoInicialEnAngulos[1] > 90:
            valoresEntrenamientoInicialEnAngulos[1:4] = [0,0,0]
            valoresEntrenamientoIntermedioEnAngulos[1:4] = [0,0,0]
            valoresEntrenamientoFinalEnAngulos[1:4] = [0,0,0]

        resultado['EntrenamientoInicial'] = valoresEntrenamientoInicial
        resultado['EntrenamientoMedio'] = valoresEntrenamientoIntermedio
        resultado['EntrenamientoFinal'] = valoresEntrenamientoFinal
        resultado['EntrenamientoInicialEnAngulos'] = valoresEntrenamientoInicialEnAngulos
        resultado['EntrenamientoMedioEnAngulos'] = valoresEntrenamientoIntermedioEnAngulos
        resultado['EntrenamientoFinalEnAngulos'] = valoresEntrenamientoFinalEnAngulos

        resultado['Orientacion'] = str(dataByAlias[cts.P_OrientacionEntrenamiento].iloc[0])
        resultados[cts.mapNames[alias]] = resultado
    return resultados


def resumeByCategorias(data=None):


    if not data:
        data = filterData()

    import seaborn as sns
    import matplotlib.pyplot as plt

    display(data[data[cts.P_Alias]=='ExpT_Magdalena'])

    data[cts.P_NivelEstimuloDinamica].update(200 - data[cts.P_NivelEstimuloDinamica])
    data = data[(data[cts.P_FaseActiva]=='TestInicial')|(data[cts.P_FaseActiva]=='TestFinal')]
    figura1 = sns.barplot(x="identificadorNivel", y="NivelSenalDinamica", data=data, hue='faseActiva')
    figura1.set_title('Total')
    plt.show()

    dataInicial = data[data[cts.P_OrientacionEntrenamiento]=='A30']
    figura2 = sns.barplot(x="identificadorNivel", y="NivelSenalDinamica", data=dataInicial, hue='faseActiva')
    figura2.set_title('Entrenamiento Angulos')
    plt.show()

    dataInicial = data[data[cts.P_OrientacionEntrenamiento]=='P30']
    display(dataInicial)
    figura3 = sns.barplot(x="identificadorNivel", y="NivelSenalDinamica", data=dataInicial, hue='faseActiva')
    figura3.set_title('Entrenamiento Paralelismo')
    plt.show()

    dataEntrenamiento = data[data[cts.P_OrientacionEntrenamiento]!='CONTROL']
    figura5 = sns.barplot(x="identificadorNivel", y="NivelSenalDinamica", data=dataEntrenamiento, hue='faseActiva')
    figura5.set_title ('Entrenamiento')
    plt.show()

    dataInicial = data[data[cts.P_OrientacionEntrenamiento]=='CONTROL']
    figura4 = sns.barplot(x="identificadorNivel", y="NivelSenalDinamica", data=dataInicial, hue='faseActiva')
    figura4.set_title ('Control')
    #sns.set(title = 'Hola')
    plt.show()
