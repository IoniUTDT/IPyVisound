def plotConvergencia (touchs):
    
    import matplotlib.pyplot as plt
    import pandas as pd
        
    from IPython.display import display
    from Scripts import fechaLocal
    
    
    for usuario in touchs['Alias'].unique():
        display ('Se hara la estadistica del usuario: '+usuario)
        touchsUsuario = touchs[touchs['Alias']==usuario]
        display ('El usuario '+usuario+' jugo '+str(len(touchsUsuario['sessionInstance'].unique()))+' veces')
        for session in touchsUsuario['sessionInstance'].unique():
            touchsSession = touchsUsuario[touchsUsuario['sessionInstance']==session]

            # Analizamos los datos para dificultad generica
            display ('En la session '+ str(fechaLocal(session))+ ' el usuario '+str(usuario)+' jugo '+str(len(touchsSession['levelInstance'].unique())) + ' niveles')
            for level in touchsSession['levelInstance'].unique():

                touchsLevel = touchsSession[touchsSession['levelInstance']==level]
                
                # Extraemos la info de del delta tita del estimulo de cada trial
                columnName = 'DeltaTita'
                if not columnName in touchsLevel.columns:
                    temp = pd.DataFrame(columns=[columnName])
                    for (i,r) in touchsLevel.iterrows():
                        e = r['jsonMetaDataRta']
                        temp.loc[i] = [e['infoConceptual']['deltaAngulo']]
                    touchsLevel = pd.concat([touchsLevel, temp], axis=1)
                else:
                    display ('Warning: Se encontraron datos ya cargados para: '+columnName)
                    
                # Extraemos la info del angulo de referencia
                columnName = 'AnguloDeReferencia'
                if not columnName in touchsLevel.columns:
                    temp = pd.DataFrame(columns=[columnName])
                    for (i,r) in touchsLevel.iterrows():
                        e = r['jsonMetaDataRta']
                        temp.loc[i] = [e['infoConceptual']['direccionAnguloReferencia']]
                    touchsLevel = pd.concat([touchsLevel, temp], axis=1)
                else:
                    display ('Warning: Se encontraron datos ya cargados para: '+columnName)
                
                levelInfo = touchsLevel.iloc[0]
                touchsLevelTrue = touchsLevel[touchsLevel['isTrue']==True]
                touchsLevelFalse = touchsLevel[touchsLevel['isTrue']==False]
                
                # Armamos el grafico
                fig = plt.figure(figsize=(10,3))
                ax = fig.add_subplot(111)
                title = 'Evolucion de la dificultad en funcion del trial \n' + 'Usuario: '+str(usuario) + ' direccion de refrencia: ' + str(levelInfo['AnguloDeReferencia'])+' grados, ' + 'levelVersion '+str(levelInfo['levelVersion']) 
                ax.set_title(title, fontsize=10, fontweight='bold')
                ax.set_xlabel('Numero de trial')
                ax.set_ylabel('Delta Tita (grados)')
                x = touchsLevel.index
                y = touchsLevel['DeltaTita'].tolist()
                ax.plot(x,y)
                x = touchsLevelTrue.index
                y = touchsLevelTrue['DeltaTita'].tolist()
                ax.plot(x,y,'go')
                x = touchsLevelFalse.index
                y = touchsLevelFalse['DeltaTita'].tolist()
                ax.plot(x,y,'ro')