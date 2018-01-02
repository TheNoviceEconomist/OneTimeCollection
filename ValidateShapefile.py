import os
import arcpy
import sys
import traceback
import logging
import time

class CheckSHP:

    def __init__(self, inpath_Folder, report_outpath=None):
        self.inpath_Folder = inpath_Folder
        self.outpath = report_outpath
        self.fcList = []
        self.field_dic = {}

        # create formatter
        formatter = ('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh = logging.basicConfig(filename=r"{}_Log_{}.csv".format(__name__, time.strftime("%Y_%m_%d_%H_%M")),
                                 level=logging.DEBUG, format=formatter)

    def __repr__(self):
        return "{}".format(self.field_dic)

    def get_shapefile_path_walk(self):


        # use os.walk to find the root, directory, and files
        for root, dirs, files in os.walk(self.inpath_Folder):
            # create a loop by files
            for file in files:
                # for the files that endswith .shp, join the root and file
                if file.endswith(".shp"):
                    # create a local variable that we can assign the root and file path then loop it
                    path = os.path.join(root, file)
                    # append the path in our file_loc list
                    self.fcList.append(path)





    def check_geom(self):

            print("\nChecking geometry for {} many shapefiles".format(len(self.fcList)))
            for fc in self.fcList:
                try:
                    print("\n\tChecking Geometry for fips: {}".format(os.path.basename(fc.strip(".shp"))))
                    logging.info("\n\nxxxxxxxxxxxxxxxxxxxxxxxx Geometry check for fips: {} xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n".format(os.path.basename(fc.strip(".shp"))))

                    if self.outpath is None:

                        out_table = r"logs\Geometry_Error_report_{}".format(os.path.basename(fc.strip(".shp")))
                        arcpy.CheckGeometry_management(fc, out_table)
                        logging.info(arcpy.GetMessages(0))

                    else:
                        out_table = os.path.join(self.outpath, "Geometry_Error_report_{}.csv".format(os.path.basename(fc.strip(".shp"))))
                        arcpy.CheckGeometry_management(fc, out_table)
                        logging.info(arcpy.GetMessages(0))

                except arcpy.ExecuteError:
                    msgs = arcpy.GetMessages(2)
                    arcpy.AddError(msgs)
                    print(msgs)
                    logging.error(msgs)

                except:
                    tb = sys.exc_info()[2]
                    tbinfo = traceback.format_tb(tb)[0]
                    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(
                        sys.exc_info()[1])
                    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
                    arcpy.AddError(pymsg)
                    arcpy.AddError(msgs)
                    print(pymsg)
                    print(msgs)
                    logging.info(pymsg)
                    logging.info(msgs)





    def check_fields(self):

        for fc in self.fcList:
            dic_key = os.path.basename(fc)
            print(dic_key)
            field_list = arcpy.ListFields(fc)
            field_name = [f.name for f in field_list]
            field_type = [f.type for f in field_list]
            self.field_dic[dic_key]={'fields': list(zip(field_name, field_type))}

            print(self.field_dic[dic_key]["fields"][2:])

            masterList = [('SEQID', 'SmallInteger'),
                          ('FRN', 'String'),
                          ('HOCO', 'String'),
                          ('SOFT', 'String'),
                          ('DATE', 'String'),
                          ('SPECTRUM', [ 'SmallInteger', 'LongInteger', 'String' ]),
                          ('BANDWIDTH', 'SmallInteger'),
                          ('RSRP', 'SmallInteger')]

            bad_file = False

            fdict = dict(self.field_dic[dic_key]["fields"])

            for fname, ftype in masterList:
                if fname not in fdict.keys():
                    bad_file = True
                elif (isinstance(fdict[fname], list) and ftype not in fdict[fname]) or ftype != fdict[fname]:
                    bad_file = True
                else:
                    bad_file = False





            if masterList in self.field_dic[dic_key]["fields"][2:]:
                print("true")
            else:
                print("not true")

