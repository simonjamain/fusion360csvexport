#Author-Simon JAMAIN
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback, csv

def saveParameterExpressions(parameterList):
    savedParameterExpressions = {}
    for parameterToSave in parameterList:
        savedParameterExpressions[parameterToSave.name] = parameterToSave.expression
    return savedParameterExpressions

def countCSVRows(fileName):
    with open(fileName) as fileName:
        csvReader = csv.reader(fileName)
        return sum(1 for row in csvReader)

def updateParameters(parametersListToUpdate, savedParameterExpressions):
    for parameterToUpdate in parametersListToUpdate:
        parameterToUpdate.expression = savedParameterExpressions[parameterToUpdate.name]

def run(context):
    ui = None
    
    try:
        app = adsk.core.Application.get()
        currentDesign = app.activeProduct
        ui  = app.userInterface
        
        csvFileDialog = ui.createFileDialog()
        csvFileDialog.isMultiSelectEnabled = False
        csvFileDialog.title = "select the parameters file"
        csvFileDialog.filter = 'Text files (*.csv)'
        
        if csvFileDialog.showOpen() == adsk.core.DialogResults.DialogOK:
            
            with open(csvFileDialog.filename) as csvFile:
                csvReader = csv.reader(csvFile)
                
                parametersNames = next(csvReader)
                
                nbVariants = countCSVRows(csvFileDialog.filename) - 1

                exportFolderDialog = ui.createFolderDialog()
                exportFolderDialog.title = str(nbVariants) + " parameter sets have been found, select an export directory"
                
                if exportFolderDialog.showDialog() == adsk.core.DialogResults.DialogOK:
                    
                    exportManager = currentDesign.exportManager                        
                    
                    previousParameterExpressions = saveParameterExpressions(currentDesign.userParameters)
                    try:
                        for parametersRow in csvReader:
                            
                            fileName = None                             
                            
                            for index,parameterCell in enumerate(parametersRow):
                                
                                parameterName = parametersNames[index]

                                if index == 0 and parameterName == "fileName":
                                    fileName = parameterCell
                                
                                elif index == 0 and parameterName != "fileName":
                                    raise Exception('Process Canceled !\nThe first column of your csv file must be a fileName parameter and the values should be a unique filename for each set of parameters.\nNote: you can also have another fileName attribute column and they won\'t interfear.')
                                
                                elif currentDesign.userParameters.itemByName(parameterName) is None :
                                    raise Exception('Process Canceled !\nParameter "' + parameterName + '" does not exists in fusion, please check the parameters names of the fusion project and match them to the csv file')
                                
                                else:
                                    currentDesignParameter = currentDesign.userParameters.itemByName(parameterName)
                                    currentDesignParameter.expression = parameterCell

                            fullFileName = exportFolderDialog.folder + "/" + fileName

                            stlExportOptions = exportManager.createSTLExportOptions(currentDesign.rootComponent, fullFileName)
                            stlExportOptions.sendToPrintUtility = False
        
                            exportManager.execute(stlExportOptions)
                        ui.messageBox("export success")
                    except Exception as e:
                        ui.messageBox(str(e))
                    finally:             
                        updateParameters(currentDesign.userParameters,previousParameterExpressions)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
