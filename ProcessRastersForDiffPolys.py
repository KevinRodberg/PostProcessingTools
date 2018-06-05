import arcpy
arcpy.env.overwriteOutput = True 
#---------------------------------
#	Set Spatial Reference for State Plane Feet HARN83 Florida East
#--------------------------------
SR = arcpy.SpatialReference(2881)

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

DiffMapGDB = []
DiffMapGDB.append(r'//ad.sfwmd.gov/dfsroot/data/wsd/GIS/GISP_2012/WorkingDirectory/KAR/ModflowProcessing/PythonTools/NPALM/NPBFWOvsALT2.gdb')
DiffMapGDB.append(r'//ad.sfwmd.gov/dfsroot/data/wsd/GIS/GISP_2012/WorkingDirectory/KAR/ModflowProcessing/PythonTools/NPALM/NPBFWOvsALT5.gdb')
DiffMapGDB.append(r'//ad.sfwmd.gov/DFSRoot/data/wsd/GIS/GISP_2012/WorkingDirectory/KAR/ModflowProcessing/PythonTools/NPALM/NPBFWOvsALT10.gdb')
DiffMapGDB.append(r'//ad.sfwmd.gov/dfsroot/data/wsd/GIS/GISP_2012/WorkingDirectory/KAR/ModflowProcessing/PythonTools/NPALM/NPBFWOvsALT12.gdb')
DiffMapGDB.append(r'//ad.sfwmd.gov/dfsroot/data/wsd/GIS/GISP_2012/WorkingDirectory/KAR/ModflowProcessing/PythonTools/NPALM/NPBFWOvsALT13.gdb')
get_SpatialA()
#--------------------------------
#  Loop through list of geodatabases each with raster layers representing water level differences from the NPB LECsR model
#
for dMap in DiffMapGDB:
  print dMap
  outGDB = dMap
  tempASCII = "h:/RasterT_rasterc1.TXT"
  tempPoly = outGDB + '/TempPoly'
#--------------------------------
#  Loop through list of Rasters in the current geodatabase and convert it to a polygon feature class
#--------------------------------
  arcpy.env.workspace = dMap
  fRasList = arcpy.ListRasters()
  for f in fRasList:
    print f
    rasFloat = arcpy.Raster(f)
    rasFloat = arcpy.sa.Times(rasFloat,100)
    arcpy.RasterToASCII_conversion(rasFloat, out_ascii_file=tempASCII)
    iRas = outGDB +'/' + f
    iPoly = outGDB + '/' + f + '_poly'
    arcpy.ASCIIToRaster_conversion(in_ascii_file=tempASCII,out_raster=iRas,data_type="INTEGER")
    arcpy.RasterToPolygon_conversion(in_raster=iRas,out_polygon_features=tempPoly,raster_field="Value")
    arcpy.Dissolve_management(in_features=tempPoly, out_feature_class=iPoly, dissolve_field="gridcode", statistics_fields="", 
                            multi_part="MULTI_PART", unsplit_lines="DISSOLVE_LINES")
    arcpy.AddField_management(iPoly,"WL_diff","FLOAT")
    arcpy.CalculateField_management(in_table=fc, field="WL_diff",
                                    expression="!gridcode! / 100.0",
                                    expression_type="PYTHON_9.3", code_block="")