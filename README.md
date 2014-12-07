pyshadowcopy
============

Python class to create, work with and delete volume shadow copies on Windows

This is a simple python class that uses the pyWin32 extensions to create shadow copies, return the equivalent shadow copy path of a file, and clean up those shadow copies. There is much room for improvement in the way of error checking, correct path matching etc but it does work. For example:

```python
import vss

# Create a set that contains the LOCAL disks you want to shadow
local_drives = set()
set.add('C')

# Initialize the Shadow Copies
sc = vss.ShadowCopy(local_drives)

# An open and locked file we want to read
locked_file = r'C:\foo\bar.txt'
shadow_path = sc.shadow_path(locked_file)

# shadow_path will look similar to:
# u'\\\\?\\GLOBALROOT\\Device\\HarddiskVolumeShadowCopy7\\foo\\bar.txt'

# Open shadow_path just like a regular file
with open(shadow_path, 'rb') as fp:
  data = fp.read()
  
# When done, clean up the shadow copies
sc.delete()
```

Please note, you must have the correct python and pyWin32 libraries installed for the bitness of your OS (32 or 64 bit). Using 32-bit python/pyWin32 on a 64-bit OS won't work.
