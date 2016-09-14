import scripts.constants as cts

from scripts.general import chkVersion
from IPython.display import display
from scripts.general import fechaLocal
from scripts.db import pandasTransferencia

def filtroEtapaUno(data):
    for levelInstance in data[cts.P_LevelInstance].unique():
        dataParcial = data[data[cts.P_LevelInstance]==levelInstance]
        if dataParcial[cts.P_LevelIdentificador].iloc[0] in cts.expListToCut:
            condicionAlcanzada = False
            listaDeTrialsARemover = []
            nivelAAlcanzar = dataParcial[cts.P_NivelEstimuloDinamica].iget(-1)
            for index in dataParcial.index:
                display (index)
            display (dataParcial.tail())
            display (nivelAAlcanzar)
