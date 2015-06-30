##WordNetMapper

This repo provides the possibility to map between lexical keys | offsets | ilidefs
from one wordnet version to the other ["16","17","171","20","21","30"].
It makes use of the index.sense files from WordNet (http://wordnet.princeton.edu/).
WordNet is redistributed in this repo (see WORDNET_LICENSE.md) for the license agreement.
and the automatically generated mappings between WordNet offsets (http://nlp.lsi.upc.edu/tools/download-map.php)

##USAGE
This library is a python module (should work with both version 2.7 and 3+). 
For python 2.7, the cPickle module has to be installed.
Epydoc was used to document the code (http://epydoc.sourceforge.net/).
The documentation can be found [here](http://htmlpreview.github.io/?https://github.com/MartenPostma/WordNetMapper/blob/master/html/WordNetMapper.wordnet_mapper.WordNetMapper-class.html).
After cloning this repo, the documentation can also be found at html/WordNetMapper.wordnet_mapper.WordNetMapper-class.html.
Here are some examples on how to use it (all methods return ValueError if no mapping is found):

```shell
python
>>> from WordNetMapper import WordNetMapper #the first time this command is executed, the resources folder will be untarred.
>>> my_mapper = WordNetMapper()
>>> my_mapper.offset_to_offset("00020846", "21", "30")
('00021939', 'n')
>>>
>>> succes_rate,missed_mappings = my_mapper.overlap("30","171")
>>> succes_rate
0.9489831562625135
>>> WordNetMapper.__license__
'Apache'
```

##list of useful methods (do help(WordNetMapper.method) for info on how to use it)
* map_ilidef_to_ilidef
* map_ilidef_to_lexkey
* map_ilidef_to_offset
* map_lexkey_to_ilidef
* map_lexkey_to_lexkey
* map_lexkey_to_offset
* map_offset_to_ilidef
* map_offset_to_lexkey
* map_offset_to_offset
* overlap

##Installation (is not needed to use it, only included for replicability)
* Clone this repository:
    * cd repository_folder
    * sudo bash install.sh

##Contact
For bugs and other things related to this repo, please contact:
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
* extend unit testing with output_format == "all" examples + catching errors
