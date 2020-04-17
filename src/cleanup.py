
import glob
import os
import time
import shutil as su

def find_matching_files(search_dict):
    file_list=[]
    for search in search_dict:
        file_list += glob.glob(search)
    return file_list   

def clean_matching_files(file_list):
    tally=0
    for f in file_list:
        try:
            os.remove(f)
            tally +=1
        except:
            print("Error cleaning the file", f)
    return tally


def delete_dir(code_dict):

    sl = "/"
    top_dir = str(os.getcwd()) + sl + "build"
    app_dir = ""
    for d in code_dict:
        app_dir = app_dir + sl + d 

    mod_dir = top_dir + sl + "modulefiles" + app_dir
    app_dir = top_dir + app_dir

    if os.path.isdir(app_dir):
        print("Removing appliation installed in "+app_dir+" continuing in 10 seconds...")
        time.sleep(10)
        su.rmtree(app_dir)
        print("Application removed.")

        try:
            su.rmtree(mod_dir)

        except:
            print("Warning, no module file located in "+mod_dir+". Skipping.")

    else:
        print("No application found in "+app_dir)


def clean():
    print("Cleaning up temp files...")
    search_dict = ['*.o*',
                   '*.e*',
                   '*.log'
                  ]

    file_list = find_matching_files(search_dict)

    if file_list:

        print("Found the following files to delete:")
        for f in file_list:
            print(f)

        print("Continuing in 10 seconds...")
        time.sleep(10)
        print("No going back now...")
        deleted = clean_matching_files(file_list)
        print("Done, ", str(deleted), " files successfuly cleaned.")

    else:
        print("No temp files found.")

def remove_app(code_str):
    code_dict=code_str.split("/")
    delete_dir(code_dict)
