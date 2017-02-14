#/usr/bin/env python3

import os
from tempfile import mkdtemp
from shutil import rmtree

def get_temp_dir(work_dir,prefix='temp'):
  '''
  This function returns a temporary directory
  '''
  try:
    temp_dir=mkdtemp(prefix=prefix,dir=work_dir)
    return temp_dir
  except Exception as e:
    print('Error: %s' % e)

def clean_temp_dir(temp_dir): 
  '''
   This function delete a directory and all its contents
  '''
  if os.path.isdir(temp_dir):
    try :
      rmtree(temp_dir)
    except Exception as e:
       print('couldn\'t remove %s' % temp_dir)
    else:
      print('removed %s' % temp_dir)
