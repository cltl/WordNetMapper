##WordNetMapper

This repo provides the possibility to map between lexical keys | offsets | ilidefs
from one wordnet version to the other ["16","17","171","20","21","30"].
It makes use of the index.sense files from WordNet (http://wordnet.princeton.edu/)
and the automatically generated mappings between WordNet offsets (http://nlp.lsi.upc.edu/tools/download-map.php)

##USAGE
This library is a python module (should work with both version 2.7 and 3+). 
For python 2.7, the cPickle module has to be installed.
Here are some examples on how to use it:

```shell
python
>>> from WordNetMapper import WordNetMapper
>>> my_mapper = WordNetMapper()
>>> my_parser.offset_to_offset("00020846", "21", "30")
('00021939', 'n')
>>>
>>> my_parser = WordNetMapper()
>>> succes_rate,missed_mappings = my_parser.overlap("30","171")
>>> succes_rate
0.9489831562625135
```

##list of useful methods (do help(WordNetMapper.method) for info on how to use it)
* ilidef_to_ilidef
* ilidef_to_lexkey
* ilidef_to_offset
* lexkey_to_ilidef
* lexkey_to_lexkey
* lexkey_to_offset
* offset_to_ilidef
* offset_to_lexkey
* offset_to_offset
* overlap

##Installation (is not not needed to use it, only included for replicability)
* Clone this repository:
    * cd repository_folder
    * sudo bash install.sh

##Contact
* Marten Postma
* m.c.postma@vu.nl
* http://martenpostma.com/
* Free University of Amsterdam

***

* Ruben Izquierdo Bevia
* ruben.izquierdobevia@vu.nl
* http://rubenizquierdobevia.com/
* Free University of Amsterdam

##TODO:
* Levenshtein for offset to lexkey
* extend unit testing