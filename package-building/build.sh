#/bin/bash


cp -r ../diwork_ways .
cp -r ../diwork_mains .
cp ../diwork.py ./diwork

chmod ug+x diwork

find . -name "__pycache__" -type d -exec rm -rf {} \;

tar -cvaf diwork.tar.gz diwork ./diwork_ways ./diwork_mains

rm -f ./diwork
rm -rf ./diwork_ways
rm -rf ./diwork_mains
