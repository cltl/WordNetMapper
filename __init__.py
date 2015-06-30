import os
import sys 
import subprocess 

cwd                          = os.path.dirname(os.path.realpath(__file__))
sys.path.append(cwd)
    
from wordnet_mapper import WordNetMapper
from config import paths

#documentation attributes
WordNetMapper.README         = open(os.path.join(cwd,"README.md")).read()
WordNetMapper.LICENSE        = open(os.path.join(cwd,"LICENSE.md")).read()
WordNetMapper.__author__     = ["Marten Postma","Ruben Izquierdo"]
WordNetMapper.__license__    = "Apache"
WordNetMapper.__version__    = "1.0.2"
WordNetMapper.__maintainer__ = "Marten Postma"
WordNetMapper.__email__      = "martenp@gmail.com"
WordNetMapper.__status__     = "development"

if os.path.exists(paths['resources']) == False:
    path_tar = os.sep.join([paths['cwd'],'resources.tar.gz'])
    cwd      = paths['cwd']

    command = "tar -zxvf {path_tar} -C {cwd}".format(**locals())
    subprocess.check_output(command,shell=True)