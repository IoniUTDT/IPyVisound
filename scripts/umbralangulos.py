def plotConvergenciaAngulos (levels):
    """
        Esta función grafica el angulo en funcion del numero de trial para cada uno de los cuadrantes
    """

    import matplotlib.pyplot as plt
    import pandas as pd
    from IPython.display import display
    from scripts.general import fechaLocal
    import json

    from scripts.general import chkVersion
    chkVersion()

    for usuario in levels['Alias'].unique():
        display ('Se hara la estadistica del usuario: '+usuario)
        levelsUsuario = levels[levels['Alias']==usuario]
        display ('El usuario '+usuario+' jugo '+str(len(levelsUsuario['sessionInstance'].unique()))+' veces')
