def fechaLocal (millisec):

    """
        Esta funcion transforma los timestamp que se crean en el programa visound a un formato amigable
    """
    import sys
    if not sys.version_info[:2] == (3, 4):
        print ('Sos un boludo!, pero uno previsor')
        print ('Este codigo esta pensado para correr en python 3.4')


    import datetime

    return datetime.datetime.fromtimestamp(millisec/1000)

def chkVersion():
    import sys
    if not sys.version_info[:2] == (3, 4):
        print ('Sos un boludo!, pero uno previsor')
        print ('Este codigo esta pensado para correr en python 3.4')
