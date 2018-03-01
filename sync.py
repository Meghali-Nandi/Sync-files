import os
import sys
import re
import shutil
import time

class Sync():
    # all path names to be used as absolute
    # we have to keep one directory as primary folder1 is assumed to be primary
    # becuase otherwise deletion will not be possible since you can not know which folder had the content
    # unless we look for folders marked for deletion by system
    def __init__(self , folder1 , folder2 , create=False):
        self.folder1 = self.__normalize_path(folder1)
        self.folder2 = self.__normalize_path(folder2)
        
        if not os.path.exists(self.folder1):
            raise ValueError("log: Given source path doesn't exists !!!")
        
        if not os.path.exists(self.folder2):
            if create:
                try:
                    os.mkdir(self.folder2)
                except OSError as e:
                    print("log: cannot create target folder " , e)
            else:
                raise ValueError("log: Target directory to sync does not exists")
        
        self.folder1_name = os.path.basename(folder1)
        self.folder2_name = os.path.basename(folder2)
        
        
        
    def __normalize_path(self , path):
        return os.path.abspath(os.sep.join(re.split(r'\\|/', path)))
    
    def __create_folders(self,root,list_of_dir):
        try:
            for entry in list_of_dir:
                print("Creating directory ",entry ," at ",root)
                os.mkdir(os.path.join(root , entry))
                
        except OSError as e:
            print("log: Error in creating directory : " ,e )
            
    def __copy_files(self , folder1_root ,folder2_root , list_of_files):
        try:
            for entry in list_of_files:
                src = os.path.join(folder1_root,entry)
                dst = os.path.join(folder2_root,entry)
                print("Copying file ",entry ," to ", folder2_root)
                shutil.copyfile(src,dst)
        except IOError as e:
            print("log: failed to copy file : ", e)
                
    def __del_files(self ,folder2_root , list_of_files ):
        try:
            for entry in list_of_files:
                os.remove(os.path.join(folder2_root , entry))
                print("Removing from ",folder2_root ," file " ,entry )
        except OSError as e:
                print("log: failed to delete file: ",e)
    
    def __del_dir(self , folder2_root , list_of_dir):
        try:
            for entry in list_of_dir:
                src = os.path.join(folder2_root , entry)
                shutil.rmtree(src)
                print("Removing entire directory ",src)
        except OSError as e:
                print("log: failed to delte entire directory + files ",e )
    
    def start_sync(self, interval):
        while True:
            self.query_content()
            time.sleep(interval)
    
    def __check_folder1(self):
        if not (os.path.exists(folder1)):
            raise  RuntimeError("log: Someone or something just deleted the source folder")
            
    def query_content(self):
        if not (os.path.exists(folder2)):
            print("log: Someone or something just deleted the target folder")
            os.mkdir(self.folder2)
        self.__check_folder1()
        
        for folder1_root, folder1_subdirs , folder1_files in os.walk(self.folder1):
            print("log: Running sync press Ctrl-c to terminate")
#            print("\nroot: ",folder1_root ,"\nsubdir: " , folder1_subdirs ,"\nfiles: ", folder1_files , "\n")
            # root of the current folder
            
            self.__check_folder1() # sanity check
            folder2_root = "".join([self.folder2,folder1_root.split(self.folder1_name)[1]])
            
            folder2_subdirs=[]
            folder2_files=[]
            
            if(os.path.exists(folder2_root)):
                for entry in os.listdir(folder2_root):
                    entry_abs = os.path.join(folder2_root,entry)
                    if(os.path.isdir(entry_abs)):
                        folder2_subdirs.append(entry)
                    else:
                        folder2_files.append(entry)
            
#                print("folder2_root: " , folder2_root , "\nfolder 2 subdir: " , folder2_subdirs , "\nfolder2 files: " , folder2_files)
            
                ## extracted the directory list at current root for folder2 now syncing both the roots
                
                folder2_subdirs = set(folder2_subdirs)
                folder2_files   = set(folder2_files)
                
                ## director to create from folder1 to folder2
                
                copy_dir_list= set(folder1_subdirs) - folder2_subdirs
                self.__create_folders(folder2_root,copy_dir_list)
                
                ## files to create from folder 1 to folder 2
                
                copy_file_list= set(folder1_files) - folder2_files
                self.__check_folder1() # sanity check
                self.__copy_files(folder1_root,folder2_root,copy_file_list)
                
                ## file to be deleted in folder 2 because they dont exists in folder1
                
                marked_files_for_del =  folder2_files - set(folder1_files)
                self.__del_files(folder2_root , marked_files_for_del)
                
                ## directory to be deleted in folder2 because 
                
                marked_dir_for_del = folder2_subdirs - set(folder1_subdirs)
                self.__del_dir(folder2_root, marked_dir_for_del)
                
                ## list of files for updating
                self.__check_folder1() # sanity check
                files = set(folder1_files) - copy_file_list
                
                list_of_updated_files = []
                
                for entry in files :
                    src = os.path.join(folder1_root , entry)
                    dst = os.path.join(folder2_root , entry)
                    
                    srctime = os.path.getmtime(src)
                    dsttime  = os.path.getmtime(dst)  
                    
                    if (srctime - dsttime) > 0 :
                        list_of_updated_files.append(entry)
                self.__copy_files(folder1_root , folder2_root , list_of_updated_files)
                
            else:
                print("log :",folder2_root," path does not exists")
            
        
if __name__ == '__main__':
    folder1 = sys.argv[1]
    folder2 = sys.argv[2]
    new     = False
    if(len(sys.argv) == 4):
        if sys.argv[3] == "True" or sys.argv[3] == "t":
            new = True
    try:
        sync = Sync(folder1 , folder2  , new)
        sync.start_sync(2)
    except ValueError as e:
        print(e)
    