#/bin/bash

export tmpdir_name="./diwork-main"

mkdir $tmpdir_name

chmod ug+x diwork

cp -r ../diwork_mains $tmpdir_name
cp -r ../diwork_ways $tmpdir_name
cp ../diwork.py $tmpdir_name

find . -name "__pycache__" -exec rm -rf {} \;

tar -cvaf diwork.tar.gz diwork ./diwork-main

rm -rf $tmpdir_name