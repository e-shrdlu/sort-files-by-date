import os
import time
import shutil
import sys

seperating_char='/'

def sort_files_by_month(copyFromDir, copyToDir, valid_file_types=('.jpg','.jpeg','.png','.avi','.mov','.thm')):
    if len(sys.argv) > 1:
        copyFromDir = sys.argv[1]
    print('Searcing for photos in: ', copyFromDir, '  and copy any found to: ', copyToDir)
    numCopied = 0
    numDuplicates = 0
    for subdir,dirs,files in os.walk(copyFromDir):
        for file in files:
            if any(file.lower().endswith(x) for x in valid_file_types):  # checks if file ends with any of the values in the list
                fn = subdir + seperating_char + file
                dateCreated = os.stat(fn).st_birthtime
                newDir = time.strftime(copyToDir + '/%Y' + seperating_char + '%m %B', time.localtime(dateCreated))
                newFn = newDir + seperating_char + file
                os.makedirs(newDir, exist_ok=True)
                dupeCount = 1
                while True:
                    if not os.path.isfile(newFn):  # False if file exists already
                        shutil.copy2(fn, newFn)
                        print('COPIED  {oldLocation}  to  {newLocation}'.format(oldLocation=fn, newLocation=newFn))
                        numCopied += 1
                        break
                    elif os.path.getsize(fn) == os.path.getsize(newFn):  # size of files is equal so files are assumed to be the same
                        print('DUPLICATE  {oldLocation}  to  {newLocation}'.format(oldLocation=fn, newLocation=newFn))
                        numDuplicates += 1
                        break
                    else:  # file is dupe. add num to end
                        newFn = newDir + seperating_char + ('-' + str(dupeCount) + '.').join(file.split('.'))
                        dupeCount += 1
                        continue
        print('Copied: ', numCopied, '  Duplicates found: ', numDuplicates)

if __name__ == '__main__':
    sort_files_by_month(copyFromDir='/imports/', copyToDir='/photo-archive/', valid_file_types=('.jpg','.jpeg','.png','.avi','.mov','.thm','.tiff'))
