##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
import argparse, os
from time import time
from scipy.io import savemat

from .fnc.extractFeature import extractFeature

# from .fnc.check_eye import check_eye
# #------------------------------------------------------------------------------
# #	Argument parsing
# #------------------------------------------------------------------------------
# parser = argparse.ArgumentParser()

# parser.add_argument("--file", type=str,
#                     help="Path to the file that you want to verify.")

# parser.add_argument("--temp_dir", type=str, default="../Saved",
# 					help="Path to the directory containing templates.")

# parser.add_argument("--id", type=int,
# 					help="Id of a user")

# args = parser.parse_args()


# ##-----------------------------------------------------------------------------
# ##  Execution
# ##-----------------------------------------------------------------------------
# start = time()
# # args.file = "../CASIA1/1/001_1_1.jpg"

# # Extract feature
# print('>>> Enroll for the file ', args.file)
# template, mask, file = extractFeature(args.file)

# # Save extracted feature
# basename = os.path.basename(file)
# out_folder = os.path.join(args.temp_dir, str(args.id))
# # out_file = os.path.join(args.temp_dir, str(args.id), "{}.mat".format(basename))

# if os.path.exists(out_folder):
#     if os.path.isdir(out_folder):
#         print('Каталог найден')
#         print('Список объектов в нем: ',os.listdir(out_folder))
# else:
#     print ('Объект не найден')
#     try:
#         os.mkdir(out_folder)
#     except OSError:
#         print ("Creation of the directory %s failed" % out_folder)
#     else:
#         print ("Successfully created the directory %s " % out_folder)


# out_file = os.path.join(out_folder, "{}.mat".format(basename))

# savemat(out_file, mdict={'template':template, 'mask':mask})
# print('>>> Template is saved in %s' % (out_file))

# end = time()
# print('>>> Enrollment time: {} [s]\n'.format(end-start))


def enroll_single(file_path):
    print(file_path)
    # if check_eye(file_path):
    folder = os.path.dirname(file_path)
    print('\tFolder: ', folder)
    print('\tFile name: ', file_path)
    template, mask, file = extractFeature(file_path)
    print('\tFile: ', file)
    basename = os.path.basename(file)
    print('\tBase name: ', basename)
    out_file = os.path.join(folder, "{}.mat".format(basename))
    print('\tOut file: ', out_file)
    savemat(out_file, mdict={'template':template, 'mask':mask})
    # else:
    #     print('FALSE')