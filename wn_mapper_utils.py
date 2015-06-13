import operator


def format_output(d):
    '''
    offset with highest confidence is returned. 
    
    @type  d: dict
    @param d: mapping (offset,pos) -> confidence (float)
    
    @rtype: str
    @return: offset with highest confidence
    '''
    (offset,pos),confidence = sorted(d.items(),
                                     key=operator.itemgetter(1),
                                     reverse=True)[0]
    
    return offset,pos

