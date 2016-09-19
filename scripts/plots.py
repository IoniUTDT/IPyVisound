import scripts.constants as cts

from scripts.general import chkVersion
from IPython.display import display
from scripts.db import dataProcesada

chkVersion()

def plotByUser (specificData=False, alias=["Todos"], filtroCompletadoActivo=True,
                expList=cts.expList, onlyOneUser=True, number=-1, join=False, db=None):

    users, db = dataProcesada(specificData=specificData, alias=alias, filtroCompletadoActivo=filtroCompletadoActivo,
                        expList=expList, onlyOneUser=onlyOneUser, number=number, join=join, db=db)

    """
    excludedSessionInstance = [1473088663797]

    from scripts.db import pandasTransferencia

    if not specificData:
        db = pandasTransferencia()

    users = db[cts.P_Alias].unique() if alias == ["Todos"] else alias
    """

    for user in users:
        """
        if onlyOneUser:
            if user != users[number]:
                continue
        """
        userDb = db[db[cts.P_Alias]==user]

        """
        if filtroCompletadoActivo:
            userDb = userDb[userDb[cts.P_LevelFinalizado]==True]
        """

        exps = userDb[cts.P_LevelIdentificador].unique()
        for exp in exps:
            #display (exp)
            if exp in expList:

                data = userDb[userDb[cts.P_LevelIdentificador]==exp]
                #data = userDb[~userDb[cts.P_SessionInstance].isin(excludedSessionInstance)]
                plotConvergencia (data, exp, join=join)


def plotConvergencia (db, expName, fromStadistics=False, join=False):

    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    import numpy as np
    from scripts.general import fechaLocal

    db=db[db[cts.P_LevelIdentificador]==expName]
    dbInfo = db.iloc[0]
    # Armamos el grafico
    colormap = plt.cm.nipy_spectral #I suggest to use nipy_spectral, Set1,Paired

    if join:
        if fromStadistics:
            fig = plt.figure(figsize=(20, 10))
        else:
            fig = plt.figure(figsize=(20, 20))

        ax = plt.subplot(111)
        ax.set_xlabel('Numero de trial')
        ax.set_ylabel('señal (nivel)')

        title = ''
        if len(db[cts.P_Alias].unique()) == 1:
            title = title + ' Usuario: ' + dbInfo[cts.P_Alias]

        title = title + ' Experimento: ' + expName

        ax.set_title(title, va='bottom')

        # Definimos la escala de colores
        size = len(db[cts.P_Alias])
        colors = iter(cm.Paired(np.linspace(0, 1, size)))
        levelColors = {}

    onceInstance = True
    # Hacemos un grafico para cada instancia del nivel jugado (en principio deberia haber una sola, pero podria haber mas)
    for levelInstance in db[cts.P_LevelInstance].unique():

        if not join:
            if fromStadistics:
                fig = plt.figure(figsize=(20, 10))
            else:
                fig = plt.figure(figsize=(20, 20))

            ax = plt.subplot(111)
            ax.set_xlabel('Numero de trial')
            ax.set_ylabel('señal (nivel)')

            title = ''
            if len(db[cts.P_Alias].unique()) == 1:
                title = title + ' Usuario: ' + dbInfo[cts.P_Alias]

            title = title + ' Experimento: ' + expName

            ax.set_title(title, va='bottom')

            # Definimos la escala de colores
            size = len(db[cts.P_Alias])
            colors = iter(cm.Paired(np.linspace(0, 1, size)))
            levelColors = {}


        dbLevelInstance = db[db[cts.P_LevelInstance] == levelInstance]
        #display (dbLevelInstance[cts.P_SessionInstance].unique())
        y = dbLevelInstance[cts.P_NivelEstimuloDinamica].tolist()
        x = range (len(y))

        # Construimos el label diferentes segun sea un grafico para un solo usuario o para varios
        label = ''

        if len(db[cts.P_Alias].unique()) != 1:
            label = label + ' Usuario: ' + dbLevelInstance[cts.P_Alias].unique()[0]

        label = label + ' referencia: ' + str(dbLevelInstance[cts.P_Referencia].unique()[0])
        label = label + ' \n Valor final: ' + str(y[-1])
        label = label + ' \n Sesion:' + str(dbLevelInstance[cts.P_SessionInstance].unique()[0])
        label = label + ' \n Fecha:' + str(fechaLocal(dbLevelInstance[cts.P_SessionInstance].unique()[0]))
        #display (levelInstance)

        # Agregamos las marcas
        aciertos = dbLevelInstance[cts.P_RtaCorrecta].tolist()
        tipo = dbLevelInstance[cts.P_TipoDeTrial].tolist()
        for i in x:
            if aciertos[i]:
                ax.plot(i,y[i],'go')
            else:
                ax.plot(i,y[i],'ro')

        if onceInstance:
            ax.plot([i for i in x if tipo[i]==cts.Db_Historial_Recurso_EtiquetaTipoNoEstimulo],[y[i] for i in x if tipo[i]==cts.Db_Historial_Recurso_EtiquetaTipoNoEstimulo],'8', color='black', markersize=15, fillstyle = 'none', label=cts.Db_Historial_Recurso_EtiquetaTipoNoEstimulo, mew = 3)
            ax.plot([i for i in x if tipo[i]==cts.Db_Historial_Recurso_EtiquetaTipoEstimulo],[y[i] for i in x if tipo[i]==cts.Db_Historial_Recurso_EtiquetaTipoEstimulo],'8', color='green', markersize=15, fillstyle = 'none', label=cts.Db_Historial_Recurso_EtiquetaTipoEstimulo, mew = 3)
            ax.plot([i for i in x if tipo[i]==cts.Db_Historial_Recurso_EtiquetaTipoTest],[y[i] for i in x if tipo[i]==cts.Db_Historial_Recurso_EtiquetaTipoTest],'8', color='cyan', markersize=15, fillstyle = 'none', label=cts.Db_Historial_Recurso_EtiquetaTipoTest, mew = 3)
        else:
            ax.plot([i for i in x if tipo[i]==cts.Db_Historial_Recurso_EtiquetaTipoNoEstimulo],[y[i] for i in x if tipo[i]==cts.Db_Historial_Recurso_EtiquetaTipoNoEstimulo],'8', color='black', markersize=15, fillstyle = 'none', mew = 3)
            ax.plot([i for i in x if tipo[i]==cts.Db_Historial_Recurso_EtiquetaTipoEstimulo],[y[i] for i in x if tipo[i]==cts.Db_Historial_Recurso_EtiquetaTipoEstimulo],'8', color='green', markersize=15, fillstyle = 'none', mew = 3)
            ax.plot([i for i in x if tipo[i]==cts.Db_Historial_Recurso_EtiquetaTipoTest],[y[i] for i in x if tipo[i]==cts.Db_Historial_Recurso_EtiquetaTipoTest],'8', color='cyan', markersize=15, fillstyle = 'none', mew = 3)

        # Graficamos
        if levelInstance in levelColors.keys():
            color = levelColors[levelInstance]
            # ax.plot(x,y,color=color)
            ax.plot(x,y)
        else:
            color=next(colors)
            #ax.plot(x,y,label=label,color=color)
            ax.plot(x,y,label=label)
            levelColors[levelInstance] = color

        if not join:
            fig.savefig('./Images/Calibracion'+str(levelInstance))

        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),numpoints=1)

        onceInstance = False

    if join:
        fig.savefig('./Images/Calibracion'+str(levelInstance))

    plt.show(block=False)


"""

def plotConvergenciaVersionPiloto (db, expName, fromStadistics=False):

    excludedLevelInstance = [1465499974725,1466028783553,1466028660936,1466028551014,1466028543250,1466027507789,1466027464069,1466027418273,1466027187076]

    from IPython.display import display
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    import numpy as np

    db=db[db['expName']==expName]
    dbInfo = db.iloc[0]
    # Armamos el grafico
    colormap = plt.cm.nipy_spectral #I suggest to use nipy_spectral, Set1,Paired
    if fromStadistics:
        fig = plt.figure(figsize=(20, 10))
    else:
        fig = plt.figure(figsize=(20, 20))
    ax = plt.subplot(111)
    ax.set_xlabel('Numero de trial')
    ax.set_ylabel('señal (nivel)')
    title = ''
    if len(db['alias'].unique()) == 1:
        title = title + ' Usuario: ' + dbInfo['alias']
    title = title + ' Experimento: ' + expName
    ax.set_title(title, va='bottom')
    # Definimos la escala de colores
    size = len(db['alias'])
    colors = iter(cm.Paired(np.linspace(0, 1, size)))
    # inicializamos los levelInstance graficoados
    levelColors = {}
    # Procesamos la info de cada convergencia
    for index, row in db.iterrows():

        if row['levelInstance'] in excludedLevelInstance:
            continue
        # La desviacion significa cosas diferentes segun el experimento. En el caso de paralelismo significa la desviacion respecto a la refrebcia, es decir que converge a 0
        # En el caso de los angulos deberia converger a 90 + referencia, por lo que para graficar y que converja todo junto conviene modificar los datos
        #
        #if expName in ['UmbralParalelismoPiloto']:
        #    y = [elemento['estimulo']['desviacion'] for elemento in row['historial']]
        #if expName in ['UmbralAngulosPiloto','UmbralAngulosTutorial']:
        #    y = [elemento['estimulo']['desviacion']-90-row['referencia'] for elemento in row['historial']]
        #
        y = [elemento['nivelEstimulo'] for elemento in row['historial']]
        estimuloReal = [elemento['estimulo']['nivelSenal'] for elemento in row['historial']]
        x = range (len(y))
        # Construimos el label diferentes segun sea un grafico para un solo usuario o para varios
        label = ''
        if len(db['alias'].unique()) != 1:
            label = label + ' Usuario: ' + row['alias']
        label = label + ' referencia: ' + str(row['referencia'])

        senalesNoCeroNiTest = [elemento for elemento in row['historial'] if elemento['trialType']=='REAL_TRIAL_ESTIMULO']
        label = label + ' \n Valor final: ' + str(senalesNoCeroNiTest[-1]['estimulo']['desviacion'])


        # Graficamos
        if row['levelInstance'] in levelColors.keys():
            color = levelColors[row['levelInstance']]
            ax.plot(x,y,color=color)
        else:
            color=next(colors)
            ax.plot(x,y,label=label,color=color)
            levelColors[row['levelInstance']] = color

        # Agregamos las marcas
        aciertos = [elemento['acertado'] for elemento in row['historial']]
        tipo = [elemento['trialType'] for elemento in row['historial']]
        for i in x:
            if aciertos[i]:
                ax.plot(i,y[i],'bo')
            else:
                ax.plot(i,y[i],'ro')

        ax.plot([i for i in x if tipo[i]=='REAL_TRIAL_CERO'],[y[i] for i in x if tipo[i]=='REAL_TRIAL_CERO'],'8', color='black', markersize=20, fillstyle = 'none', label='Señal cero', mew = 3)
        ax.plot([i for i in x if tipo[i]=='REAL_TRIAL_ESTIMULO'],[y[i] for i in x if tipo[i]=='REAL_TRIAL_ESTIMULO'],'8', color='green', markersize=20, fillstyle = 'none', label='Señal nivel', mew = 3)
        ax.plot([i for i in x if tipo[i]=='TEST_EASY_Trial'],[y[i] for i in x if tipo[i]=='TEST_EASY_Trial'],'8', color='cyan', markersize=20, fillstyle = 'none', label='Señal test', mew = 3)
        # Agregamos las marcas de los niveles reales
        textos = zip(estimuloReal,x,y,tipo)
        for elemento in textos:
            if elemento[3] =='TEST_EASY_Trial':
                ax.annotate(elemento[0],(elemento[1],elemento[2]))

        if not fromStadistics:
            # Agregamos el punto finalo que marca la convergencia alcanzada
            if row['levelFinalizadoCorrectamente']:
                # Calculamos el valor medio de la cantidad de estimulos usados en el programa
                #n = row['tamanoVentanaAnalisisConvergencia']
                #mean = sum(y[-n:]) / float(n)
                #ax.plot([len(y)-n-1,len(y)-1],[mean,mean],'r--')
                ax.plot([len(y)-1],y[-1],'bs', markersize=10)
            else:
                ax.plot([len(y)-1],y[-1],'rs', markersize=10)


    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show(block=False)


def plotAllByUser (userAlias=[], soloCompletados = True):


        # Extraemos datos del la estructura de datos almacenada
        experimento = convergencia['session']['expName']
        usuario = alias[convergencia['session']['session']['user']['id']]['alias']
        levelInstance = convergencia['session']['levelInstance']
        dinamica = convergencia['dinamica']['identificador']
        referencia = convergencia['dinamica']['referencia']

        # Extraemos los puntos a graficar
        y = [elemento['estimulo']['desviacion'] for elemento in convergencia['dinamica']['historial']]
        x = range (len(y))

        # Armamos el grafico
        ax.set_xlabel('Numero de trial')
        ax.set_ylabel('Delta Tita (grados)')

        # Graficamos
        ax.plot(x,y,label=dinamica)

        aciertos = [elemento['acertado'] for elemento in convergencia['dinamica']['historial']]

        for i in x:
            if aciertos[i]:
                ax.plot(i,y[i],'bo')
            else:
                ax.plot(i,y[i],'ro')

        # Agregamos el punto finalo que marca la convergencia alcanzada
        if convergencia['dinamica']['convergenciaAlcanzada']:
            # Calculamos el valor medio de la cantidad de estimulos usados en el programa
            n = convergencia['dinamica']['tamanoVentanaAnalisisConvergencia']
            mean = sum(y[-n:]) / float(n)
            ax.plot([len(y)-n-1,len(y)-1],[mean,mean],'r--')
            ax.plot([len(y)-1],y[-1],'bs', markersize=10)
        else:
            ax.plot([len(y)-1],y[-1],'rs', markersize=10)

        ax.set_title(experimento + ' angulo de referencia: ' + str(referencia) + '\n' + ' correspondiente a ' + usuario + ' en la fecha ' + str(fechaLocal(levelInstance)), va='bottom')


        # Agregamos decorados
        ax.plot(ax.get_xlim(),[0,0],'r')
        #ax.set_title(experimento + ' angulo de referencia: ' + str(referencia) + '\n' + ' correspondiente a ' + usuario + ' en la fecha ' + str(fechaLocal(levelInstance)), va='bottom')
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
"""
