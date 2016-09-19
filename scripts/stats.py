import scripts.constants as cts

from scripts.general import chkVersion
from IPython.display import display
from scripts.general import fechaLocal
from scripts.db import pandasTransferencia


def sessionStats():

    data = pandasTransferencia()
    sessionInstances = data[cts.P_SessionInstance].unique()
    for sessionInstance in sessionInstances:
        infoSesion = data[data[cts.P_SessionInstance] == sessionInstance]
        display('El usuario ' + infoSesion.iloc[0][cts.P_Alias] + ' inicio sesion el ' + str(fechaLocal(sessionInstance)) + ' y juego ' + str(len(infoSesion[cts.P_LevelInstance].unique())) + ' niveles.')
        for levelInstance in data[data[cts.P_SessionInstance]==sessionInstance][cts.P_LevelInstance].unique():
            infoLevel = data[data[cts.P_LevelInstance] == levelInstance].iloc[0]
            display(' Level ' + infoLevel[cts.P_LevelIdentificador] + ' jugado a las: ' + str(fechaLocal(levelInstance)) + ' Envio de datos terminado a las: ' + str(fechaLocal(infoLevel[cts.P_EnvioInstance])))

def lastSessionStats(number=-1):

    data = pandasTransferencia()
    sessionInstances = data[cts.P_SessionInstance].unique()
    lastUser = data[cts.P_Alias].unique()[number]
    data = data[data[cts.P_Alias]==lastUser]
    sessionInstances = data[cts.P_SessionInstance].unique()
    for sessionInstance in sessionInstances:
        infoSesion = data[data[cts.P_SessionInstance] == sessionInstance]
        display ('El usuario ' + infoSesion.iloc[0][cts.P_Alias] + ' inicio sesion el ' + str(fechaLocal(sessionInstance)) + ' y juego ' + str(len(infoSesion[cts.P_LevelInstance].unique())) + ' niveles.')
        for levelInstance in data[data[cts.P_SessionInstance]==sessionInstance][cts.P_LevelInstance].unique():
            infoLevel = data[data[cts.P_LevelInstance] == levelInstance].iloc[0]
            display (' Level ' + infoLevel[cts.P_LevelIdentificador] + ' jugado a las: ' + str(fechaLocal(levelInstance)) + ' Envio de datos terminado a las: ' + str(fechaLocal(infoLevel[cts.P_EnvioInstance])))

def usersResumen():
    data = pandasTransferencia()
    for user in data[cts.P_Alias].unique():
        display ('El usuario ' + user + ' realizo entrenamiento en ' + str(data[data[cts.P_Alias]==user][cts.P_OrientacionEntrenamiento].unique()))
        display ('Y realizo los siguientes niveles: ' + str(data[data[cts.P_Alias]==user][cts.P_FaseActiva].unique()))
