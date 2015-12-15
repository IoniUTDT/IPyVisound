def crearTabla (touchs):

    from scripts.general import chkVersion
    chkVersion()

    import pandas as pd
    from IPython.display import display

    resumen = touchs[['jsonMetaDataTouched','jsonMetaDataRta','userID','Alias']]

    # Extraemos la info de los jsons
    columnName = 'AnguloReferencia'
    if not columnName in resumen.columns:
        temp = pd.DataFrame(columns=[columnName])
        for (i,r) in touchs.iterrows():
            temp.loc[i] = r['jsonMetaDataRta']['infoConceptual']['direccionAnguloReferencia']
        resumen = pd.concat([resumen, temp], axis=1)
    else:
        display ('Warning: Se encontraron datos ya cargados para: '+columnName)

    columnName = 'DeltaTita'
    if not columnName in resumen.columns:
        temp = pd.DataFrame(columns=[columnName])
        for (i,r) in touchs.iterrows():
            temp.loc[i] = r['jsonMetaDataRta']['infoConceptual']['deltaAngulo']
        resumen = pd.concat([resumen, temp], axis=1)
    else:
        display ('Warning: Se encontraron datos ya cargados para: '+columnName)

    columnName = 'SeJuntanEstimulo'
    if not columnName in resumen.columns:
        temp = pd.DataFrame(columns=[columnName])
        for (i,r) in touchs.iterrows():
            temp.loc[i] = r['jsonMetaDataRta']['infoConceptual']['seJuntan']
        resumen = pd.concat([resumen, temp], axis=1)
    else:
        display ('Warning: Se encontraron datos ya cargados para: '+columnName)

    columnName = 'SeJuntanSeleccion'
    if not columnName in resumen.columns:
        temp = pd.DataFrame(columns=[columnName])
        for (i,r) in touchs.iterrows():
            temp.loc[i] = r['jsonMetaDataTouched']['infoConceptual']['seJuntan']
        resumen = pd.concat([resumen, temp], axis=1)
    else:
        display ('Warning: Se encontraron datos ya cargados para: '+columnName)


    return resumen
