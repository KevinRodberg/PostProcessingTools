
import arcpy
import sys
import numpy
from pandas import *

sr = arcpy.SpatialReference(2881)
arcpy.env.overwriteOutput = True

workdir = r"//ad.sfwmd.gov/dfsroot/data/wsd/GIS/GISP_2012/DistrictAreaProj/CFWI/Data/Soils/"
Myworkspace = workdir + "ProcessDir.gdb"
ModelMesh =  r"\\ad.sfwmd.gov\dfsroot\data\wsd\GIS\GISP_2012\DistrictAreaProj\CFWI\Data\Soils\ECFTX_GRID_V3.shp"
"""
	Clip nrcs_soils_jun12 features to ECFTX model area
"""
SoilGroups = workdir + "ECFTXsoilHG.shp"
SoilModelMesh = Myworkspace + "/SoilHGModelMesh"
maxAreaSoilMesh = Myworkspace + "/maxAreaSoilHGMesh"
InterceptFeatures = ModelMesh + " #;" + SoilGroups + " #"
arcpy.Intersect_analysis(in_features=InterceptFeatures,out_feature_class=SoilModelMesh,join_attributes="ALL",cluster_tolerance="#",output_type="INPUT")
                            
arcpy.AddGeometryAttributes_management(Input_Features=SoilModelMesh,Geometry_Properties="AREA",Length_Unit="FEET_US",Area_Unit="SQUARE_FEET_US",Coordinate_System=sr)
                                                        
arcpy.Dissolve_management(in_features=SoilModelMesh,
	out_feature_class=maxAreaSoilMesh,
	dissolve_field="SEQNUM;HYDRGRP",statistics_fields="POLY_AREA SUM",multi_part="MULTI_PART",unsplit_lines="DISSOLVE_LINES")
# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "LECSAS_MMsoilHydGrp"
arcpy.Dissolve_management(in_features="LECSAS_MMsoilHydGrp", 
	out_feature_class="//ad.sfwmd.gov/dfsroot/data/wsd/GIS/GISP_2012/DataLib/ModelData/LECSAS/maxAreaSoilHGMesh.shp", 
	dissolve_field="Id;Column_;Row;ROWCO;hydgrpdcd", statistics_fields="POLY_AREA SUM", multi_part="MULTI_PART", unsplit_lines="DISSOLVE_LINES")

Soil_Mesh = maxAreaSoilMesh
Soil_Mesh_lyr = arcpy.MakeFeatureLayer_management(Soil_Mesh, "SoilHG_Mesh_lyr")

"""
	Figure out which attribute is needed from maxAreaSoilMesh
"""	


Soil_Mesh_nparr = arcpy.da.FeatureClassToNumPyArray(Soil_Mesh_lyr, ['FID','Id','Column_','Row','ROWCO','hydgrpdcd','SUM_POLY_A'])
Soil_Mesh_df = DataFrame(Soil_Mesh_nparr, columns=['SEQNUM','HYDRGRP','SUM_POLY_AREA'])
Soil_Mesh_df.columns=['SEQNUM','HYDRGRP','SOIL_AREA']
maxAreabySeq = Soil_Mesh_df.sort(['SOIL_AREA'],ascending=False).groupby(['SEQNUM'], as_index=False).first()        

Soilcsv = workdir + "predomSoilHG.csv"
maxAreabySeq.to_csv(Soilcsv,index=False)
pdomSoil = Myworkspace + "/PredomSoil"
arcpy.CopyRows_management(Soilcsv, pdomSoil)
arcpy.MakeFeatureLayer_management(in_features=ModelMesh,out_layer="memSoilHGMM",where_clause="#",workspace=Myworkspace)
arcpy.JoinField_management ("memSoilHGMM", "SEQNUM", pdomSoil, "SEQNUM")                                                   
