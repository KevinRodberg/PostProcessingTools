
import arcpy
import sys
import numpy
from pandas import *

sr = arcpy.SpatialReference(2881)
workdir = r"//ad.sfwmd.gov/dfsroot/data/wsd/GIS/GISP_2012/WorkingDirectory/KAR/ModflowProcessing/PythonTools/LWCSIM/LandUse/"
#workdir = r"//ad.sfwmd.gov/dfsroot/data/wsd/GIS/GISP_2012/DistrictAreaProj/CFWI/Data/ProcessDir/"
Myworkspace = workdir + "PredomLWCSIM_LU.gdb"
LandUse=r"//ad.sfwmd.gov/dfsroot/data/wsd/mod/LWCSASIAS/GIS/LSI_process.gdb/"

LU2000= LandUse + "LU_2000_Union"
LU2004= LandUse + "LU_2004_Union"
LU2010= LandUse + "LU_2010_Union"
LU2014= r"//ad.sfwmd.gov/dfsroot/data/wsd/GIS/GISP_2012/DistrictWideProj/LandUse/2015/LU2014.gdb/LWC/LWCSIM_All_081214"

ModelMesh =  Myworkspace + "/LWCSIM_mesh"

LU00ModelMesh = Myworkspace + "/LU00ModelMesh"
LU04ModelMesh = Myworkspace + "/LU04ModelMesh"
LU10ModelMesh = Myworkspace + "/LU10ModelMesh"
LU14ModelMesh = Myworkspace + "/LU14ModelMesh"

maxAreaLU00Mesh = Myworkspace + "/maxAreaLU00Mesh"
maxAreaLU04Mesh = Myworkspace + "/maxAreaLU04Mesh"
maxAreaLU10Mesh = Myworkspace + "/maxAreaLU10Mesh"
maxAreaLU14Mesh = Myworkspace + "/maxAreaLU14Mesh"


#			Process 2000 Land Use

InterceptFeatures = ModelMesh + " #;" + LU2000 + " #"
arcpy.Intersect_analysis(in_features=InterceptFeatures,out_feature_class=LU00ModelMesh,join_attributes="ALL",cluster_tolerance="#",output_type="INPUT")

# Add Geometry Time : (Elapsed Time:  minutes  seconds)
arcpy.AddGeometryAttributes_management(Input_Features=LU00ModelMesh,Geometry_Properties="AREA",Length_Unit="FEET_US",Area_Unit="SQUARE_FEET_US",Coordinate_System=sr)
#

#   PAUSE for command to complete.  Add Geometry needs to be ran from the tool.  Double click failed entry in Results window.

# Dissolve Time: (Elapsed Time: 28 minutes 32 seconds)
arcpy.Dissolve_management(in_features=LU00ModelMesh,out_feature_class=maxAreaLU00Mesh,dissolve_field="SEQNUM;LU_CODE_2000",statistics_fields="POLY_AREA SUM",multi_part="MULTI_PART",unsplit_lines="DISSOLVE_LINES")

LU_Mesh = maxAreaLU00Mesh
LU_Mesh_lyr = arcpy.MakeFeatureLayer_management(LU_Mesh, "LU_Mesh_lyr")
LU_Mesh_nparr = arcpy.da.FeatureClassToNumPyArray(LU_Mesh_lyr, ['OBJECTID','SEQNUM','LU_CODE_2000','SUM_POLY_AREA'])
LU_Mesh_df = DataFrame(LU_Mesh_nparr, columns=['SEQNUM','LU_CODE_2000','SUM_POLY_AREA'])
LU_Mesh_df.columns=['SEQNUM','LU00_CODE','LU00_SQFT']

maxAreabySeq = LU_Mesh_df.sort(['LU00_SQFT'],ascending=False).groupby(['SEQNUM'], as_index=False).nth(0)
maxAreabySeq.columns=['SEQNUM','LU00_CODE_1','LU00_SQFT_1']
SecAreabySeq = LU_Mesh_df.sort(['LU00_SQFT'],ascending=False).groupby(['SEQNUM'], as_index=False).nth(1)
SecAreabySeq.columns=['SEQNUM','LU00_CODE_2','LU00_SQFT_2']
ThrdAreabySeq = LU_Mesh_df.sort(['LU00_SQFT'],ascending=False).groupby(['SEQNUM'], as_index=False).nth(2)
ThrdAreabySeq.columns=['SEQNUM','LU00_CODE_3','LU00_SQFT_3']


Top2AreabySeq = merge(maxAreabySeq, SecAreabySeq, how='left', on=['SEQNUM'])
Top3AreabySeq = merge(Top2AreabySeq, ThrdAreabySeq, how='left', on=['SEQNUM'])

LUcsv = workdir + "predominanteLu00.csv"
Top3AreabySeq.to_csv(LUcsv,index=False)
pdomLU = Myworkspace + "/PredomLU_00"
arcpy.CopyRows_management(LUcsv, pdomLU)


#			Process 2004 Land Use  6 min 19 sec

InterceptFeatures = ModelMesh + " #;" + LU2004 + " #"
arcpy.Intersect_analysis(in_features=InterceptFeatures,out_feature_class=LU04ModelMesh,join_attributes="ALL",cluster_tolerance="#",output_type="INPUT")

# Add Geometry Time : (Elapsed Time: 8 minutes 33 seconds)
arcpy.AddGeometryAttributes_management(Input_Features=LU04ModelMesh,Geometry_Properties="AREA",Length_Unit="FEET_US",Area_Unit="SQUARE_FEET_US",Coordinate_System=sr)
#

#   PAUSE for command to complete.  Add Geometry needs to be ran from the tool.  Double click failed entry in Results window.

# Dissolve Time: (Elapsed Time: 13 minutes 47 seconds)
arcpy.Dissolve_management(in_features=LU04ModelMesh,out_feature_class=maxAreaLU04Mesh,dissolve_field="SEQNUM;LU_CODE_2004",statistics_fields="POLY_AREA SUM",multi_part="MULTI_PART",unsplit_lines="DISSOLVE_LINES")

LU_Mesh = maxAreaLU04Mesh
LU_Mesh_lyr = arcpy.MakeFeatureLayer_management(LU_Mesh, "LU_Mesh_lyr")
LU_Mesh_nparr = arcpy.da.FeatureClassToNumPyArray(LU_Mesh_lyr, ['OBJECTID','SEQNUM','LU_CODE_2004','SUM_POLY_AREA'])
LU_Mesh_df = DataFrame(LU_Mesh_nparr, columns=['SEQNUM','LU_CODE_2004','SUM_POLY_AREA'])
LU_Mesh_df.columns=['SEQNUM','LU04_CODE','LU04_SQFT']

maxAreabySeq = LU_Mesh_df.sort(['LU04_SQFT'],ascending=False).groupby(['SEQNUM'], as_index=False).nth(0)
maxAreabySeq.columns=['SEQNUM','LU04_CODE_1','LU04_SQFT_1']
SecAreabySeq = LU_Mesh_df.sort(['LU04_SQFT'],ascending=False).groupby(['SEQNUM'], as_index=False).nth(1)
SecAreabySeq.columns=['SEQNUM','LU04_CODE_2','LU04_SQFT_2']
ThrdAreabySeq = LU_Mesh_df.sort(['LU04_SQFT'],ascending=False).groupby(['SEQNUM'], as_index=False).nth(2)
ThrdAreabySeq.columns=['SEQNUM','LU04_CODE_3','LU04_SQFT_3']


Top2AreabySeq = merge(maxAreabySeq, SecAreabySeq, how='left', on=['SEQNUM'])
Top3AreabySeq = merge(Top2AreabySeq, ThrdAreabySeq, how='left', on=['SEQNUM'])

LUcsv = workdir + "predominanteLu04.csv"
Top3AreabySeq.to_csv(LUcsv,index=False)
pdomLU = Myworkspace + "/PredomLU_04"
arcpy.CopyRows_management(LUcsv, pdomLU)



#			Process 2010 Land Use  6 min 19 sec

InterceptFeatures = ModelMesh + " #;" + LU2010 + " #"
arcpy.Intersect_analysis(in_features=InterceptFeatures,out_feature_class=LU10ModelMesh,join_attributes="ALL",cluster_tolerance="#",output_type="INPUT")

# Add Geometry Time : (Elapsed Time: 8 minutes 33 seconds)
arcpy.AddGeometryAttributes_management(Input_Features=LU10ModelMesh,Geometry_Properties="AREA",Length_Unit="FEET_US",Area_Unit="SQUARE_FEET_US",Coordinate_System=sr)
#

#   PAUSE for command to complete.  Add Geometry needs to be ran from the tool.  Double click failed entry in Results window.

# Dissolve Time: (Elapsed Time: 13 minutes 11 seconds)
arcpy.Dissolve_management(in_features=LU10ModelMesh,out_feature_class=maxAreaLU04Mesh,dissolve_field="SEQNUM;LU_CODE_2010",statistics_fields="POLY_AREA SUM",multi_part="MULTI_PART",unsplit_lines="DISSOLVE_LINES")

LU_Mesh = maxAreaLU10Mesh
LU_Mesh_lyr = arcpy.MakeFeatureLayer_management(LU_Mesh, "LU_Mesh_lyr")
LU_Mesh_nparr = arcpy.da.FeatureClassToNumPyArray(LU_Mesh_lyr, ['OBJECTID','SEQNUM','LU_CODE_2010','SUM_POLY_AREA'])
LU_Mesh_df = DataFrame(LU_Mesh_nparr, columns=['SEQNUM','LU_CODE_2010','SUM_POLY_AREA'])
LU_Mesh_df.columns=['SEQNUM','LU10_CODE','LU10_SQFT']

maxAreabySeq = LU_Mesh_df.sort(['LU10_SQFT'],ascending=False).groupby(['SEQNUM'], as_index=False).nth(0)
maxAreabySeq.columns=['SEQNUM','LU10_CODE_1','LU10_SQFT_1']
SecAreabySeq = LU_Mesh_df.sort(['LU10_SQFT'],ascending=False).groupby(['SEQNUM'], as_index=False).nth(1)
SecAreabySeq.columns=['SEQNUM','LU10_CODE_2','LU10_SQFT_2']
ThrdAreabySeq = LU_Mesh_df.sort(['LU10_SQFT'],ascending=False).groupby(['SEQNUM'], as_index=False).nth(2)
ThrdAreabySeq.columns=['SEQNUM','LU10_CODE_3','LU10_SQFT_3']


Top2AreabySeq = merge(maxAreabySeq, SecAreabySeq, how='left', on=['SEQNUM'])
Top3AreabySeq = merge(Top2AreabySeq, ThrdAreabySeq, how='left', on=['SEQNUM'])

LUcsv = workdir + "predominanteLu10.csv"
Top3AreabySeq.to_csv(LUcsv,index=False)
pdomLU = Myworkspace + "/PredomLU_10"
arcpy.CopyRows_management(LUcsv, pdomLU)

#			Process 2014 Land Use  6 min 19 sec

InterceptFeatures = ModelMesh + " #;" + LU2014 + " #"
arcpy.Intersect_analysis(in_features=InterceptFeatures,out_feature_class=LU14ModelMesh,join_attributes="ALL",cluster_tolerance="#",output_type="INPUT")

# Add Geometry Time : (Elapsed Time: 8 minutes 33 seconds)
arcpy.AddGeometryAttributes_management(Input_Features=LU14ModelMesh,Geometry_Properties="AREA",Length_Unit="FEET_US",Area_Unit="SQUARE_FEET_US",Coordinate_System=sr)
#

#   PAUSE for command to complete.  Add Geometry needs to be ran from the tool.  Double click failed entry in Results window.

# Dissolve Time: (Elapsed Time: 13 minutes 47 seconds)

#  2012 is being called 2014

arcpy.Dissolve_management(in_features=LU14ModelMesh,out_feature_class=maxAreaLU14Mesh,dissolve_field="SEQNUM;LUCODE_2012",statistics_fields="POLY_AREA SUM",multi_part="MULTI_PART",unsplit_lines="DISSOLVE_LINES")

LU_Mesh = maxAreaLU14Mesh
LU_Mesh_lyr = arcpy.MakeFeatureLayer_management(LU_Mesh, "LU_Mesh_lyr")
LU_Mesh_nparr = arcpy.da.FeatureClassToNumPyArray(LU_Mesh_lyr, ['OBJECTID','SEQNUM','LUCODE_2012','SUM_POLY_AREA'])
LU_Mesh_df = DataFrame(LU_Mesh_nparr, columns=['SEQNUM','LUCODE_2012','SUM_POLY_AREA'])

# Rename to more specific and expected attribute names: LUCODE_2012 to LU12_CODE and SUM_POLY_AREA to LU14_SQFT

LU_Mesh_df.columns=['SEQNUM','LU14_CODE','LU14_SQFT']

maxAreabySeq = LU_Mesh_df.sort(['LU14_SQFT'],ascending=False).groupby(['SEQNUM'], as_index=False).nth(0)
maxAreabySeq.columns=['SEQNUM','LU14_CODE_1','LU14_SQFT_1']
SecAreabySeq = LU_Mesh_df.sort(['LU14_SQFT'],ascending=False).groupby(['SEQNUM'], as_index=False).nth(1)
SecAreabySeq.columns=['SEQNUM','LU14_CODE_2','LU14_SQFT_2']
ThrdAreabySeq = LU_Mesh_df.sort(['LU14_SQFT'],ascending=False).groupby(['SEQNUM'], as_index=False).nth(2)
ThrdAreabySeq.columns=['SEQNUM','LU14_CODE_3','LU14_SQFT_3']


Top2AreabySeq = merge(maxAreabySeq, SecAreabySeq, how='left', on=['SEQNUM'])
Top3AreabySeq = merge(Top2AreabySeq, ThrdAreabySeq, how='left', on=['SEQNUM'])

LUcsv = workdir + "predominanteLu14.csv"
Top3AreabySeq.to_csv(LUcsv,index=False)
pdomLU = Myworkspace + "/PredomLU_14"
arcpy.CopyRows_management(LUcsv, pdomLU)





