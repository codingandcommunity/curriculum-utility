import os
import sys

dir = sys.argv[1] #'C:/Users/Ritvik Vaish/Projects' # Add directory here

def parseFile(fp):
    ofile = open("parsed_output.txt", "w+")
    line = fp.readline() # commit id
    while True:
        line = fp.readline()
        if line.split()[0] != "Author:":
            print("done") # some weird behavior here
            break
        author = ' '.join(line.split()[1:])
        line = fp.readline()
        time = ' '.join(line.split()[1:4])

        line = fp.readline() # blank line

        message = fp.readline() # commit message

        line = fp.readline() # blank line

        # start chunk
        line = fp.readline()
        if line.split()[0] == "diff":
            fname = line.split()[-1] # file being modified
        else:
            continue # no diffs present

        # index, file legends don't seem useful
        line = fp.readline()
        line = fp.readline()
        line = fp.readline()

        # begin chunks of edits
        while line:
            line = fp.readline()
            markers = line.split()
            if markers[0] == "@@":
                if markers[1][1] == '-':
                    removed = [markers[1].split(',')[0][1:], markers[1].split(',')[1]]
                    added = [markers[2].split(',')[0][1:], markers[2].split(',')[1]]
                else:
                    removed = ""
                    added = [markers[1].split(',')[0][1:], markers[1].split(',')[1]]
                
                line = fp.readline()
                edits = ""
                while line.strip():
                    edits = edits + line + "\n"
                    line = fp.readline()
                
                ofile.write(time + ": " + author + " modified " + fname + ":\n")
                ofile.write(message + "\n")
                if removed == "":
                    ofile.write("Added " + added[1] + " lines, starting from line " + added[0] + "\n\n")
                else:
                    ofile.write("Removed " + removed[1] + "lines, starting from line " + removed[0] + "\n")
                    ofile.write("Added " + added[1] + " lines, starting from line " + added[0] + "\n\n")
                ofile.write("Changes:\n" + "========\n" + edits)

            else:
                break
    
    ofile.close()

for file in os.listdir(dir):
    if file.endswith(".txt"):
        try:
            with open(os.path.join(dir, file), "r") as logFile:
                parseFile(logFile)
        
        except:
            print("No more files")