
import arcpy
import sys
import numpy
from pandas import *

sr = arcpy.SpatialReference(2881)

workdir = r"//ad.sfwmd.gov/dfsroot/data/wsd/GIS/GISP_2012/DistrictAreaProj/CFWI/Data/Soils/"
Myworkspace = workdir + "ProcessDir.gdb"

ModelMesh =  r"\\ad.sfwmd.gov\dfsroot\data\wsd\GIS\GISP_2012\DistrictAreaProj\CFWI\Data\Soils\ECFTX_GRID_V3.shp"
SoilGroups = workdir + "ECFTXsoilMu.shp"
SoilModelMesh = Myworkspace + "/SoilModelMesh"
maxAreaSoilMesh = Myworkspace + "/maxAreaSoilMesh"
InterceptFeatures = ModelMesh + " #;" + SoilGroups + " #"
arcpy.Intersect_analysis(in_features=InterceptFeatures,out_feature_class=SoilModelMesh,join_attributes="ALL",cluster_tolerance="#",output_type="INPUT")
                            
arcpy.AddGeometryAttributes_management(Input_Features=SoilModelMesh,Geometry_Properties="AREA",Length_Unit="FEET_US",Area_Unit="SQUARE_FEET_US",Coordinate_System=sr)
                                                        
arcpy.Dissolve_management(in_features=SoilModelMesh,out_feature_class=maxAreaSoilMesh,dissolve_field="SEQNUM;MUKEY",statistics_fields="POLY_AREA SUM",multi_part="MULTI_PART",unsplit_lines="DISSOLVE_LINES")
              
Soil_Mesh = maxAreaSoilMesh
Soil_Mesh_lyr = arcpy.MakeFeatureLayer_management(Soil_Mesh, "Soil_Mesh_lyr")
Soil_Mesh_nparr = arcpy.da.FeatureClassToNumPyArray(Soil_Mesh_lyr, ['OBJECTID','SEQNUM','MUKEY','SUM_POLY_AREA'])
Soil_Mesh_df = DataFrame(Soil_Mesh_nparr, columns=['SEQNUM','MUKEY','SUM_POLY_AREA'])
Soil_Mesh_df.columns=['SEQNUM','MUKEY','SOIL_AREA']
maxAreabySeq = Soil_Mesh_df.sort(['SOIL_AREA'],ascending=False).groupby(['SEQNUM'], as_index=False).first()        

Soilcsv = workdir + "predominanteSoil.csv"
maxAreabySeq.to_csv(Soilcsv,index=False)
pdomSoil = Myworkspace + "/PredomSoil"
arcpy.CopyRows_management(Soilcsv, pdomSoil)
arcpy.MakeFeatureLayer_management(in_features=ModelMesh,out_layer="memSoilModelMesh",where_clause="#",workspace=Myworkspace)
arcpy.JoinField_management ("memSoilModelMesh", "SEQNUM", pdomSoil, "SEQNUM")                                                   
