import os
import time
import shutil


wordMonthToNum = {'January':'01', "February":'02', "March":'03', 'April':'04', 'May':'05', 'June':'06', 'July':'07',
                  'August':'08', 'September':'09', 'October':'10', 'November':'11', 'December':'12'}


def sort_files_by_month(seperating_char='\\', valid_file_types=('.jpg','.jpeg','.png','.avi','.mov')):
    for subdir,dirs,files in os.walk('.'):
        for file in files:
            if any(file.endswith(x) for x in valid_file_types):  # checks if file ends with any of the values in the list
                fn = subdir + seperating_char + file
                dateCreated = str(time.ctime(os.path.getctime(fn))).split()
                # 0day, 1month, 2numday, 3time(24:60:60), 4yr
                newDir = wordMonthToNum[dateCreated[1]] + ' ' + dateCreated[1] + ' ' + dateCreated[4]
                newFn = newDir + seperating_char + file
                os.makedirs(newDir, exist_ok=True)
                dupeCount = 1
                while True:
                    if not os.path.isfile(newFn):  # False if file exists already
                        shutil.copy2(fn, newFn)
                        break
                    elif os.path.getsize(fn) == os.path.getsize(newFn):  # size of files is equal so files are assumed to be the same
                        break
                    else:  # file is dupe. add num to end
                        newFn = newDir + seperating_char + (str(dupeCount) + '.').join(file.split('.'))
                        dupeCount += 1
                        continue
                print('moved {oldLocation} to {newLocation}'.format(oldLocation=fn, newLocation=newFn))


if __name__ == '__main__':
    sort_files_by_month(seperating_char='\\', valid_file_types=('.jpg','.jpeg','.png','.avi','.mov'))
