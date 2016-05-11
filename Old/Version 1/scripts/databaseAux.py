def joinDB(touchs, sounds, tag, identificador):

    """
        Funcion que acumula en archivos con formato piclke los touchs y sounds ya en formato limpio (no como vienen en la base de datos json) a una base de datos mas general verificando de no duplicar datos.
        el tag es un texto corto que sirve para describir cada anexion de datos y el identificador que es una string corto para usar despues de filtro.
    """

    import os
    import pandas as pd
    from IPython.display import display

    # Creamos una base de datos vacia
    touchsToJoin = touchs.copy()
    soundsToJoin = sounds.copy()

    # Cargamos los datos ya guardados
    display ('Verificando datos guardados previamente')
    filenameTouchs = 'dbTouchs'
    filenameSounds = 'dbSounds'

    if os.path.isfile(filenameTouchs):
        touchsLoad = pd.read_pickle(filenameTouchs)
        display ('Datos de touchs previos cargados')
    else:
        display ('Datos de touchs previos inexistentes')
        touchsLoad = pd.DataFrame()

    if os.path.isfile(filenameSounds):
        soundsLoad = pd.read_pickle(filenameSounds)
        display ('Datos de sounds previos cargados')
    else:
        display ('Datos de sounds previos inexistentes')
        soundsLoad = pd.DataFrame()


    # Limpiamos de los touchs a almacenar los que ya estan almacenados
    if touchsLoad.index.size>0:
        for (i,r) in touchsLoad.iterrows():
            touchsToJoin.drop(touchsToJoin.index[touchsToJoin['touchInstance'] == r['touchInstance']], inplace=True)
    touchsToJoin['TagJoin'] = tag
    touchsToJoin['identificador'] = identificador

    # Limpiamos de los sounds a almacenar los que ya estan almacenados
    if soundsLoad.index.size>0:
        for (i,r) in soundsLoad.iterrows():
            soundsToJoin.drop(soundsToJoin.index[soundsToJoin['soundInstance'] == r['soundInstance']], inplace=True)
    soundsToJoin['TagJoin'] = tag
    soundsToJoin['identificador'] = identificador

    soundsLoad = soundsLoad.append(soundsToJoin, ignore_index=True)
    display ('Agregados '+str(soundsToJoin.index.size)+' entradas a los sounds')
    soundsLoad.to_pickle(filenameSounds)
    touchsLoad = touchsLoad.append(touchsToJoin, ignore_index=True)
    display ('Agregados '+str(touchsToJoin.index.size)+' entradas a los touchs')
    touchsLoad.to_pickle(filenameTouchs)


def loadFromDb(identificador=0):

    """
        Funcion que devuelve todos los touchs y sounds filtrando por un string identificador. El valor 0 equivale a no filtrar los datos.
    """
    import sys
    if not sys.version_info[:2] == (3, 4):
        print ('Sos un boludo!, pero uno previsor')
        print ('Este codigo esta pensado para correr en python 3.4')

    import os
    import pandas as pd
    from IPython.display import display

    display ('Verificando datos guardados previamente')
    filenameTouchs = 'dbTouchs'
    filenameSounds = 'dbSounds'

    if os.path.isfile(filenameTouchs):
        touchsLoad = pd.read_pickle(filenameTouchs)
        display ('Datos de touchs previos cargados')
    else:
        display ('Datos de touchs previos inexistentes')
        touchsLoad = pd.DataFrame()

    if os.path.isfile(filenameSounds):
        soundsLoad = pd.read_pickle(filenameSounds)
        display ('Datos de sounds previos cargados')
    else:
        display ('Datos de sounds previos inexistentes')
        soundsLoad = pd.DataFrame()

    if identificador!=0:
        touchsLoad = touchsLoad[touchsLoad['identificador']==identificador]
        soundsLoad = soundsLoad[soundsLoad['identificador']==identificador]

    return touchsLoad, soundsLoad


def guardarComo (touchs, filename):

    """
        Funcion que sirve para guardar un conjunto de touchs con un nombre particular
    """
    import pandas as pd
    import os
    from IPython.display import display

    import sys
    if not sys.version_info[:2] == (3, 4):
        print ('Sos un boludo!, pero uno previsor')
        print ('Este codigo esta pensado para correr en python 3.4')

    if os.path.isfile(filename):
        display ('Ya existe una base de datos con ese nombre')
    else:
        display ('Archivo guardado')
        touchs.to_pickle('./Guardados/'+filename)

def guardarComoSounds (sounds, filename):

    """
        funcion que sirve para guardar en formato pikle un determinado conjunto de sounds con un nombre especifico
    """
    import pandas as pd
    import os
    from IPython.display import display

    import sys
    if not sys.version_info[:2] == (3, 4):
        print ('Sos un boludo!, pero uno previsor')
        print ('Este codigo esta pensado para correr en python 3.4')

    if os.path.isfile(filename):
        display ('Ya existe una base de datos con ese nombre')
    else:
        display ('Archivo guardado')
        sounds.to_pickle(filename)

def cargarTouchs (filename):
    """
        funcion que carga un conjunto de touchs previamente guardado en formato pickle con un nombre especifico.
    """
    import sys
    if not sys.version_info[:2] == (3, 4):
        print ('Sos un boludo!, pero uno previsor')
        print ('Este codigo esta pensado para correr en python 3.4')

    import pandas as pd
    import os
    from IPython.display import display

    if os.path.isfile(filename):
        return pd.read_pickle (filename)
    else:
        display ('No existe una base de datos guardada con el nombre: '+filename)


def guardarPickle (touchs, sounds, filename):

    """
        Esta funcion guarda touchs y sounds en formato pickle. Englobna otras. Revisar superposicion
    """

    import pandas as pd
    import os
    from IPython.display import display

    import sys
    if not sys.version_info[:2] == (3, 4):
        print ('Sos un boludo!, pero uno previsor')
        print ('Este codigo esta pensado para correr en python 3.4')

    if os.path.isfile('./Guardados/'+filename+'.touch'):
        display ('Ya existe una base de datos con ese nombre')
    else:
        display ('Archivo guardado')
        touchs.to_pickle('./Guardados/'+filename+'.touch')
        sounds.to_pickle('./Guardados/'+filename+'.sounds')

def cargarPickle (filename):

    """
        Esta funcion carga touchs y sounds en formato pickle. Englobna otras. Revisar superposicion
    """

    import pandas as pd
    import os
    from IPython.display import display

    import sys
    if not sys.version_info[:2] == (3, 4):
        print ('Sos un boludo!, pero uno previsor')
        print ('Este codigo esta pensado para correr en python 3.4')

    if os.path.isfile('./Guardados/'+filename+'.touch'):
        touchs = pd.read_pickle ('./Guardados/'+filename+'.touch')
    else:
        display ('Error, no se encontro los touchs buscados')
        return

    if os.path.isfile('./Guardados/'+filename+'.sounds'):
        sounds = pd.read_pickle ('./Guardados/'+filename+'.touch')
    else:
        display ('Error, no se encontro los sounds buscados')
        return

    return touchs, sounds
