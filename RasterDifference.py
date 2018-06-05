"""
..module:: RasterDiff
    :platform: Windows
    ::creation: 04-Feb-2016
    :purpose:  Create raster differences where raster names match across 2 workspaces
..moduleauthor:: Kevin A. Rodberg <krodberg@sfwmd.gov>
"""

import os
import arcpy
from argparse import ArgumentParser

def getOptions():
    """Return command line arguments and options.

    -h              --help          Show help message and exit
 [Positional arguments:]
    bgdb                    Rasters to be subtracted from found in B-geoDatabase

 [Arguments required with the following Options:]

    -fgeo FGDB              Rasters names from F-geoDatabase found in B-geoDatabase will be subtracted (B-F)
    -one  rasterName        
    -rasras [FirstRaster, SecondRaster]
    -ogeo GEODB             Saves rasters in GeoDatabase
        
  [for instance:]
  
   C:\python27\arcGIS10.2\python T:\RasterDifference.py T:\WCFM\WCFMbase.gdb -fgeo T:\WCFM\WCFMfb.gdb -ogeo=T:\WCFM\WCFMdiffs.gdb
   or
   C:\python27\arcGIS10.2\python T:\RasterDifference.py T:\WCFM\WCFMbase.gdb  -one T:\WCFM\WCFMbase.gdb\HEAD_00012_1 -ogeo t:\WCFM\WCFMdiffsV1.gdb    
   or
   C:\python27\arcGIS10.2\python T:\RasterDifference.py T:\WCFM\WCFMbase.gdb  -one T:\WCFM\WCFMbase.gdb\clpHEAD_00012_1 -ogeo t:\WCFM\WCFMclpDiffsV2.gdb    
   or
   C:\python27\arcGIS10.2\python T:\RasterDifference.py L:\MB\GIS\Spatial\TDS\gdb\KARecfmtds2016b.gdb -rasras L:\MB\GIS\Spatial\TDS\gdb\KARecfmtds2016b.gdb\CONC_08766_1 L:\MB\GIS\Spatial\TDS\gdb\KARecfmtds2016b.gdb\CONC_00365_1 -ogeo L:\MB\GIS\Spatial\TDS\gdb\KARtdsDiffs.gdb
   

   
"""
    parser = ArgumentParser(prog='RasterDifference')
    parser.add_argument("bgdb",
                        help="Rasters to be subtracted from found in B-geoDatabase")
    parser.add_argument("-fgeo",dest="fgdb",
                        help="Rasters from F-geoDatabase will be subtracted from rasters in B-geoDatabase")
    parser.add_argument("-one",dest="oneras",
                        help="Single Raster is subtracted from by each raster in the B-geoDatabase (One Raster - B Rasters)")
    parser.add_argument("-rasras",nargs=2,dest="rasras",
                        help="SecondRaster is subtracted from FirstRaster:  -rasras FirstRaster SecondRaster")
    parser.add_argument("-ogeo",dest="ogdb",default='Default.gdb',
                        help="Rasters will be saved in O-geoDatabase.  Default value is: Default.gdb")

    args = parser.parse_args()
    print (args)
 
    return args

def setModelOrigins():
    
   # Provide Default Sparial Reference to assure output is properly projected
    global SR
    SR = arcpy.SpatialReference(2881)
    
   # Model origins are not currently needed but are useful for reference
    modelOrigins = dict(C4CDC=arcpy.Point(763329.000,437766.000),
                        ECFM=arcpy.Point(565465.000,-44448.000),
                        ECFT=arcpy.Point(330706.031,1146903.250),
                        LECSR=arcpy.Point(680961.000,318790.000),
                        NPALM=arcpy.Point(680961.000,840454.000),                        
                        LKBGWM=arcpy.Point(444435.531,903882.063),
                        LWCFAS=arcpy.Point(438900.000,-80164.000),
                        LWCSAS=arcpy.Point(292353.000,456228.000),
                        WCFM=arcpy.Point(20665.000,-44448.000)
                        )
    return

def get_SpatialA():
    arcpy.CheckInExtension("Spatial")   
    # Check out the ArcGIS Spatial Analyst extension license
    availability = arcpy.CheckExtension("Spatial")
    if availability == "Available":
        arcpy.CheckOutExtension("Spatial")
    else:
        arcpy.AddError("%s extension is not available (%s)"%("Spatial Analyst Extension",availability))
        arcpy.AddError("Please ask someone who has it checked out but not using to turn off the extension")
        exit()
    return(availability)
 
def define_workspace(geodb,usetype):
    
    # Set base paths for Modflow namefile and ESRI workspace.
    out_folder_path = "H:\\Documents\\ArcGIS"

    if geodb == "Default.gdb":
        out_name = "Default.gdb"
        print ("Default geodatabase path defined as: {}".format(out_folder_path))
    elif geodb <> None:
        (temp_path, gdbfile) = os.path.split(geodb)
        out_folder_path = temp_path
        out_name = geodb        
    else:
        print ("Unspecified working path.  Assigning: {}".format(path))
        out_folder_path =  path
        (out_folder_path, gdbfile) = os.path.split(out_folder_path)
        out_name = gdbfile

    workspace = os.path.join(out_folder_path, gdbfile)
    print ("Workspace: {} exists: {}".format(workspace, arcpy.Exists(workspace)))
    
    if not arcpy.Exists(workspace):
        print ("Workspace does not exist...")
        if usetype == 'input':
            print ("Input workspace required.  Please provide valid input workspace")
            exit()
        else:
            (temp_path, gdbfile) = os.path.split(workspace)
            if temp_path == "":
                temp_path = out_folder_path
            print "Creating: " + temp_path    +     gdbfile
            arcpy.CreateFileGDB_management(temp_path, gdbfile)
            arcpy.env.workspace = os.path.join(temp_path, gdbfile)
    else:
        arcpy.env.workspace = workspace
        
    print("{} processes are using:  {}".format(usetype ,workspace))
    arcpy.env.overwriteOutput = True 
    return arcpy.env.workspace

def myListDatasets(workspace):
    # Creates arry list of Rasters from workspace
    arcpy.env.workspace = workspace
    datasetList = arcpy.ListDatasets("*", "Raster")
    arraylist = []
    
    for dataset in datasetList:
        ##get path
        desc = arcpy.Describe(dataset)
        ## append to list
        arraylist.append(desc.catalogPath)
    return arraylist  

model_choices = setModelOrigins()
options = getOptions()

if options.bgdb == None or (options.rasras == None
                            and options.fgdb == None
                            and options.oneras == None):
    """
    Provide warning that required arguments must be supplied
    """
    print ("""Unable to process Raster data without bgdb and 
    (fgdb workspace or single raster) details.""")
    exit()
    
if options.ogdb:
    oWorkspace = define_workspace(options.ogdb,'output')
if options.bgdb:
    bWorkspace = define_workspace(options.bgdb,'input')
if options.fgdb:
    fWorkspace = define_workspace(options.fgdb,'input')

get_SpatialA()

arraylistB = myListDatasets(bWorkspace)

# List  datasets and print Features for fgdb
if options.fgdb:
    arcpy.env.workspace = fWorkspace
    fRasList = arcpy.ListRasters()
    for fRas in fRasList:
        for bRas in arraylistB:
            (temp_path, ras) = os.path.split(bRas)
            if fRas == ras:
                rasType, stressPeriod, layer = ras.split("_",2)
                rasType, stressPeriod, layer
                outputName = "D_"+ ras
            
                ras1 = arcpy.Raster(bRas)
                ras2 = arcpy.Raster(ras)
                oras = ras1 - ras2
                
                results = os.path.join(oWorkspace,outputName)

                print ("{} minus {} equals {}".format(ras1,ras2,outputName))
                oras.save(results)
                
if options.oneras:
    (temp_path, initRaster) = os.path.split(options.oneras)
    initRasType, initSP, initLay = initRaster.split("_",2)
    print (arraylistB)
    for bRas in arraylistB:
        (temp_path, ras) = os.path.split(bRas)
        rasType, stressPeriod, layer = ras.split("_",2)
        if initRasType == rasType:
            if initLay == layer:
                outputName = rasType + "_diff_" + stressPeriod + "_" + layer
                ras2 = arcpy.Raster(bRas)
                ras1 = arcpy.Raster(options.oneras)
                oras = ras2 - ras1
                results = os.path.join(oWorkspace,outputName)
                if arcpy.TestSchemaLock(results) or not arcpy.Exists(results):
                    print ("{} minus {} equals {}".format(ras2,ras1,outputName))
                    oras.save(results)
                else:
                	print ("Output SKIPPED [Schema lock present]. Can't save {}".format(results))
            else:
                print ("Layers Do Not Match [{} <> {}]".format(initLay,layer))
        else:
            print ("Raster Types Do Not Match[{} <> {}]".format(initRasType,rasType))
if options.rasras:           
    print options.rasras
    (temp_path,Ras1) = os.path.split(options.rasras[0])
    (temp_path,Ras2) = os.path.split(options.rasras[1])
    rasType1, stressPeriod1, layer1 = Ras1.split("_",2)
    rasType2, stressPeriod2, layer2 = Ras2.split("_",2)
    if rasType1 == rasType2 and layer1 == layer2:
        outputName = rasType1 +'_'+layer1 + '_'+stressPeriod1 + "_"+stressPeriod2
        print outputName
    else:
        print('rasters are mismatched')
        
    ras1 = arcpy.Raster(options.rasras[0])
    ras2 = arcpy.Raster(options.rasras[0])
    oras = ras1 - ras2
    results = os.path.join(oWorkspace,outputName)
    if arcpy.TestSchemaLock(results) or not arcpy.Exists(results):
        print ("{} minus {} equals {}".format(ras1,ras2,outputName))
        oras.save(results)
    
print ("End of Execution")