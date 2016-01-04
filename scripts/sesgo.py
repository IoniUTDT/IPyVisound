def crearTabla (touchs,experimentoUmbralCompleto=True):

    """
        Esta funcion transforma la info que viene en los tochs en info util para hacer graficos de tipo de contiengencia donde es relevante la siguientes informacion:
        - La señal estimulo (converge/diverge +/-)
        - La señal reportada (converge/diverge +/-)
        - El delta tita
        - El angulo de referencia
        - La separacion entre las rectas
        - El usuario
    """
    from scripts.general import chkVersion
    chkVersion()

    import pandas as pd
    import numpy as np
    from IPython.display import display

    display ('Creando tabla resumen de la informacion de los toques en funcion de los parametros para el experimento de umbral')


    resumen = touchs[['jsonMetaDataTouched','jsonMetaDataEstimulo','userID','Alias']]

    # Extraemos la info de los jsons
    columnName = 'AnguloReferencia'
    display ('Extrayendo informacion de: '+columnName)
    if not columnName in resumen.columns:
        temp = pd.DataFrame(columns=[columnName])
        for (i,r) in touchs.iterrows():
            temp.loc[i] = r['jsonMetaDataEstimulo']['infoConceptual']['direccionAnguloReferencia']
        resumen = pd.concat([resumen, temp], axis=1)
    else:
        display ('Warning: Se encontraron datos ya cargados para: '+columnName)

    columnName = 'DeltaTita'
    display ('Extrayendo informacion de: '+columnName)
    if not columnName in resumen.columns:
        temp = pd.DataFrame(columns=[columnName])
        for (i,r) in touchs.iterrows():
            temp.loc[i] = r['jsonMetaDataEstimulo']['infoConceptual']['deltaAngulo']
        resumen = pd.concat([resumen, temp], axis=1)
    else:
        display ('Warning: Se encontraron datos ya cargados para: '+columnName)

    columnName = 'SeJuntanEstimulo'
    display ('Extrayendo informacion de: '+columnName)
    if not columnName in resumen.columns:
        temp = pd.DataFrame(columns=[columnName])
        for (i,r) in touchs.iterrows():
            temp.loc[i] = r['jsonMetaDataEstimulo']['infoConceptual']['seJuntan']
        resumen = pd.concat([resumen, temp], axis=1)
    else:
        display ('Warning: Se encontraron datos ya cargados para: '+columnName)

    columnName = 'Separacion'
    display ('Extrayendo informacion de: '+columnName)
    if not columnName in resumen.columns:
        temp = pd.DataFrame(columns=[columnName])
        for (i,r) in touchs.iterrows():
            temp.loc[i] = r['jsonMetaDataEstimulo']['infoConceptual']['separacion']
        resumen = pd.concat([resumen, temp], axis=1)
    else:
        display ('Warning: Se encontraron datos ya cargados para: '+columnName)

    columnName = 'SeJuntanSeleccion'
    display ('Extrayendo informacion de: '+columnName)
    if not columnName in resumen.columns:
        temp = pd.DataFrame(columns=[columnName])
        for (i,r) in touchs.iterrows():
            temp.loc[i] = r['jsonMetaDataTouched']['infoConceptual']['seJuntan']
        resumen = pd.concat([resumen, temp], axis=1)
    else:
        display ('Warning: Se encontraron datos ya cargados para: '+columnName)

    resumen['Aciertos'] = np.where(resumen['SeJuntanEstimulo']==resumen['SeJuntanSeleccion'], 'Acierto', 'Error')


    # Filtramos solo los datos de usuarios que hicieron los 26 niveles
    if experimentoUmbralCompleto:
        for user in touchs['userID'].unique():
            resumenFiltrado = resumen[resumen['userID']==user]
            if resumenFiltrado['AnguloReferencia'].unique().size != 26:
                resumen = resumen[resumen['userID']!=user]

    display (resumen['Alias'].unique())
    display ('Resumen completado')

    return resumen

def histogramaAciertosVsOrientacionVsSeparacion(resumen):

    import seaborn as sns
    import matplotlib.pyplot as plt

    g = sns.FacetGrid(resumen, col="Alias")#, row="AnguloReferencia")
    g.map(sns.countplot, "SeJuntanSeleccion")
    g.add_legend()
