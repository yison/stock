import sys
import easyhistory
import gflags
import flags

FLAGS = gflags.FLAGS

def init_history_data(time_type, export, path):
    return easyhistory.init(time_type, export=export, path=path)

def init_day_history(export, path):
    return init_history_data(FLAGS.time_type_day, export=export,
                      path=path)

if __name__=="__main__":
    FLAGS(sys.argv)
#    print (FLAGS.host)
    ## init history data(day)
    print ("init history data:day")
    init_day_history(export=FLAGS.history_export_file_type,
                     path=FLAGS.history_path)
    print ("init history data:day, Done!")
