#!/usr/bin/env python3

import irods_connection

[ses, home] = irods_connection.get()

data_object_name = "newdataobj.txt"
data_object_fullpath = home + "/" + data_object_name

# Create the data object and write content (a bytestring object) into it.

data_object = ses.data_objects.open( data_object_fullpath, "w")
data_object.write( "This is some text to put into the file\n".encode() )
data_object.close()

# Get the collection object and use it to list the contained data object(s).

home_collection = ses.collections.get( home )
for d in home_collection.data_objects:
    print (d)
