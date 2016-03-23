def sessionStats():

    from scripts.db import pandasUtilPiloto
    from IPython.display import display
    from scripts.general import fechaLocal

    dbPiloto = pandasUtilPiloto()
    sessionInstances = dbPiloto['sessionInstance'].unique()
    for sessionInstance in sessionInstances:
        dbPilotoBySession = dbPiloto[dbPiloto['sessionInstance'] == sessionInstance]
        display ('El usuario ' + dbPilotoBySession.iloc[0]['alias'] + ' inicio sesion el ' + str(fechaLocal(sessionInstance)) + ' y juego ' + str(len(dbPilotoBySession['levelInstance'])) + ' niveles.')
