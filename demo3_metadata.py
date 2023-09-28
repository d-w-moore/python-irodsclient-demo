#!/usr/bin/env python3

import irods_connection

from irods.models import Collection, DataObject, DataObjectMeta
from irods.column import Like

[ses, home] = irods_connection.get()

#
# This is a big one. We'll do the following:
#
# 1. use the get() method within the  data_objects and collections "managers" of the session object (ses) to 
#    procure a reference to those specific catalog objects.  Note that iRODS catalog objects include resources,
#    users, data objects, collections, metadata tuples, and more.  For the most part, any catalog object can
#    have 0 or more attached metadata tuples to make them more searchable, ie discoverable.
# 2. Attach metadata tuple, or AVU (= attribute/value/units) to a data object.
# 3. Query the metadata AVU we've just attached, and get info about the data object in question.
# 4. change the metadata AVU to have a different value.
#
home_collection = ses.collections.get(home)

NAME = "newdataobj.txt"

# Another way to get a reference to an existing data object.  Here, we could have done an
# iRODS query again but instead we use the Pythonic "list comprehension", don't ask why :)

data_objects_in_home = [ _ for _ in home_collection.data_objects
                                   if _.name == NAME ]
d = data_objects_in_home[0]

# If there's no metadata, then attach some:

if len(d.metadata) == 0:
    d.metadata.add( "some key", "some value", "some units")

# Create a subcollection under our Home Collection and copy the original data object into it.
# We'll notice that the metadata doesn't get copied with it. (Ie. only one data object of the
# two shows up in the query below.)

SUBCOLLECTION_FULL_PATH = home_collection.path + "/subcollection"
if not ses.collections.exists(SUBCOLLECTION_FULL_PATH):
    home_sub_collection = ses.collections.create( SUBCOLLECTION_FULL_PATH)
    ses.data_objects.copy(d.path, home_sub_collection.path)

# Now query the metadata and the data object to which it is attached.  We'll also query Collection information
# to be able to get at the object's full path.

import pprint
result = ses.query( DataObject.name, Collection.name, DataObjectMeta).filter(Like(DataObjectMeta.name,"%key%")).one()

print(f"""Retrieved the data object "joined" to an AVU of:
      name =  {result[DataObjectMeta.name]}
      value = {result[DataObjectMeta.value]}
      units = {result[DataObjectMeta.units]}
      """)

# Change the original AVU to have a different <value> field

d = ses.data_objects.get(f"{result[Collection.name]}"
                         "/"
                         f"{result[DataObject.name]}")

# Retrieve the AVU. In this case, we know there will be exactly one.
avu = d.metadata.items() [0]
avu.value = "some OTHER value"
d.metadata.set(avu)

# At this point, if we have icommands, then we can type this at the command prompt to see the results:
#   iquest "select COLL_NAME, DATA_NAME, META_DATA_ATTR_NAME, META_DATA_ATTR_VALUE, META_DATA_ATTR_UNITS where META_DATA_ATTR_NAME like '%key%'"

# Or... just rerun this script to see the changed AVU.
