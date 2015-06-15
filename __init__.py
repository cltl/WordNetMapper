import os
import sys 

cwd                          = os.path.dirname(os.path.realpath(__file__))
sys.path.append(cwd)
    
from wordnet_mapper import WordNetMapper

#documentation attributes
WordNetMapper.README         = open(os.path.join(cwd,"README.md")).read()
WordNetMapper.LICENSE        = open(os.path.join(cwd,"LICENSE.md")).read()
WordNetMapper.__author__     = ["Marten Postma","Ruben Izquierdo"]
WordNetMapper.__license__    = "Apache"
WordNetMapper.__version__    = "1.0.1"
WordNetMapper.__maintainer__ = "Marten Postma"
WordNetMapper.__email__      = "martenp@gmail.com"
WordNetMapper.__status__     = "development"

