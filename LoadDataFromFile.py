def LoadDataFromFile ():
    
    import json
    import pandas as pd
    import numpy as np
    
    filename = 'db.json'
        
    with open(filename) as data_file:    
        db = json.load(data_file)

    # Cargo la data de las sesiones en una tabla pandas
    sessions = pd.concat((pd.DataFrame(x) for x in db['SessionEnviables']), ignore_index=True)
    # Transformo la info de los logueos en formato unixtime a una fecha legible (en zona horaria GTM=0)
    sessions['sessionDate'] = pd.to_datetime(sessions['id'], unit='ms')
    # Cargo de los niveles
    levels = pd.concat((pd.DataFrame(x) for x in db['LevelEnviables']), ignore_index=True)
    # Carga las fechas en formato legible para todo lo que corresponda
    levels['fechaEnvio'] = pd.to_datetime(levels['idEnvio'], unit='ms')
