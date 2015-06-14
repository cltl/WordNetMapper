#import built-in
import os 

#import pickle (use cPickle for python2)
import sys
if sys.version_info.major == 2:
    import cPickle as pickle
else:
    import pickle
    
#import installed or created modules
from config import paths
from config import Offset2OffsetException,BinException,Offset2OffsetException,Lexkey2OffsetException,IliException,Offset2Lexkey

import wn_mapper_utils as utils 

class WordNetMapper():
    '''
    this class provides various methods to map lexkey | offset | ilidef
    to lexkey | offset | ilidef. each method contains a docstring that
    explains the full process.
    
    In terms of efficiency, the main idea behind this setup is that once
    a particular method is called, for example offset_to_offset between
    two wordnet versions, the mapping will stay in memory. Hence, when the
    same method is called for the same wordnet versions, the process will be
    very quick.
    '''
    def __init__(self):
        
        self.current_path_bin      = ""
        self.cur_lexkey_to_offset  = ""
        self.map_offset_to_offset   = {}
        self.cur_offset_to_offset  = ""
        self.map_offset_to_lexkey   = {}
        self.cur_offset_to_lexkey  = ""
        self.map_lexkey_to_offset   = {}
        
    def load_bin_if_needed(self,
                           current_path_bin,
                           new_path_bin,
                           attribute):
        '''
        method checks if the new_path_bin is different from currently in memory.
        if so new_path_bin is load into memory, else nothing is done.
        If the combination of source and target wordnet is not available, 
        BinException is raised.
        
        @type  current_path_bin: str
        @param current_path_bin: full path to bin that is currently in memory
        (with first usage this variable will be an empty string
        
        @type  new_path_bin: str
        @param new_path_bin: full path to new path of the bin which might be
        loaded.
        
        @type  attribute: str
        @param attribute: map_offset_to_offset | map_offset_to_lexkey | map_lexkey_to_offset
        ''' 
        if new_path_bin != self.current_path_bin:
            
            try:
                mapping = pickle.load(open(new_path_bin,"rb"))
            except IOError:
                raise BinException('''there is no dict available for the combination of the given source and target versions''')
            
            self.current_path_bin = new_path_bin
            setattr(self, attribute, mapping)  

    def offset_to_lexkey(self, offset, 
                               lemma,
                               source_wn_version):
        '''
        method tries to return the lexkey of an offset. the following strategy
        is applied:
        (1) map offset to possible sensekeys
        (2) check for direct lemma match in possible sensekeys
        (3) check if only one sensekey
        (4) [TODO]: try something Levenshtein like to find possible sensekey
        Exception Offset2Lexkey is raised if no lexkey is found.
        
        >>> my_mapper = WordNetMapper()
        >>> my_mapper.offset_to_lexkey("05262185","moustache","30")
        'moustache%1:08:00::'
        
        @type  offset: str
        @param offset: 8 character offset with trailing zeros (for example
        02102663)
        
        @type  lemma: str
        @param lemma: the lemma corresponding to the offset (for example '1000')
        
        @type  source_wn_version: str
        @param source_wn_version: source wn_version (for example '21')
        
        @rtype: str
        @return: lexkey if found, else Exception Offset2Lexkey is raised.
        '''
        #load_bin_if_needed
        path_bin = os.path.join(paths['dir_offset2lexkey_bins'],
                                source_wn_version)
        self.load_bin_if_needed(self.cur_offset_to_lexkey, 
                                path_bin, 
                                'map_offset_to_lexkey')
        
        #map offset to possible lexkeys
        list_lexkeys = self.map_offset_to_lexkey[(offset,source_wn_version)]
        
        #check for direct match in possible lexkeys
        for lexkey in list_lexkeys:
            if lexkey.startswith("%s%%" % lemma):
                return lexkey 
            
        #check if only one lexkeys
        #TODO: implement Levenshtein to find lexkey and add as option

        if len(list_lexkeys) == 1:
            return list_lexkeys[0]
        
        raise Offset2Lexkey('''no lexkey found for combination of %s %s in wordnet version %s''' % (offset,lemma,source_wn_version))
                        
    def offset_to_offset(self, 
                         offset, 
                         source_wn_version, 
                         target_wn_version,
                         output_format='highest'):
        '''
        
        >>> my_parser = WordNetMapper()
        >>> my_parser.offset_to_offset("00020846", "21", "30")
        ('00021939', 'n')
        
        method tries to map offset to offset across versions of wordnet
        Offset2OffsetException is raised if no mapping available.
        
        @type  offset: str
        @param offset: 8 character offset with trailing zeros (for example
        00003469)
        
        @type  source_wn_version: str
        @param source_wn_version: source wn_version (for example '2.1')
    
        @type  target_wn_version: str
        @param target_wn_version: source wn_version (for example '3.0')

        @type  output_format: str
        @param output_format: if 'highest': str is returned of (offset,pos)
        with highest confidence. if 'all', a dict is returned mapping the 
        (offset,pos) -> confidence (float)
        
        @rtype: tuple | dict
        @return: if param output_format == 'highest': str is returned of (offset,pos)
        with highest confidence. if param output_format == 'all', a dict is returned mapping the 
        (offset,pos) -> confidence (float). Offset2OffsetException is raised if no mapping available.
        '''
        #load_bin_if_needed
        path_bin = os.path.join(paths['dir_offset2offset_bins'],
                                "%s_%s" % (source_wn_version,
                                           target_wn_version))
        self.load_bin_if_needed(self.cur_offset_to_offset,
                                path_bin,
                                'map_offset_to_offset')
        
        #map offset to offset
        target_offsets = self.map_offset_to_offset[(offset,
                                                    source_wn_version,
                                                    target_wn_version)]
        
        #check if mapping output is not empty, else raise error
        if not target_offsets:
            raise Offset2OffsetException('''no mapping available for offset %s
                                            between wordnet version %s and %s''' % (offset,
                                                                                    source_wn_version,
                                                                                    target_wn_version)) 
        
        elif output_format == "all":
            return target_offsets
        else:
            offset_with_highest_confidence,pos = utils.format_output(target_offsets)
            return (offset_with_highest_confidence,pos)
    
    def offset_to_ilidef(self,  
                         offset, 
                         source_wn_version, 
                         target_wn_version,
                         output_format='highest'):
        '''
        method tries to map offset to ildef across versions of wordnet
        
        >>> my_parser = WordNetMapper()
        >>> my_parser.offset_to_ilidef("00020846", "21", "30")
        'ili-30-00021939-n'

        @type  offset: str
        @param offset: 8 character offset with trailing zeros (for example
        00003469)
        
        @type  source_wn_version: str
        @param source_wn_version: source wn_version (for example '21')
    
        @type  target_wn_version: str
        @param target_wn_version: source wn_version (for example '30')

        @type  output_format: str
        @param output_format: if 'highest': str is returned of ilidef
        with highest confidence. if 'all', a dict is returned mapping the 
        (ilidef,pos) -> confidence (float)
        
        @rtype: str | dict
        @return: if param output_format == 'highest': str is returned of ilidef
        with highest confidence. if param output_format == 'all', a dict is returned mapping the 
        (ildef,pos) -> confidence (float)

        '''
        output = self.offset_to_offset(offset, 
                                       source_wn_version, 
                                       target_wn_version, 
                                       output_format)
        
        if output_format   == "highest": 
            offset_with_highest_confidence,pos = output
            ilidef = "ili-{target_wn_version}-{offset_with_highest_confidence}-{pos}".format(**locals())
            return ilidef
        
        elif output_format == "all":
            ilidef_output = {}
            for (offset,pos),confidence in output.items():
                ilidef = "ili-{target_wn_version}-{offset}-{pos}".format(**locals())
                ilidef_output[(ilidef,pos)] = confidence
            return ilidef_output

    def lexkey_to_lexkey(self,
                         lexkey,
                         source_wn_version,
                         target_wn_version):
        '''
        lexkey is mapped to lexkey. Exception Offset2Lexkey is raised 
        if not found
        
        >>> my_mapper = WordNetMapper()
        >>> my_mapper.lexkey_to_lexkey('rock_hopper%1:05:00::','21','30')
        'rock_hopper%1:05:00::'
        
        @type  lexkey: str
        @param lexkey: wordnet sensekey (for example 'rock_hopper%1:05:00::')

        @type  source_wn_version: str
        @param source_wn_version: source wn_version (for example '21')
    
        @type  target_wn_version: str
        @param target_wn_version: source wn_version (for example '30')
        
        @rtype: str
        @return: lexkey, Exception Offset2Lexkey is raised if not found
        '''
        #obtain lemma
        lemma = lexkey.split("%")[0]
         
        #map lexkey to offset
        source_offset = self.lexkey_to_offset(lexkey, source_wn_version)
        
        #map offset to offset with highest confidence
        target_offset,pos = self.offset_to_offset(source_offset, 
                                                  source_wn_version, 
                                                  target_wn_version)
         
        #map offset to lexkey
        target_lexkey = self.offset_to_lexkey(target_offset, 
                                              lemma, 
                                              target_wn_version)
        
        return target_lexkey
         

    def lexkey_to_offset(self, lexkey, source_wn_version): 
        '''
        method tries to return the offset of a lexkey from a particular wordnet
        version. Lexkey2OffsetException is raised if no mapping is found.
        
        >>> my_mapper = WordNetMapper()
        >>> my_mapper.lexkey_to_offset('rock_hopper%1:05:00::','21')
        '02037384'
        
        @type  lexkey: str
        @param lexkey: wordnet sensekey (for example 'rock_hopper%1:05:00::')
        
        @type  source_wn_version: str
        @param source_wn_version: source wn_version (for example '21')
        
        @rtype: str
        @return: offset of lexkey, Lexkey2OffsetException is raised if not found
        '''
        #load_bin_if_needed
        path_bin = os.path.join(paths['dir_lexkey2offset_bins'],
                                source_wn_version)
        self.load_bin_if_needed(self.cur_lexkey_to_offset, 
                                path_bin, 
                                "map_lexkey_to_offset")
        
        #map lexkey to offset
        offset = self.map_lexkey_to_offset[(lexkey,source_wn_version)]
        
        if not offset:
            raise Lexkey2OffsetException("no offset found for %s in wordnet version %s" % (lexkey,
                                                                                           source_wn_version))
        else:
            return offset
    
    def lexkey_to_ilidef(self,
                         lexkey,
                         source_wn_version,
                         target_wn_version,
                         output_format="highest"):
        '''
        lexkey is mapped to ilidef
        
        
        >>> my_mapper = WordNetMapper()
        >>> my_mapper.lexkey_to_ilidef('rock_hopper%1:05:00::','20','30')
        'ili-30-02057330-n'
        
        @type  lexkey: str
        @param lexkey: wordnet sensekey (for example 'rock_hopper%1:05:00::')

        @type  source_wn_version: str
        @param source_wn_version: source wn_version (for example '21')
    
        @type  target_wn_version: str
        @param target_wn_version: source wn_version (for example '30')
        
        @type  output_format: str
        @param output_format: if 'highest': str is returned of ilidef
        with highest confidence. if 'all', a dict is returned mapping the 
        (ilidef,pos) -> confidence (float)

        @rtype: str | dict
        @return: if param output_format == 'highest': str is returned of ilidef
        with highest confidence. if param output_format == 'all', a dict is returned mapping the 
        (ildef,pos) -> confidence (float)
        '''
        #map lexkey to offset
        source_offset = self.lexkey_to_offset(lexkey, source_wn_version)
        
        #map offset to ilidef
        ilidef = self.offset_to_ilidef(source_offset, 
                                       source_wn_version, 
                                       target_wn_version,
                                       output_format=output_format)
        
        return ilidef 
    
    def ilidef_to_lexkey(self, ilidef, lemma):
        '''
        method tries to map ilidef to lexkey. Exception Offset2Lexkey is 
        raised if not found.
        
        >>> my_mapper = WordNetMapper()
        >>> my_mapper.ilidef_to_lexkey('ili-30-02069355-a','other')
        'other%3:00:00::'
        
        @type  ili: str
        @param ili: ili defintion of wordnet synset (for example ili-30-02069355-a)
        
        @type  lemma: str
        @param lemma: a lemma, for example 'other'
        
        @rtype: str
        @return: lexkey of combination of ilidef and lemma. Exception Offset2Lexkey
        ''' 
        ili,source_wn_version,offset,pos = ilidef.split('-')
        
        lexkey = self.offset_to_lexkey(offset, 
                                       lemma,
                                       source_wn_version)
        
        return lexkey
    
    def ilidef_to_offset(self, ili, 
                               target_wn_version,
                               output_format="highest"):
        '''
        given a certain ili definition (for example ili-30-02069355-a)
        the ilidef is mapped to an offset between wordnet versions.
        IliException is raised if the input format of the ili is not correct
        
        >>> my_mapper = WordNetMapper()
        >>> my_mapper.ilidef_to_offset('ili-30-02069355-a','20')
        ('01999889', 'a')
        
        @type  ili: str
        @param ili: ili defintion of wordnet synset (for example ili-30-02069355-a)
        
        @type  target_wn_version: str
        @param target_wn_version: source wn_version (for example '30')
        
        @type  output_format: tuple | dict
        @param output_format: if 'highest': str is returned of (offset,pos)
        with highest confidence. if 'all', a dict is returned mapping the 
        (offset,pos) -> confidence (float)

        @rtype: tuple | dict
        @return: if param output_format == 'highest': str is returned of (offset,pos)
        with highest confidence. if param output_format == 'all', a dict is returned mapping the 
        (offset,pos) -> confidence (float)
        
        '''
        #split ili
        try:
            ili,source_wn_version,source_offset,pos = ili.split("-")
        except:
            raise IliException("this ili: %s does not have the format ili-source_wn_version-offset-pos")
        
        #map offset2offset
        output = self.offset_to_offset(source_offset, 
                                        source_wn_version, 
                                        target_wn_version,
                                        output_format=output_format)
        
        return output
       
    def ilidef_to_ilidef(self,
                         ili,
                         source_wn_version,
                         target_wn_version,
                         output_format="highest"):
        '''
        given a certain ili def, this method tries to map it to ilidef
        of another wordnet version
        
        >>> my_mapper = WordNetMapper()
        >>> my_mapper.ilidef_to_ilidef('ili-30-02069355-a','30','16')
        'ili-16-01991315-a'
        
        @type  ili: str
        @param ili: ili defintion of wordnet synset (for example ili-30-02069355-a)
        
        @type  source_wn_version: str
        @param source_wn_version: source wn_version (for example '16')
        
        @type  target_wn_version: str
        @param target_wn_version: target wn_version (for example '30')
        
        @type  output_format: tuple | dict
        @param output_format: if 'highest': str is returned of (ili,pos)
        with highest confidence. if 'all', a dict is returned mapping the 
        (ili,pos) -> confidence (float)

        @rtype: str | dict
        @return: if param output_format == 'highest': str is returned of ilidef
        with highest confidence. if param output_format == 'all', a dict is returned mapping the 
        (ildef,pos) -> confidence (float)
        '''
        
        #map ilidef2offset
        target_offsets = self.ilidef_to_offset(ili, 
                                               target_wn_version,
                                               output_format)
        
        #map offset2ilidef
        
        if output_format   == 'all':
            output = {}
            for (offset,pos),confidence in target_offsets.items():
                ili = self.offset_to_ilidef(offset, 
                                            target_wn_version, 
                                            target_wn_version)
                output[(ili,pos)] = confidence
                
        elif output_format == 'highest':
            offset,pos = target_offsets    
            output     = self.offset_to_ilidef(offset, 
                                               target_wn_version, 
                                               target_wn_version, 
                                               output_format)
        
        return output
    
    def overlap(self,source_wn_version,target_wn_version):
        '''
        this method determines the percentage of offset that can be succesfully
        mapped between two wordnet version
        
        >>> my_parser = WordNetMapper()
        >>> succes_rate,missed_mappings = my_parser.overlap("30","171")
        >>> succes_rate
        0.9489831562625135
        
        @type  source_wn_version: str
        @param source_wn_version: source wn_version (for example '21')
        
        @type  target_wn_version: str
        @param target_wn_version: source wn_version (for example '30')
        
        @type: tuple
        @return: (succes_rate,missed_mappings). succes_rate, float between 0 and 1
        indicating the percentage that was succesfully mapped. missed_mappings is 
        a list of offsets that were unable to be mapped
        '''
        result          = 0.0
        missed_mappings = []
        
        bin_path = os.path.join(paths['dir_offset2lexkey_bins'],
                                source_wn_version)
        bin      = pickle.load(open(bin_path,"rb"))
        
        for counter,(offset,version) in enumerate(bin):
    
            try:
                output = self.offset_to_offset(offset,
                                                   source_wn_version,
                                                   target_wn_version)
                result +=1
            except:
                missed_mappings.append(offset)
        
        if 0 in [result,counter]:
            succes_rate = 0.0
        else:
            succes_rate = result/counter
        
        return succes_rate,missed_mappings
        

