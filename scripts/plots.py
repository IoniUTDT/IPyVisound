def plotByUser (alias=["Todos"], completado=True, expList=['UmbralAngulosPiloto', 'UmbralParalelismoPiloto','UmbralAngulosTutorial']):

    from scripts.db import pandasUtilPiloto
    from IPython.display import display

    db = pandasUtilPiloto()

    if alias == ["Todos"]:
        users = db['alias'].unique()
    else:
        users = alias


    for user in users:

        userDb = db[db['alias']==user]
        userAlias = userDb.iloc[0]['alias']

        if completado:
            userDb = userDb[userDb['levelFinalizadoCorrectamente']==True]

        exps = userDb['expName'].unique()
        for exp in exps:
            if exp in expList:
                plotConvergenciaVersionPiloto (userDb, exp)


def plotConvergenciaVersionPiloto (db, expName, fromStadistics=False, excludedLevelInstance = [1465499974725,1466028783553,1466028660936,1466028551014,1466028543250,1466027507789,1466027464069,1466027418273,1466027187076]):

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

"""
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
