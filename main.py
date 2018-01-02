from Script import ValidateShapefile

text = ValidateShapefile.CheckSHP(r"D:\FCC_GIS_Projects\MFII\DataCollection\PTI Pacifica\New Submission", "logs")

text.get_shapefile_path_walk()

print(text.fcList)

text.check_geom()

text.check_fields()

print(text.field_dic)
