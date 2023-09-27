#!/usr/bin/env python3

import irods_connection

from irods.models import DataObject, Collection

from irods.collection import iRODSCollection
from irods.data_object import iRODSDataObject

[ses, home] = irods_connection.get()

data_object_name = "newdataobj.txt"

query_results = list(
        ses.query(DataObject,Collection).filter(DataObject.name == data_object_name)
        )

assert len(query_results) >= 1, 'Must run demo1 first to create data object.'

# Get the first result.
first_result = query_results[0]

# Print out database "columns"
print ('data id', first_result[DataObject.id])            # Print the DataObject (R_DATA_MAIN) table's ID column.
print ('data name', first_result[DataObject.name])        # The data object's name column contains only the base name.
print ('collection name', first_result[Collection.name])  # The collection name column contains its full logical path.

# Extra Credit: Instantiation of objects from iRODS query results
# All of the below information would be displayed by ils -L <data_object_path>

collection =  iRODSCollection(ses.collections, result = first_result)
data_object = iRODSDataObject(ses.data_objects, parent = collection, results = [first_result])

print ("\n" "As extra credit :), we have retrieved these objects using the query:")
print (collection)
print (data_object)
print ("\n" f"The data object has size {data_object.size}.")
print (f"The data object has { len(data_object.replicas) } replicas, listed below:")
for repl in data_object.replicas:
    print ("\t",repl.number,repl)
