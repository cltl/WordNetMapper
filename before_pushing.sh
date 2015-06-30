
echo
echo 
echo
echo "decide if you need to change version in new commit"

#gzipping files if needed
for file in $(find "resources/bins/" -not -name "*.gz");
do
    gzip $file
done


#unit test
bash unit_testing.sh

#epydoc
epydoc --html *.py

