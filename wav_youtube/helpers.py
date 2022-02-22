#helper functions
import shutil # For deleting directories that are not empty\
import os
def start_fresh():
    # Delete metadata csv
    if os.path.exists("./metadata.csv"):
        os.remove("./metadata.csv")
    else:
        f = open("metadata.csv", "w")
        f.close()

    shutil.rmtree('./wavs', ignore_errors=True) # Delete if exists


# Get the number of the most recent line in the metadata file so we can append to it for new additions
def get_most_recent_metadata_line():
    metafile = open("metadata.csv", "r")
    last_line = ""
    for item in metafile:
        last_line = item
    if(last_line == ""):
        print("Metadata file empty")
        return last_line
    # When the loop gets here we will have the last line text, inefficient but it works
    # EXMPL-001||Hello World! -> split | -> ['EXMPL-001', 'Hello World!'] -> 'EXMPL-001'.split('-')[1] = 001
    last_line = last_line.split('|')[0].split('-')
    return last_line[1]



def get_total_audio_length():
    pass