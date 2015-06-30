import os

#set cwd
cwd = os.path.dirname(os.path.realpath(__file__))

#set general paths                
paths = {'cwd'                    : cwd,
         'resources'              : os.sep.join([cwd,'resources']),
         'wn_versions'            : ['16','17','171','20','21','30'],
         'dir_offset2offset_bins' : os.path.join(cwd,'resources','bins','offset2offset'),
         'dir_lexkey2offset_bins' : os.path.join(cwd,'resources','bins','lexkey2offset'),
         'dir_offset2lexkey_bins' : os.path.join(cwd,'resources','bins','offset2lexkey'),
         'mappings_upc_2007'      : os.path.join(cwd,'resources','mappings-upc-2007'),
         'index_senses_dir'       : os.path.join(cwd,'resources','wn_index_senses')
         }

