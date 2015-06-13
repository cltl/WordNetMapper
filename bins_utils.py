from collections import defaultdict
import os 

def mapping_offset2offset(map_file,
                          source_wn_version,
                          target_wn_version, 
                          pos):
                          
    '''
    this method create a defaultdict mappping 
    (source_offset,source_wn_version,target_wn_version)    ->
        'confidence' ->    (target_offset,pos)
    
    @type  map_file: str
    @param map_file: full path to file mapping offsets of one wn version to
    another. example of lines in file:
    00035448 00042340 1 
    00035605 00044164 0.333 01849351 0.333 01854163 0.333 

    @type  source_wn_version: str
    @param source_wn_version: source wn_version (for example '2.1')
    
    @type  target_wn_version: str
    @param target_wn_version: source wn_version (for example '3.0')
    
    @type  pos: str
    @param pos: part of speech (n,v,a,r)
    
    @rtype:  collections.defaultdict
    @return: (source_offset,source_wn_verison,target_wn_version)    ->
        (target_offset,pos) -> confidence (float)

    '''
    #set mapping
    mapping = defaultdict(dict)
    
    #loop through file
    with open(map_file) as infile:
        for line in infile:
            split         = line.strip().split()
            source_offset = split[0]
            
            for index_target_offset in range(1,len(split),2):
                
                #obtain indices
                index_target_offset_conf = index_target_offset+1
                
                if source_wn_version == target_wn_version:
                    target_offset      = source_offset
                    target_offset_conf = 1.0
                else:
                    target_offset            = split[index_target_offset]
                    target_offset_conf       = split[index_target_offset_conf]
                
                #set keys and values
                main_key = (source_offset,source_wn_version,target_wn_version)
                subkey   = (target_offset,pos)
                subvalue = float(target_offset_conf)
                
                #update mapping
                mapping[main_key][subkey] = subvalue
    
    #return output
    return mapping

def mapping_offset2lexkey(index_sense_file,
                          source_wn_version):
                          
    '''
    method create a dict mapping:
    (offset,source_wn_version) -> list of possible sensekeys
    
    @type  index_sense_file: str
    @param index_sense_file: full path to wordnet index.sense file 
    
    @type  source_wn_version: str
    @param source_wn_version: source wn_version (for example '2.1')
    
    @rtype: collections.defaultdict
    @return: mapping (offset,source_wn_version) -> list of possible sensekeyss
    '''
    #set mapping
    mapping = defaultdict(list)
    
    #loop through index.sense file
    with open(index_sense_file) as infile:
        for line in infile:
            
            #get lexkey and offset
            split    = line.strip().split()
            lexkey   = split[0]
            offset   = split[1]
            
            #update mapping
            mapping[(offset,source_wn_version)].append(lexkey)

    #return output
    return mapping

def mapping_lexkey2offset(index_sense_file,
                          source_wn_version):
                          
    '''
    method create a dict mapping:
    (lexkey,source_wn_version) ->    offset
    
    @type  index_sense_file: str
    @param index_sense_file: full path to wordnet index.sense file 
    
    @type  source_wn_version: str
    @param source_wn_version: source wn_version (for example '2.1')
    
    @rtype:  collections.defaultdict
    @return: (lexkey,source_wn_version) -> offset
    '''
    #set mapping
    mapping = defaultdict()
    
    #loop through index.sense file
    with open(index_sense_file) as infile:
        for line in infile:
            
            #get lexkey and offset
            split    = line.strip().split()
            lexkey   = split[0]
            offset   = split[1]
            
            #update mapping
            mapping[(lexkey,source_wn_version)] = offset

    #return output
    return mapping


def get_pos(full_path):
    '''
    given a full path that ends with         adj | adv | noun | verb
    the pos is returned following the tagset a   , r,    n ,    v
    
    @rtype: str
    @return: n | v | r | a
    '''
    for ending,pos in [('adj','a',),('adv','r'),('noun','n'),('verb','v')]:
        if full_path.endswith(ending):
            return pos
    else:
        print('pos not found')
        return ""