def recreateDb ():

    from scripts.general import chkVersion
    chkVersion()

    from scripts.extract import join
    from IPython.display import display
    import glob, os, time
    from os import path
    from datetime import datetime, timedelta

    #os.chdir('/backups/')
    for file in glob.glob("./backups/*.json"):
        display (file)
        fileCreation = datetime.fromtimestamp(path.getctime(file))
        tiempolimite = datetime.now() - timedelta(days=14)
        display (fileCreation > tiempolimite)
        if fileCreation > tiempolimite:
            join(file)

    Display ('FIN!')
