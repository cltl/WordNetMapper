#import built-in modules
import os 
import sys
from collections import defaultdict
from glob import glob 
import subprocess

#import pickle (use cPickle for python2)
import sys
if sys.version_info.major == 2:
    import cPickle as pickle
else:
    import pickle

#import external modules (created or installed)
import bins_utils
from config import paths

#extract general variables
cwd                    = paths['cwd']
wn_versions            = paths['wn_versions']

dir_offset2offset_bins = paths['dir_offset2offset_bins']
dir_lexkey2offset_bins = paths['dir_lexkey2offset_bins']
dir_offset2lexkey_bins = paths['dir_offset2lexkey_bins']

mappings_upc_2007      = paths['mappings_upc_2007']
index_senses_dir       = paths['index_senses_dir']

def save_pickle(mapping,output_path_mapping):
    '''
    the mapping is saved, then gzipped
    
    @type  mapping: collections.defaultdict
    @param mapping: a mapping
    
    @type output_path_mapping: str
    @param output_path_mapping: output path where mapping should be stored
    '''
    #dump defaultdict
    pickle.dump(mapping,open(output_path_mapping,'wb'))
    
    #gzip it
    command = "gzip {output_path_mapping}".format(**locals())
    subprocess.call(command,shell=True)
    
    
def create_offset2offset():
    '''
    '''
    for source_wn_version in wn_versions:
        for target_wn_version in wn_versions:
            
            #set output path for mapping offset2offset
            bin_path   = os.path.join(dir_offset2offset_bins,
                                      "%s_%s" % (source_wn_version,
                                                target_wn_version))
            
            #create path source dir with mappings offset 2 offsets
            if source_wn_version == target_wn_version:
                
                if target_wn_version == "30":
                    source_dir = os.path.join(mappings_upc_2007,
                                          'mapping-%s-%s' % (source_wn_version,
                                                             '20'))
                else:
                    source_dir = os.path.join(mappings_upc_2007,
                                          'mapping-%s-%s' % (source_wn_version,
                                                             '30'))
                    
            else:
                source_dir = os.path.join(mappings_upc_2007,
                                          'mapping-%s-%s' % (source_wn_version,
                                                             target_wn_version))
                
            
            #loop
            offset2offset = defaultdict(dict)
            for map_file in glob(source_dir+"/*"):
                
                pos     = bins_utils.get_pos(map_file)
                mapping = bins_utils.mapping_offset2offset(map_file,
                                                           source_wn_version,
                                                           target_wn_version, 
                                                           pos)
                
                offset2offset.update(mapping)
            
            #dump defaultdict
            save_pickle(offset2offset, bin_path)

def create_lexkey2offset():
    '''
    '''
    for source_wn_version in wn_versions:
        
        index_sense_file = os.path.join(index_senses_dir,source_wn_version)
        bin_path         = os.path.join(dir_lexkey2offset_bins,
                                        source_wn_version)
        mapping          = bins_utils.mapping_lexkey2offset(index_sense_file,
                                                            source_wn_version)
        
        #dump mapping 
        save_pickle(mapping,bin_path)
    
def create_offset2lexkey():
    '''
    '''
    for source_wn_version in wn_versions:
        
        index_sense_file = os.path.join(index_senses_dir,source_wn_version)
        bin_path         = os.path.join(dir_offset2lexkey_bins,
                                        source_wn_version)
        mapping          = bins_utils.mapping_offset2lexkey(index_sense_file,
                                                            source_wn_version)
        
        #dump mapping 
        save_pickle(mapping,bin_path)    

if len(sys.argv) == 2:    
    #create offset2offset
    create_offset2offset()                   
                    
    #create lexkey2offset bins
    create_lexkey2offset()

    #create offset2lexkey bins
    create_offset2lexkey()