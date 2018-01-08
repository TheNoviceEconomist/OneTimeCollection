from Script import ValidateShapefile

text = ValidateShapefile.CheckSHP(r"D:\FCC_GIS_Projects\MFII\DataCollection\PTI Pacifica\New Submission", r"..\logs\sprint")

text.get_shapefile_path_walk()

#print(text.fcList)

text.check_geom()

text.check_fields()

#print(text.field_dic)

headers = sorted([('SEQID', 'SmallInteger'), ('FRN', 'String'), ('HOCO', 'String'), ('SOFT', 'String'),
                      ('DATE', 'Date'), ('SPECTRUM', ['SmallInteger', 'LongInteger', 'String']),
                      ('BANDWIDTH', ['SmallInteger', 'LongInteger', 'String']), ('RSRP', 'SmallInteger')])

text.fields_headers_match(headers)
