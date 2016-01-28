
echo
echo 
echo
echo "decide if you need to change version in new commit"

#unit test
bash unit_testing.sh

#epydoc
epydoc --html *.py
