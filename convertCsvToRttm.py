import argparse, csv, os, sys

if __name__ == "__main__":
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", default="",
                    help="csv file path")
    args = vars(ap.parse_args())
    file = args['file']
    if not ('.csv' in file):
       print('Did not input a csv file!')
       sys.exit(1)
    else:
        csvFile = open(file, 'r')
        data = csv.reader(csvFile, delimiter=',')
        # csvFile.close()
        fileName, fileExt = os.path.splitext(file)
        fileName = fileName.replace('_data','')
        with open(fileName+'_score.rttm','w') as f:
            for row in data:
                offset = row[0]
                duration = row[1]
                f.write('SPEAKER {} 1 {} {} <NA> <NA> 1 <NA> <NA>\n'.format(fileName, row[0], row[1]))
    
    sys.exit(0)