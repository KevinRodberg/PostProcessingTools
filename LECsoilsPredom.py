
import arcpy
import sys
import numpy
from pandas import *
arcpy.env.overwriteOutput = True

workdir = r'//ad.sfwmd.gov/dfsroot/data/wsd/GIS/GISP_2012/DataLib/ModelData/LECSAS/'
Myworkspace = workdir+ 'soilWork.gdb'
Soil_Mesh = r'\\ad.sfwmd.gov\dfsroot\data\wsd\GIS\GISP_2012\DataLib\ModelData\LECSAS\maxAreaSoilHGMesh.shp'
Soil_Mesh_lyr = arcpy.MakeFeatureLayer_management(Soil_Mesh, "SoilHG_Mesh_lyr")
ModelMesh =r'\\ad.sfwmd.gov\dfsroot\data\wsd\GIS\GISP_2012\DataLib\ModelData\LECSAS\LECSAS_MM.shp'
"""
              Figure out which attribute is needed from maxAreaSoilMesh
"""           


#Soil_Mesh_nparr = arcpy.da.FeatureClassToNumPyArray(Soil_Mesh_lyr, ['OBJECTID','SEQNUM','HYDRGRP','SUM_POLY_AREA'])
Soil_Mesh_nparr = arcpy.da.FeatureClassToNumPyArray('SoilHG_Mesh_lyr', ['Id','hydgrpdcd','SUM_POLY_A'])

#Soil_Mesh_df = DataFrame(Soil_Mesh_nparr, columns=['SEQNUM','HYDRGRP','SUM_POLY_AREA'])
Soil_Mesh_df = DataFrame(Soil_Mesh_nparr, columns=['Id','hydgrpdcd','SUM_POLY_A'])

Soil_Mesh_df.columns=['SEQNUM','HYDRGRP','SOIL_AREA']
maxAreabySeq = Soil_Mesh_df.sort(['SOIL_AREA'],ascending=False).groupby(['SEQNUM'], as_index=False).first()        

Soilcsv = workdir + "predomSoilHG.csv"
maxAreabySeq.to_csv(Soilcsv,index=False)
pdomSoil = Myworkspace + "/PredomSoil"
arcpy.CopyRows_management(Soilcsv, pdomSoil)
arcpy.MakeFeatureLayer_management(in_features=ModelMesh,out_layer="memSoilHGMM",where_clause="#",workspace=Myworkspace)
arcpy.JoinField_management ("memSoilHGMM", "SEQNUM", pdomSoil, "Id")                                                   
