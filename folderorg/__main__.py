import argparse
import os
import re
import shutil

def main():
    parser = argparse.ArgumentParser(description="Folder Org")
    parser.add_argument('--path', metavar='Subreddit', type=str, help='The absolute path to the directory')
    args = parser.parse_args()

    id_to_paths = dict()
    id_to_dirname = dict()

    print("Scanning files")

    try:
        if os.path.isabs(args.path):
            #Collects path names and ids and stores in dict
            for dirName, subdirList, fileList in os.walk(args.path):
                matchID = re.search('\[[0-9]+\]$',str(dirName))
                subdirname = str(dirName)[str(dirName).rfind('\\')+1:]
                if matchID:
                    dirID = matchID.group(0)
                    if dirID not in id_to_paths:
                        id_to_paths[dirID] = [str(dirName)]
                        id_to_dirname[dirID] = subdirname
                    else:
                        id_to_paths[dirID].append(str(dirName))

        print("Copying files to organized directory")

        dirCount = 0
        fileCount = 0

        #Create a new directory and copy files from old to new
        newPath = args.path + "_org"
        os.mkdir(newPath)
        for dirID in id_to_dirname.keys():
            dest = newPath+"\\"+id_to_dirname[dirID]
            os.mkdir(newPath+"\\"+id_to_dirname[dirID])
            for directory in id_to_paths[dirID]:
                print("Copying directory", dirCount)
                dirCount += 1
                for f in os.listdir(directory):
                    fileCount +=1
                    shutil.copy(directory + "\\" + f, dest)

        print("Copied {} files and {} directories to {}".format(fileCount, dirCount, newPath))
        
    except AttributeError:
        parser.print_help()



if __name__ == "__main__":
    main()