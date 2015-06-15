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

def levenshtein(s, t):
    ''' 
    source: https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
    
    >>> levenshtein('house', 'home')
    2
    
    @type  s: str
    @param s: a string (for example 'house')
    
    @type  t: str
    @param t: a string (for example ('home')
    
    @rtype: int
    @param: levenshtein distance
    '''
    
    if s == t: 
        return 0
    
    elif len(s) == 0: 
        return len(t)
    elif len(t) == 0: 
        return len(s)
    
    v0 = [None] * (len(t) + 1)
    v1 = [None] * (len(t) + 1)
    
    for i in range(len(v0)):
        v0[i] = i
    
    for i in range(len(s)):
        v1[0] = i + 1
        for j in range(len(t)):
            cost = 0 if s[i] == t[j] else 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
        for j in range(len(v0)):
            v0[j] = v1[j]
 
    return v1[len(t)]