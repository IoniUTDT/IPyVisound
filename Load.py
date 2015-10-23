def LoadDataFromFile ():
    
    import json
    import pandas as pd
    import numpy as np
    
    filename = 'db.json'
        
    with open(filename) as data_file:    
        db = json.load(data_file)

    # Cargo la data de las sesiones en una tabla pandas
    sessions = pd.concat((pd.DataFrame(x) for x in db['SessionEnviables']), ignore_index=True)
    sessions['sessionInstance'] = sessions['id']
    # Cargo de los niveles
    levels = pd.concat((pd.DataFrame(x) for x in db['LevelEnviables']), ignore_index=True)

    trials = pd.concat((pd.DataFrame(x) for x in db['TrialEnviables']), ignore_index=True)

    touchs = pd.concat(pd.DataFrame(x) for x in list(trials['touchLog']) if x is not np.nan)
    sounds = pd.concat(pd.DataFrame(x) for x in list(trials['soundLog']) if x is not np.nan)
    touchs = pd.merge(touchs, trials, on='trialInstance', suffixes=['', '_trial'])
    touchs = pd.merge(touchs, levels, on='levelInstance', suffixes=['', '_level'])
    touchs = pd.merge(touchs, sessions, on='sessionInstance')
    name_map = {user_id: alias for alias, user_id in enumerate(touchs['userID'].unique())}
    touchs['Alias'] = touchs['userID'].map(name_map)
    usuarios.rename(columns={'index': 'Alias'}, inplace=True)    
    return touch
