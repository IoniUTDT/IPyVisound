def plotParalelismos (soloCompletados = True):

    from IPython.display import display
    from scripts.general import fechaLocal
    import matplotlib.pyplot as plt
    import os
    import pickle
    import json

    # Cargamos los usuarios
    filename = './Guardados/db.' + 'Alias'
    if os.path.isfile(filename):
        with open(filename, 'rb') as f:
            alias = pickle.load(f)
    else:
        display ('ERROR : No se ha encontrado el archivo ' + filename)

    # Cargamos los registros de convergencia para umbral paralelismo
    filename = './Guardados/db.' + 'CONVERGENCIA'
    if os.path.isfile(filename):
        with open(filename, 'rb') as f:
            convergencias = pickle.load(f)
    else:
        display ('ERROR : No se ha encontrado el archivo ' + filename)


    convergenciasByLevelInstance = {}

    for convergencia in convergencias:
        convergencia = json.loads(convergencia['contenido'])

        # Eliminamos las convergencias no terminadas si corresponde
        if soloCompletados:
            if not convergencia['dinamica']['convergenciaFinalizada']:
                continue

        # agrupamos los pares segun corresponda
        if convergencia['session']['levelInstance'] in convergenciasByLevelInstance.keys():
            convergenciasByLevelInstance [convergencia['session']['levelInstance']] = convergenciasByLevelInstance [convergencia['session']['levelInstance']] + [convergencia]
        else:
            convergenciasByLevelInstance [convergencia['session']['levelInstance']] = [convergencia]

    for levelInstance in convergenciasByLevelInstance.keys():

        # Armamos el grafico
        fig = plt.figure(figsize=(20, 20))
        ax = plt.subplot(111)
        ax.set_xlabel('Numero de trial')
        ax.set_ylabel('Delta Tita (grados)')

        for convergencia in convergenciasByLevelInstance[levelInstance] :

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
