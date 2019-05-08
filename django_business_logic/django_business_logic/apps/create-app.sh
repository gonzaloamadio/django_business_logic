#!/bin/bash


# $1 = nombre app
# $2 = version de api

if [ "$#" -ne 2 ]; then
echo "Usage: ./create_app.sh nombre_app version_api"
echo "Example :   ./create_app.sh company v1"
echo "Example :   ./create_app.sh test v2"
exit
fi

django-admin startapp $1
mkdir $1/api_$2
mkdir $1/tests
mv $1/views.py $1/api_$2/
touch $1/api_$2/serializers.py
touch $1/api_$2/urls.py

rm $1/tests.py
touch $1/tests/doctst.py
touch $1/tests/test_creation.py
touch $1/tests/__init__.py

echo "import doctest" >> $1/tests/__init__.py
echo "__test__ = {" >> $1/tests/__init__.py
echo "    'Doctest': doctest" >> $1/tests/__init__.py
echo "}" >> $1/tests/__init__.py

