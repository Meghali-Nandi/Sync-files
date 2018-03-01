# Sync-files
A simple python class to Sync two folders in a system. should be extensible to network if modified aptly

The class that can be imported is called Sync
Usage  

```
# folder1 location of the folder in absolute or relative format
# folder2 location of the folder2 in absolute of relative format
# new is True or False whether target folder2 should be created if it does not exists
sync = Sync(folder1 , folder2  , new)
sync.start_sync(interval = 2)

```
As a simple daemon service in backrground  
type this in terminal.
```
python sync.py ./folder1 ../folder3 t

```
t if you need the target directory to get created. 
