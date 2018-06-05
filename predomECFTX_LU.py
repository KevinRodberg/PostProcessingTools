
import arcpy
import sys
import numpy
from pandas import *

sr = arcpy.SpatialReference(2881)

workdir = r"//ad.sfwmd.gov/dfsroot/data/wsd/GIS/GISP_2012/DistrictAreaProj/CFWI/Data/ProcessDir/"
Myworkspace = workdir + "PredomECFTX_LU.gdb"

ModelMesh =  r"\\ad.sfwmd.gov\dfsroot\data\wsd\GIS\GISP_2012\DistrictAreaProj\CFWI\Data\From_SW_SJ\ECFTX_GRID_V3.shp"

LandUse =r"\\ad.sfwmd.gov\DFSroot\data\wsd\GIS\GISP_2012\DistrictAreaProj\ECFTX\ECFTX_LU.gdb/StplnEast/"
Lu95_merge = LandUse + "Lu95_merge"
Lu99_merge = LandUse + "Lu99_merge"
Lu04_merge = LandUse + "Lu04_merge"
Lu09_merge = LandUse + "Lu09_merge"


LU95ModelMesh = Myworkspace + "/LU95ModelMesh"
LU99ModelMesh = Myworkspace + "/LU99ModelMesh"
LU04ModelMesh = Myworkspace + "/LU04ModelMesh"
LU09ModelMesh = Myworkspace + "/LU09ModelMesh"
LU2009ModelMesh = Myworkspace + "/LU2009ModelMesh"


maxAreaLU95Mesh = Myworkspace + "/maxAreaLU95Mesh"
maxAreaLU99Mesh = Myworkspace + "/maxAreaLU99Mesh"
maxAreaLU04Mesh = Myworkspace + "/maxAreaLU04Mesh"
maxAreaLU09Mesh = Myworkspace + "/maxAreaLU09Mesh"


#			Process 1995 Land Use

InterceptFeatures = ModelMesh + " #;" + Lu95_merge + " #"
arcpy.Intersect_analysis(in_features=InterceptFeatures,out_feature_class=LU95ModelMesh,join_attributes="ALL",cluster_tolerance="#",output_type="INPUT")

# Add Geometry Time : (Elapsed Time: 26 minutes 44 seconds)
arcpy.AddGeometryAttributes_management(Input_Features=LU95ModelMesh,Geometry_Properties="AREA",Length_Unit="FEET_US",Area_Unit="SQUARE_FEET_US",Coordinate_System=sr)
# Dissolve Time: (Elapsed Time: 28 minutes 32 seconds)
arcpy.Dissolve_management(in_features=LU95ModelMesh,out_feature_class=maxAreaLU95Mesh,dissolve_field="SEQNUM;LU_CODE",statistics_fields="POLY_AREA SUM",multi_part="MULTI_PART",unsplit_lines="DISSOLVE_LINES")

LU_Mesh = maxAreaLU95Mesh
LU_Mesh_lyr = arcpy.MakeFeatureLayer_management(LU_Mesh, "LU_Mesh_lyr")
LU_Mesh_nparr = arcpy.da.FeatureClassToNumPyArray(LU_Mesh_lyr, ['OBJECTID','SEQNUM','LU_CODE','SUM_POLY_AREA'])
LU_Mesh_df = DataFrame(LU_Mesh_nparr, columns=['SEQNUM','LU_CODE','SUM_POLY_AREA'])
LU_Mesh_df.columns=['SEQNUM','LU95_CODE','LU95_SQFT']
maxAreabySeq = LU_Mesh_df.sort(['LU95_SQFT'],ascending=False).groupby(['SEQNUM'], as_index=False).nth(0)
LUcsv = workdir + "predominanteLu95.csv"
maxAreabySeq.to_csv(LUcsv,index=False)
pdomLU = Myworkspace + "/PredomLU_95"
arcpy.CopyRows_management(LUcsv, pdomLU)

arcpy.MakeFeatureLayer_management (ModelMesh, "memMM")
# Join Field Time: Elapsed Time: 6 hours 4 minutes 31 seconds
arcpy.JoinField_management ("memMM", "SEQNUM", pdomLU, "SEQNUM")

#			Process 1999 Land Use

InterceptFeatures = ModelMesh + " #;" + Lu99_merge + " #"
# Intersect Analysis Time: (Estimated Time: 15 minutes)
arcpy.Intersect_analysis(in_features=InterceptFeatures,out_feature_class=LU99ModelMesh,join_attributes="ALL",cluster_tolerance="#",output_type="INPUT")

# Add Geometry Time : (Estimated Time: 30 minutes )
arcpy.AddGeometryAttributes_management(Input_Features=LU99ModelMesh,Geometry_Properties="AREA",Length_Unit="FEET_US",Area_Unit="SQUARE_FEET_US",Coordinate_System=sr)
# Dissolve Time: (Estimated Time: 30 minutes)
arcpy.Dissolve_management(in_features=LU99ModelMesh,out_feature_class=maxAreaLU99Mesh,dissolve_field="SEQNUM;LU_CODE",statistics_fields="POLY_AREA SUM",multi_part="MULTI_PART",unsplit_lines="DISSOLVE_LINES")

LU99_Mesh = maxAreaLU99Mesh
LU99_Mesh_lyr = arcpy.MakeFeatureLayer_management(LU99_Mesh, "LU99_Mesh_lyr")
LU99_Mesh_nparr = arcpy.da.FeatureClassToNumPyArray(LU99_Mesh_lyr, ['OBJECTID','SEQNUM','LU_CODE','SUM_POLY_AREA'])
LU99_Mesh_df = DataFrame(LU99_Mesh_nparr, columns=['SEQNUM','LU_CODE','SUM_POLY_AREA'])
LU99_Mesh_df.columns=['SEQNUM','LU99_CODE','LU99_SQFT']
maxAreabySeq = LU99_Mesh_df.sort(['LU99_SQFT'],ascending=False).groupby(['SEQNUM'], as_index=False).first()
LUcsv = workdir + "predominanteLu99.csv"
maxAreabySeq.to_csv(LUcsv,index=False)
pdomLU99 = Myworkspace + "/PredomLU_99"
arcpy.CopyRows_management(LUcsv, pdomLU99)

arcpy.MakeFeatureLayer_management (ModelMesh, "memMM99")
# Join Field Time: (Estimated Time: 6 hours)
arcpy.JoinField_management ("memMM99", "SEQNUM", pdomLU99, "SEQNUM")

#			Process 2004 Land Use

InterceptFeatures = ModelMesh + " #;" + Lu04_merge + " #"
# Intersect Analysis Time: (Estimated Time: 15 minutes)
arcpy.Intersect_analysis(in_features=InterceptFeatures,out_feature_class=LU04ModelMesh,join_attributes="ALL",cluster_tolerance="#",output_type="INPUT")

# Add Geometry Time : (Estimated Time: 30 minutes )
arcpy.AddGeometryAttributes_management(Input_Features=LU04ModelMesh,Geometry_Properties="AREA",Length_Unit="FEET_US",Area_Unit="SQUARE_FEET_US",Coordinate_System=sr)
# Dissolve Time: (Estimated Time: 30 minutes )
arcpy.Dissolve_management(in_features=LU04ModelMesh,out_feature_class=maxAreaLU04Mesh,dissolve_field="SEQNUM;LU_CODE",statistics_fields="POLY_AREA SUM",multi_part="MULTI_PART",unsplit_lines="DISSOLVE_LINES")

LU04_Mesh = maxAreaLU04Mesh
LU04_Mesh_lyr = arcpy.MakeFeatureLayer_management(LU04_Mesh, "LU04_Mesh_lyr")
LU04_Mesh_nparr = arcpy.da.FeatureClassToNumPyArray(LU04_Mesh_lyr, ['OBJECTID','SEQNUM','LU_CODE','SUM_POLY_AREA'])
LU04_Mesh_df = DataFrame(LU04_Mesh_nparr, columns=['SEQNUM','LU_CODE','SUM_POLY_AREA'])
LU04_Mesh_df.columns=['SEQNUM','LU04_CODE','LU04_SQFT']
maxAreabySeq = LU04_Mesh_df.sort(['LU04_SQFT'],ascending=False).groupby(['SEQNUM'], as_index=False).first()
LUcsv = workdir + "predominanteLu04.csv"
maxAreabySeq.to_csv(LUcsv,index=False)
pdomLU04 = Myworkspace + "/PredomLU_04"
arcpy.CopyRows_management(LUcsv, pdomLU04)

arcpy.MakeFeatureLayer_management (ModelMesh, "memMM04")
# Join Field Time: Elapsed Time: (Estimated Time: 6 hours)
arcpy.JoinField_management ("tempMM", "SEQNUM", pdomLU04, "SEQNUM")

#			Process 2009 Land Use

InterceptFeatures = ModelMesh + " #;" + Lu09_merge + " #"(Estimated Time: 15 minutes)(Elapsed Time: 15 minutes 37 seconds)
arcpy.Intersect_analysis(in_features=InterceptFeatures,out_feature_class=LU2009ModelMesh,join_attributes="ALL",cluster_tolerance="#",output_type="INPUT")

# Add Geometry Time : (Estimated Time: 30 minutes )
arcpy.AddGeometryAttributes_management(Input_Features=LU2009ModelMesh,Geometry_Properties="AREA",Length_Unit="FEET_US",Area_Unit="SQUARE_FEET_US",Coordinate_System=sr)
# Dissolve Time: (Estimated Time: 30 minutes )
arcpy.Dissolve_management(in_features=LU2009ModelMesh,out_feature_class=maxAreaLU09Mesh,dissolve_field="SEQNUM;LU_CODE",statistics_fields="POLY_AREA SUM",multi_part="MULTI_PART",unsplit_lines="DISSOLVE_LINES")

LU09_Mesh = maxAreaLU09Mesh
LU09_Mesh_lyr = arcpy.MakeFeatureLayer_management(LU09_Mesh, "LU09_Mesh_lyr")
LU09_Mesh_nparr = arcpy.da.FeatureClassToNumPyArray(LU09_Mesh_lyr, ['OBJECTID','SEQNUM','LU_CODE','SUM_POLY_AREA'])
LU09_Mesh_df = DataFrame(LU09_Mesh_nparr, columns=['SEQNUM','LU_CODE','SUM_POLY_AREA'])
LU09_Mesh_df.columns=['SEQNUM','LU09_CODE','LU09_SQFT']
#maxAreabySeq = LU09_Mesh_df.sort(['LU09_SQFT'],ascending=False).groupby(['SEQNUM']).first()
maxAreabySeq = LU09_Mesh_df.sort(['LU09_SQFT'],ascending=False).groupby(['SEQNUM'], as_index=False).nth(0)
SecAreabySeq = LU09_Mesh_df.sort(['LU09_SQFT'],ascending=False).groupby(['SEQNUM'], as_index=False).nth(1)
ThrdAreabySeq = LU09_Mesh_df.sort(['LU09_SQFT'],ascending=False).groupby(['SEQNUM'], as_index=False).nth(2)

#  example to reset indexes
#calls.groupby('agent').count().sort('call_number', ascending=False).reset_index()

Top2AreabySeq = concat([maxAreabySeq, SecAreabySeq], axis =1, join_axes=[maxAreabySeq.index])
Top3AreabySeq = concat([Top2AreabySeq, ThrdAreabySeq], axis =1, join_axes=[Top2AreabySeq.index])

LUcsv = workdir + "predominanteLu09.csv"
maxAreabySeq.to_csv(LUcsv,index=False)
Top3AreabySeq.to_csv(LUcsv,index=False)

pdomLU09 = Myworkspace + "/PredomLU_09"
arcpy.CopyRows_management(LUcsv, pdomLU09)

arcpy.MakeFeatureLayer_management (ModelMesh, "memMM09")
# Join Field Time: Elapsed Time: (Estimated Time: 6 hours)
arcpy.JoinField_management ("tmpMM", "SEQNUM", pdomLU09, "SEQNUM")