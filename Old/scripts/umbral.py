def buscarUmbral (touchs, ordenado=False):

    """
        Esta funcion toma el dataframe de un conjunto de touchs incluidos en muchos niveles, y devuelve un dataframe con la informacion del nivel de umbral detectado.
        El parametro ordenado indica si se ordena los datos en funcion del angulo de referencia para las mediciones de un mismo usuario.

        Estas cuentas estan en el contexto de la medicion de umbral de deteccion.
    """

    import pandas as pd
    from IPython.display import display
    from scripts.general import fechaLocal

    import numpy as np # importando numpy
    from scipy import stats # importando scipy.stats

    # Definimos los levelversion compatibles
    levelVersionCompatibles = [22]

    # Creamos un dataframe para guardar los datos
    resumen = pd.DataFrame(columns=['AnguloReferencia','MediaDeltaTita',
                                    'DesviacionDeltaTita','CumpleCriterioCola',
                                    'Session','Usuario','Level','LevelVersion',
                                    'Identificador'])

    #Procesamos solo los datos de niveles completos
    touchs = touchs[touchs['levelCompleted']==True]

    # Se filtra los datos de levelVersion no compatibles con este procesamientos
    touchs = touchs[touchs['levelVersion'].isin(levelVersionCompatibles)]

    for usuario in touchs['Alias'].unique():
        touchsUsuario = touchs[touchs['Alias']==usuario]
        for session in touchsUsuario['sessionInstance'].unique():
            touchsSession = touchsUsuario[touchsUsuario['sessionInstance']==session]

            for level in touchsSession['levelInstance'].unique():

                resumenToAppend = pd.DataFrame(columns=['AnguloReferencia','MediaDeltaTita','DesviacionDeltaTita','CumpleCriterioCola','Session','Usuario','Level','LevelVersion','Identificador'])

                # Cargamos cosas en el resumen
                resumenToAppend['Session'] = [fechaLocal(session)]
                resumenToAppend['Usuario'] = [usuario]
                resumenToAppend['Level'] = [fechaLocal(level)]


                touchsLevel = touchsSession[touchsSession['levelInstance']==level]

                #filtramos la ultima mitad de los datos
                touchsLevelEnd = touchsLevel.iloc[-int(touchsLevel.index.size/2):,:]

                # Miramos si tiene algun tipo de sentido (que este en el fondo de la cola). Para eso revisamos que no haya mas false que true (Xq una vez q se estabiliza tiene q haber dos true x cada false (el codigo disminuye la señal despues de dos aciertos))
                # y ademas revisamos que no haya menos de 1/4 de falses xq eso indicaria que no esta rebotando

                levelInfo = touchsLevel.iloc[0]
                contadorTouchsLevelTrue = touchsLevelEnd[touchsLevelEnd['isTrue']==True].index.size
                contadorTouchsLevelFalse = touchsLevelEnd[touchsLevelEnd['isTrue']==False].index.size

                if ((contadorTouchsLevelTrue < contadorTouchsLevelFalse) or (contadorTouchsLevelFalse*3<contadorTouchsLevelTrue)):
                    resumenToAppend['CumpleCriterioCola'] = [False]
                else:
                    resumenToAppend['CumpleCriterioCola'] = [True]


                # Extraemos la info de del delta tita del estimulo de cada trial
                columnName = 'DeltaTita'
                if not columnName in touchsLevelEnd.columns:
                    temp = pd.DataFrame(columns=[columnName])
                    for (i,r) in touchsLevelEnd.iterrows():
                        e = r['jsonMetaDataEstimulo']
                        temp.loc[i] = [e['infoConceptual']['deltaAngulo']]
                    touchsLevelEnd = pd.concat([touchsLevelEnd, temp], axis=1)
                else:
                    display ('Warning: Se encontraron datos ya cargados para: '+columnName)

                # Extraemos la info del angulo de referencia
                columnName = 'AnguloDeReferencia'
                if not columnName in touchsLevelEnd.columns:
                    temp = pd.DataFrame(columns=[columnName])
                    for (i,r) in touchsLevelEnd.iterrows():
                        e = r['jsonMetaDataEstimulo']
                        temp.loc[i] = [e['infoConceptual']['direccionAnguloReferencia']]
                    touchsLevelEnd = pd.concat([touchsLevelEnd, temp], axis=1)
                else:
                    display ('Warning: Se encontraron datos ya cargados para: '+columnName)

                levelInfo = touchsLevelEnd.iloc[0]
                datos = touchsLevelEnd['DeltaTita'].tolist()

                resumenToAppend['AnguloReferencia'] = [levelInfo['AnguloDeReferencia']]
                resumenToAppend['MediaDeltaTita'] = [np.mean(datos)]
                resumenToAppend['DesviacionDeltaTita'] = [np.std(datos)]
                resumenToAppend['LevelVersion'] = [levelInfo['levelVersion']]
                if 'appVersion' in touchsLevelEnd.columns:
                    resumenToAppend['AppVersion'] = [levelInfo['appVersion']]
                else:
                    resumenToAppend['AppVersion'] = 'Sin Dato'
                if 'identificador' in touchsLevelEnd.columns:
                    resumenToAppend['Identificador'] = [levelInfo['identificador']]
                else:
                    resumenToAppend['Identificador'] = 'Dato no cargado'
                resumen = pd.concat([resumen, resumenToAppend], axis=0, ignore_index=True)

    if ordenado:
        resumen = resumen.sort(['AnguloReferencia'], ascending=[True])

    return resumen



def plotResumen (resumen, zoom=2):

    """
        Esta funcion grafica los resultados del analisis de umbral de detecciones de paralelismo, en el contexto del experimento para medirlo.
        Tiene como input el resumen de sensibilidad y un parametro que indica el zoom con que se muestra el resultado al haer zoom.
    """
    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib.cm as cm

    resumen['ReferenciaEnRadianes'] = resumen['AnguloReferencia']/180*np.pi
    resumen['MediaDeltaTitaRad'] = resumen['MediaDeltaTita']/180*np.pi
    resumen['RefRadCorregida'] = resumen['ReferenciaEnRadianes'] - resumen['MediaDeltaTitaRad']/2
    resumen['Color'] = ['g' if x else 'r' for x in resumen['CumpleCriterioCola'].tolist() ]
    resumen['Identificador'].fillna('SinDato',inplace=True)

    fig = plt.figure(num=None, figsize=(10, 10), dpi=180, facecolor='w', edgecolor='k')
    ax = plt.subplot(111, projection='polar')
    ax.set_title("Separacion angular minima (en º) que se puede detectar en funcion de la orientacion de las rectas \'pseudoparalelas\'. \n El color del punto representa si se considera que la medicion paso un test de confianza o no.", va='bottom')

    for user in resumen['Usuario'].unique():
        resumenFiltrado = resumen[resumen['Usuario']==user]
        resumenInfo = resumenFiltrado.iloc[0]

        x = resumenFiltrado['ReferenciaEnRadianes'].tolist()
        y = resumenFiltrado['MediaDeltaTita'].tolist()
        color = resumenFiltrado['Color'].tolist()
        size = resumenFiltrado['DesviacionDeltaTita']

        ax.set_xticks(np.pi/180. * np.linspace(180,  -180, 36, endpoint=False))
        ax.plot(x, y, label=resumenInfo['Usuario'])
        ax.scatter(x, y, marker='o', c=color)
        ax.legend()

        """
        fig2, ax2 = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))

        ax2.set_title("Visualizacion del overlap para el usuario " + user, va='bottom')
        ax2.set_xticks(np.pi/180. * np.linspace(180,  -180, 36, endpoint=False))

        theta = resumenFiltrado['RefRadCorregida'].tolist()
        radii = resumenFiltrado['MediaDeltaTita'].tolist()
        width = resumenFiltrado['MediaDeltaTitaRad'].tolist()
        bars = ax2.bar(theta, radii, width=width, bottom=0.0)
        for r,bar in zip(radii, bars):
            bar.set_facecolor( cm.jet(r/10.))
            bar.set_alpha(0.5)
        """

    # Repetimos el plot pero con zoom
    fig = plt.figure(num=None, figsize=(10, 10), dpi=180, facecolor='w', edgecolor='k')

    if not all(i >= zoom for i in resumen['MediaDeltaTita'].tolist()):

        ax = plt.subplot(111, projection='polar')
        ax.set_title("Separacion angular minima (en º) que se puede detectar en funcion de la orientacion de las rectas \'pseudoparalelas\'. \n El color del punto representa si se considera que la medicion paso un test de confianza o no.", va='bottom')
        ax.set_ylim(0,zoom)


        for user in resumen['Usuario'].unique():
            resumenFiltrado = resumen[resumen['Usuario']==user]

            x = resumenFiltrado['ReferenciaEnRadianes'].tolist()
            y = resumenFiltrado['MediaDeltaTita'].tolist()
            color = resumenFiltrado['Color'].tolist()
            size = resumenFiltrado['DesviacionDeltaTita']
            resumenInfo = resumenFiltrado.iloc[0]

            ax.plot(x, y, label=resumenInfo['Usuario'])
            ax.scatter(x, y, marker='o', c=color)
            ax.legend()

            fig3, ax3 = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))

            ax3.set_title("Visualizacion del overlap para el usuario " + user +" con zoom.", va='bottom')
            ax3.set_xticks(np.pi/180. * np.linspace(180,  -180, 36, endpoint=False))
            ax3.set_ylim(0,0.02)

            theta = resumenFiltrado['RefRadCorregida'].tolist()
            radii = resumenFiltrado['MediaDeltaTita'].tolist()
            width = resumenFiltrado['MediaDeltaTitaRad'].tolist()
            bars = ax3.bar(theta, radii, width=width, bottom=0.0)
            for r,bar in zip(radii, bars):
                bar.set_facecolor( cm.jet(r/10.))
                bar.set_alpha(0.5)

def plotConvergencia (touchs, completo=True):

    """
        Esta funcion grafica la convergencia del delta tita en funcion del del avance del level. Sirve solo para visualizar datos.
    """

    import matplotlib.pyplot as plt
    import pandas as pd

    from IPython.display import display
    from scripts.general import fechaLocal

    #Procesamos solo los datos de niveles completos
    if completo:
        touchs = touchs[touchs['levelCompleted']==True]

    for usuario in touchs['Alias'].unique():
        display ('Se hara la estadistica del usuario: '+usuario)
        touchsUsuario = touchs[touchs['Alias']==usuario]
        display ('El usuario '+usuario+' jugo '+str(len(touchsUsuario['sessionInstance'].unique()))+' veces')
        for session in touchsUsuario['sessionInstance'].unique():
            touchsSession = touchsUsuario[touchsUsuario['sessionInstance']==session]

            # Analizamos los datos para dificultad generica
            display ('En la session '+ str(fechaLocal(session))+ ' el usuario '+str(usuario)+' jugo '+str(len(touchsSession['levelInstance'].unique())) + ' niveles')
            for level in touchsSession['levelInstance'].unique():

                touchsLevel = touchsSession[touchsSession['levelInstance']==level]

                # Extraemos la info de del delta tita del estimulo de cada trial
                columnName = 'DeltaTita'
                if not columnName in touchsLevel.columns:
                    temp = pd.DataFrame(columns=[columnName])
                    for (i,r) in touchsLevel.iterrows():
                        e = r['jsonMetaDataEstimulo']
                        temp.loc[i] = [e['infoConceptual']['deltaAngulo']]
                    touchsLevel = pd.concat([touchsLevel, temp], axis=1)
                else:
                    display ('Warning: Se encontraron datos ya cargados para: '+columnName)

                # Extraemos la info del angulo de referencia
                columnName = 'AnguloDeReferencia'
                if not columnName in touchsLevel.columns:
                    temp = pd.DataFrame(columns=[columnName])
                    for (i,r) in touchsLevel.iterrows():
                        e = r['jsonMetaDataEstimulo']
                        temp.loc[i] = [e['infoConceptual']['direccionAnguloReferencia']]
                    touchsLevel = pd.concat([touchsLevel, temp], axis=1)
                else:
                    display ('Warning: Se encontraron datos ya cargados para: '+columnName)

                levelInfo = touchsLevel.iloc[0]
                touchsLevelTrue = touchsLevel[touchsLevel['isTrue']==True]
                touchsLevelFalse = touchsLevel[touchsLevel['isTrue']==False]

                # Armamos el grafico
                fig = plt.figure(figsize=(10,3))
                ax = fig.add_subplot(111)
                title = 'Evolucion de la dificultad en funcion del trial \n' + 'Usuario: '+str(usuario) + ' direccion de refrencia: ' + str(levelInfo['AnguloDeReferencia'])+' grados, ' + 'levelVersion '+str(levelInfo['levelVersion'])
                ax.set_title(title, fontsize=10, fontweight='bold')
                ax.set_xlabel('Numero de trial')
                ax.set_ylabel('Delta Tita (grados)')
                x = touchsLevel.index
                y = touchsLevel['DeltaTita'].tolist()
                ax.plot(x,y)
                x = touchsLevelTrue.index
                y = touchsLevelTrue['DeltaTita'].tolist()
                ax.plot(x,y,'go')
                x = touchsLevelFalse.index
                y = touchsLevelFalse['DeltaTita'].tolist()
                ax.plot(x,y,'ro')
