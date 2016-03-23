def plotByUser (completado=True, expList=['UmbralAngulosPiloto', 'UmbralParalelismoPiloto']):

    from scripts.db import pandasUtilPiloto
    from IPython.display import display

    db = pandasUtilPiloto()

    users = db['userId'].unique()

    for user in users:

        userDb = db[db['userId']==user]
        userAlias = userDb.iloc[0]['alias']

        if completado:
            userDb = userDb[userDb['convergenciaFinalizada']==True]

        exps = userDb['expName'].unique()
        for exp in exps:
            if exp in expList:
                plotConvergenciaVersionPiloto (userDb, exp)

def plotConvergenciaVersionPiloto (db, expName):

    from IPython.display import display
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    import numpy as np

    db=db[db['expName']==expName]
    dbInfo = db.iloc[0]
    # Armamos el grafico
    colormap = plt.cm.nipy_spectral #I suggest to use nipy_spectral, Set1,Paired
    fig = plt.figure(figsize=(20, 20))
    ax = plt.subplot(111)
    ax.set_xlabel('Numero de trial')
    ax.set_ylabel('señal (grados)')
    title = ''
    if len(db['alias'].unique()) == 1:
        title = title + ' Usuario: ' + dbInfo['alias']
    title = title + ' Experimento: ' + expName
    ax.set_title(title, va='bottom')
    # Definimos la escala de colores
    size = len(db['alias'])
    colors = iter(cm.Paired(np.linspace(0, 1, size)))
    # inicializamos los levelInstance graficoados
    levelDraws = []

    # Procesamos la info de cada convergencia
    for index, row in db.iterrows():
        # La desviacion significa cosas diferentes segun el experimento. En el caso de paralelismo significa la desviacion respecto a la refrebcia, es decir que converge a 0
        # En el caso de los angulos deberia converger a 90 + referencia, por lo que para graficar y que converja todo junto conviene modificar los datos
        if expName == 'UmbralParalelismoPiloto':
            y = [elemento['estimulo']['desviacion'] for elemento in row['historial']]
        if expName == 'UmbralAngulosPiloto':
            y = [elemento['estimulo']['desviacion']-90-row['referencia'] for elemento in row['historial']]
        x = range (len(y))
        label = ''
        if len(db['alias'].unique()) != 1:
            label = label + ' Usuario: ' + row['alias']
        label = label + ' referencia: ' + str(row['referencia'])

        # Graficamos
        if row['levelInstance'] in levelDraws:
            ax.plot(x,y,color=color)
        else:
            color=next(colors)
            ax.plot(x,y,label=label,color=color)
            levelDraws = levelDraws + [row['levelInstance']]

        # Agregamos las marcas
        aciertos = [elemento['acertado'] for elemento in row['historial']]
        for i in x:
            if aciertos[i]:
                ax.plot(i,y[i],'bx')
            else:
                ax.plot(i,y[i],'rx')

        # Agregamos el punto finalo que marca la convergencia alcanzada
        if row['convergenciaAlcanzada']:
            # Calculamos el valor medio de la cantidad de estimulos usados en el programa
            n = row['tamanoVentanaAnalisisConvergencia']
            mean = sum(y[-n:]) / float(n)
            ax.plot([len(y)-n-1,len(y)-1],[mean,mean],'r--')
            ax.plot([len(y)-1],y[-1],'bs', markersize=10)
        else:
            ax.plot([len(y)-1],y[-1],'rs', markersize=10)



    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))


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
                ax.plot(i,y[i],'bx')
            else:
                ax.plot(i,y[i],'rx')

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
