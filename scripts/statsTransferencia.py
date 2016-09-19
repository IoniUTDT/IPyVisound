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

def resumeByUsers(data=None):

    import numpy as np
    import matplotlib.pyplot as plt

    if not data:
        data = lastTrialsOfLevels(data)

    for alias in data[cts.P_Alias].unique():
        dataByAlias = data[data[cts.P_Alias] == alias]

        # Corregimos errores en a generacion de datos
        if alias == "ExpT_Magdalena":
            dataByAlias[cts.P_OrientacionEntrenamiento].replace('A30', 'P30', inplace=True)
        if alias == "ExpT_Julieta":
            dataByAlias[cts.P_OrientacionEntrenamiento].replace('P30', 'CONTROL', inplace=True)



        # Generamos las etiquetas
        etiquetasTest = ['P30', 'P60', 'P120', 'P150', 'A30', 'A60', 'A120', 'A150']
        etiquetasEntrenamiento = ['FeedbackInicial', 'SinFeedback', 'FeedbackFinal']

        # y las series de datos
        dataTestInicial = dataByAlias[dataByAlias[cts.P_FaseActiva] == 'TestInicial']
        dataTestInicial = dataTestInicial[dataTestInicial[cts.P_LevelIdentificador]!='AngulosTutorial']
        if len (dataTestInicial.index) == 8:
            valoresTestInicial = []
            valoresTestInicial = valoresTestInicial + [dataTestInicial[dataTestInicial[cts.P_LevelIdentificador]=='TESTP30'].iloc[0][cts.P_NivelEstimuloDinamica]]
            valoresTestInicial = valoresTestInicial + [dataTestInicial[dataTestInicial[cts.P_LevelIdentificador]=='TESTP60'].iloc[0][cts.P_NivelEstimuloDinamica]]
            valoresTestInicial = valoresTestInicial + [dataTestInicial[dataTestInicial[cts.P_LevelIdentificador]=='TESTP120'].iloc[0][cts.P_NivelEstimuloDinamica]]
            valoresTestInicial = valoresTestInicial + [dataTestInicial[dataTestInicial[cts.P_LevelIdentificador]=='TESTP150'].iloc[0][cts.P_NivelEstimuloDinamica]]
            valoresTestInicial = valoresTestInicial + [dataTestInicial[dataTestInicial[cts.P_LevelIdentificador]=='TESTA30'].iloc[0][cts.P_NivelEstimuloDinamica]]
            valoresTestInicial = valoresTestInicial + [dataTestInicial[dataTestInicial[cts.P_LevelIdentificador]=='TESTA60'].iloc[0][cts.P_NivelEstimuloDinamica]]
            valoresTestInicial = valoresTestInicial + [dataTestInicial[dataTestInicial[cts.P_LevelIdentificador]=='TESTA120'].iloc[0][cts.P_NivelEstimuloDinamica]]
            valoresTestInicial = valoresTestInicial + [dataTestInicial[dataTestInicial[cts.P_LevelIdentificador]=='TESTA150'].iloc[0][cts.P_NivelEstimuloDinamica]]
            valoresTestInicial = [200 - x for x in valoresTestInicial]
        else:
            continue

        dataByAlias[cts.P_FaseActiva].replace('ExperimentoCompleto', 'TestFinal', inplace=True)
        dataTestFinal = dataByAlias[dataByAlias[cts.P_FaseActiva] == 'TestFinal']
        if len (dataTestFinal.index) == 8:
            valoresTestFinal = []
            valoresTestFinal = valoresTestFinal + [dataTestFinal[dataTestFinal[cts.P_LevelIdentificador]=='TESTP30'].iloc[0][cts.P_NivelEstimuloDinamica]]
            valoresTestFinal = valoresTestFinal + [dataTestFinal[dataTestFinal[cts.P_LevelIdentificador]=='TESTP60'].iloc[0][cts.P_NivelEstimuloDinamica]]
            valoresTestFinal = valoresTestFinal + [dataTestFinal[dataTestFinal[cts.P_LevelIdentificador]=='TESTP120'].iloc[0][cts.P_NivelEstimuloDinamica]]
            valoresTestFinal = valoresTestFinal + [dataTestFinal[dataTestFinal[cts.P_LevelIdentificador]=='TESTP150'].iloc[0][cts.P_NivelEstimuloDinamica]]
            valoresTestFinal = valoresTestFinal + [dataTestFinal[dataTestFinal[cts.P_LevelIdentificador]=='TESTA30'].iloc[0][cts.P_NivelEstimuloDinamica]]
            valoresTestFinal = valoresTestFinal + [dataTestFinal[dataTestFinal[cts.P_LevelIdentificador]=='TESTA60'].iloc[0][cts.P_NivelEstimuloDinamica]]
            valoresTestFinal = valoresTestFinal + [dataTestFinal[dataTestFinal[cts.P_LevelIdentificador]=='TESTA120'].iloc[0][cts.P_NivelEstimuloDinamica]]
            valoresTestFinal = valoresTestFinal + [dataTestFinal[dataTestFinal[cts.P_LevelIdentificador]=='TESTA150'].iloc[0][cts.P_NivelEstimuloDinamica]]
            valoresTestFinal = [200 - x for x in valoresTestFinal]
        else:
            continue

        # Creamos las dos figuras para el usuario
        fig = plt.figure(figsize=(20,2))
        fig.suptitle("Usuario: " + str(dataByAlias[cts.P_Alias].iloc[0]) + ". Entrenamiento: " + str(dataByAlias[cts.P_OrientacionEntrenamiento].iloc[0]), fontsize=12)
        fig.subplots_adjust(top=0.85)

        # Creamos el grafico de test
        figuraTest = plt.subplot(121)
        n_groups = 8
        index = np.arange(n_groups)
        bar_width = 0.35
        opacity = 0.4
        rects1 = figuraTest.bar(index, valoresTestInicial, bar_width,
                 alpha=opacity,
                 color='b',
                 label='Test Inicial')
        rects2 = figuraTest.bar(index + bar_width, valoresTestFinal, bar_width,
                 alpha=opacity,
                 color='r',
                 label='TestFinal')
        plt.xlabel('Orientacion')
        plt.ylabel('Performance')
        plt.title('Comparacion test inicial y final')
        plt.xticks(index + bar_width, etiquetasTest)
        plt.legend(bbox_to_anchor=(0.95, 1), loc=2, borderaxespad=0.)
        figuraTest.set_ylim([0,200])

        # Grafico de entreamiento
        figuraEntrenamiento = plt.subplot(122)
