
# Nombres que vienen del codigo del Java
Db_Envios_Key = 'Envio'
Db_Envios_TipoDeEnvioKey = 'tipo'
Db_Envios_InstanceKey = 'instance'
Db_Envios_TipoDeEnvio_Sesion = 'SESION'
Db_Envios_TipoDeEnvio_RESULTADOS = 'RESULTADOS'
Db_Envios_Contenido = 'objeto'

Db_Sesion_User = 'user'
Db_Sesion_User_Id = 'id'
Db_Sesion_User_Fase = 'faseDeExperimentoActiva'
Db_Sesion_User_Eleccion = 'eleccion'

Db_Sesion_Instance = 'sessionInstance'
Db_Sesion_CodeVersion = 'codeVersion'

Db_Resultados_NivelLog = 'levelLog'
Db_Resultados_NivelLog_LevelInstance = 'instance'
Db_Resultados_NivelLog_LevelIdentificador = 'identificadorNivel'
Db_Resultados_NivelLog_Sesion = 'sesion'

Db_Resultados_Dinamica = 'dinamica'
Db_Resultados_Dinamica_IdentificadorLevel = 'identificadorNivel'
Db_Resultados_Dinamica_Finalizado = 'levelFinalizadoCorrectamente'
Db_Resultados_Dinamica_Referencia = 'referencia'
Db_Resultados_Dinamica_Historial = 'historial'

Db_Historial_RtaCorrecta = 'acertado'
Db_Historial_Confianza = 'confianza'
Db_Historial_EstimuloDinamica = 'nivelEstimulo'
Db_Historial_TiempoRta = 'selectionTimeInTrial'
Db_Historial_TiempoConfianza = 'confianceTimeInTrial'
Db_Historial_loops = 'soundLoops'
Db_Historial_TipoDeTrial = 'trialType'
Db_Historial_Recurso = 'estimulo'
Db_Historial_Recurso_AnguloFijo = 'anguloFijo'
Db_Historial_Recurso_Desviacion = 'desviacion'
Db_Historial_Recurso_Estimulo = 'nivelSenal'
Db_Historial_Recurso_Id = 'idResource'
Db_Historial_Recurso_EtiquetaTipoEstimulo = 'Estimulo'
Db_Historial_Recurso_EtiquetaTipoNoEstimulo = 'NoEstimulo'
Db_Historial_Recurso_EtiquetaTipoTest = 'Test'

# Estructuras dict de python
Db_Users_id = 'id'
Db_Users_Alias = 'alias'
Db_Users_Ignore = 'ignore'
Db_Users_UserId = 'UserId'

# Estructura del pandas
P_SessionInstance = 'sessionInstance'
P_Alias = 'alias'
P_LevelInstance = 'levelInstance'
P_LevelIdentificador = 'identificadorNivel'
P_UserId = 'userId'
P_FaseActiva = 'faseActiva'
P_OrientacionEntrenamiento = 'OrientacionEntrenamiento'
P_CodeVersion = 'CodeVersion'
P_LevelFinalizado = 'Finalizado'
P_Referencia = 'Refrencia'
P_RtaCorrecta = 'RtaCorrecta'
P_NivelConfianza = 'NivelConfianza'
P_NivelEstimuloDinamica = 'NivelSenalDinamica'
P_TiempoRespuesta = 'TiempoRespuestaCategoria'
P_TiempoRespuestaConfianza = 'TiempoRespuestaCategoriaMasConfianza'
P_NumeroDeLoopsAudio = 'LoopsDelAudio'
P_TipoDeTrial = 'TipoDeTrial'
P_AnguloFijo = 'AnguloFijo'
P_Desviacion = 'Desviacion'
P_NivelEstimuloEstimulo = 'NivelSenalEstimulo'
P_IdEstimulos = 'IdEstimulo'
P_EnvioInstance = 'EnvioInstance'

# Constantes utiles localmente
PathDirDatosLocal = './Guardados/datos.'
PATHALIAS = PathDirDatosLocal + 'Alias'
PATHSESSSION = PathDirDatosLocal + Db_Envios_TipoDeEnvio_Sesion
PATHLEVELS = PathDirDatosLocal + 'NewLevel'
PATHRESULTS = PathDirDatosLocal + 'RESULTADOS'

#Otras Constantes
expList = ['ParalelismoTutorial', 'AngulosTutorial',
        'TESTP30', 'TESTP60', 'TESTP120', 'TESTP150',
        'TESTA30', 'TESTA60', 'TESTA120', 'TESTA150',
        'ENTRENAMIENTOA60INICIAL', 'ENTRENAMIENTOP60INICIAL',
        'ENTRENAMIENTOA60MEDIO','ENTRENAMIENTOA120MEDIO', 
        'ENTRENAMIENTOP30INICIAL','ENTRENAMIENTOP30MEDIO',
        'ENTRENAMIENTOP30FINAL']

URLserver = 'http://turintur.dynu.com/db'
FileNameLocalDb = 'db.json'
FileNameLocalDbTemp = 'temp.json'
PathDirDbBackUp = './backups/'
