

cwd=${PWD#*}

function obtain_index_sense () {

echo
echo "extracting index.sense for wordnet version $2"
wget $1
rm -rf tmp && mkdir tmp
tar -xf $(basename $1) -C $cwd/tmp
mv -f $(find tmp/ -name "index.sense") $cwd/resources/wn_index_senses/$2  
rm $(basename $1)
echo "sorry, but I need sudo right to delete some downloaded wordnet files"
rm -rf tmp
}

function mappings () {

echo
echo "downloading wordnet mappings"
wget http://nlp.lsi.upc.edu/tools/download-map.php
mv download-map.php $cwd/resources/mappings.tar.gz
cd $cwd/resources
tar -zxvf mappings.tar.gz
rm mappings.tar.gz
cd $cwd
}


#(1) create folders if needed
rm -rf resources
mkdir -p resources/wn_index_senses
mkdir -p resources/bins/lexkey2offset
mkdir -p resources/bins/offset2offset
mkdir -p resources/bins/offset2lexkey

#(2) download upc mappings
mappings

#(3) download wn index.sense files

#1.6
obtain_index_sense "http://wordnetcode.princeton.edu/1.6/wn16.unix.tar.gz" 16

#1.7
obtain_index_sense "http://wordnetcode.princeton.edu/1.7/wn17.unix.tar.gz" 17

#1.7.1
obtain_index_sense "http://wordnetcode.princeton.edu/1.7.1/WordNet-1.7.1.tar.gz" 171

#2.0
obtain_index_sense "http://wordnetcode.princeton.edu/2.0/WordNet-2.0.tar.gz" 20

#2.1
obtain_index_sense "http://wordnetcode.princeton.edu/2.1/WordNet-2.1.tar.gz" 21

#3.0
obtain_index_sense "http://wordnetcode.princeton.edu/3.0/WordNet-3.0.tar.gz" 30

#create bins
python2 create_bins.py run

#rm mappings and index file
rm -rf resources/wn_index_senses
rm -rf resources/mappings-upc-2007
