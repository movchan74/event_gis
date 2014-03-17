#!/bin/bash

export CFLAGS="-O3 -s"
export CXXFLAGS="-O3 -s"
export OPT="-O3 -s"
export PATH=$OPENSHIFT_DATA_DIR/bin:$PATH

cd $OPENSHIFT_TMP_DIR

wget http://python.org/ftp/python/2.7.4/Python-2.7.4.tar.bz2
tar jxf Python-2.7.4.tar.bz2
cd Python-2.7.4

./configure --prefix=$OPENSHIFT_DATA_DIR
make
make install

$OPENSHIFT_DATA_DIR/bin/python -V

cd $OPENSHIFT_TMP_DIR
rm -rf ./Python-2.7.4*

wget http://pypi.python.org/packages/source/s/setuptools/setuptools-0.6c11.tar.gz
tar zxf setuptools-0.6c11.tar.gz
cd setuptools-0.6c11
$OPENSHIFT_DATA_DIR/bin/python setup.py install

cd $OPENSHIFT_TMP_DIR
rm -rf ./setuptools-0.6c11*

wget http://pypi.python.org/packages/source/p/pip/pip-1.3.1.tar.gz
tar zxf pip-1.3.1.tar.gz
cd pip-1.3.1
$OPENSHIFT_DATA_DIR/bin/python setup.py install

cd $OPENSHIFT_TMP_DIR
rm -rf ./pip-1.3.1*

$OPENSHIFT_DATA_DIR/bin/pip install uwsgi
$OPENSHIFT_DATA_DIR/bin/uwsgi --version

cd $OPENSHIFT_TMP_DIR
wget http://download.osgeo.org/proj/proj-4.8.0.tar.gz
tar xzf proj-4.8.0.tar.gz
cd proj-4.8.0
./configure --prefix=$OPENSHIFT_DATA_DIR
make
make install
cd ..
rm -rf ./proj-4.8.0*


cd $OPENSHIFT_TMP_DIR
wget http://download.osgeo.org/geos/geos-3.3.8.tar.bz2
tar xjf geos-3.3.8.tar.bz2
cd geos-3.3.8
./configure --prefix=$OPENSHIFT_DATA_DIR
make
make install
cd ..
rm -rf ./geos-3.3.8*


cd $OPENSHIFT_TMP_DIR
wget ftp://ftp.remotesensing.org/gdal/gdal-1.9.2.tar.gz
tar zxf gdal-1.9.2.tar.gz
cd gdal-1.9.2
./configure --prefix=$OPENSHIFT_DATA_DIR --disable-static --with-geos=$OPENSHIFT_DATA_DIR/bin/geos-config
make
make install
cd ..
rm -rf ./gdal-1.9.2*




createdb -E UTF8 template_postgis
createlang plpgsql template_postgis
psql -d template_postgis -f /usr/share/pgsql/contrib/postgis-64.sql
psql -d template_postgis -f /usr/share/pgsql/contrib/spatial_ref_sys.sql
createuser -dSLR gis_group

echo "Creating new user (gis_user) for the project..."
createuser -dlSRE -P gis_user

psql postgres -c "GRANT gis_group TO gis_user;"
createdb -O gis_group -T template_postgis -E UTF8 project_db
psql project_db -c "ALTER TABLE geometry_columns OWNER TO gis_group;"
psql project_db -c "ALTER TABLE spatial_ref_sys OWNER TO gis_group;"


echo "Activating hooks"
cp -f $OPENSHIFT_REPO_DIR/.openshift/.template_hooks/* $OPENSHIFT_REPO_DIR/.openshift/action_hooks 
