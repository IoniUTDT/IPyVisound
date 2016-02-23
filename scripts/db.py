def downloadFile ():

    """
        Esta funcion descarga la base de datos en formato json del servidor y hace una backup del archivo anterior.
    """

    import datetime
    import time
    import urllib
    import os

    from scripts.general import chkVersion
    chkVersion()

    url='http://turintur.dynu.com/db'
    filenameTemp = 'temp.json'
    filename = 'db.json'
    timestamp = time.time()
    st = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    filenameBackup = './backups/' + filename[:-5] + ' backup ' + st + '.json'

    print ('Starting download, please wait')

    # Bajamos el archivo
    urllib.request.urlretrieve(url, filenameTemp)


    # Renombramos el archivo viejo y dejamos el descargado con el nombre que corresponde si se descargo bien
    if os.path.isfile(filenameTemp):
        if os.path.isfile(filename):
            os.rename(filename,filenameBackup)
        os.rename(filenameTemp,filename)

    print ('Donload finish')
