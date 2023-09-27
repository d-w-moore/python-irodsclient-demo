import irods.session
import irods.test.helpers as helpers

irods_version = tuple(int(_) for _ in irods.__version__.split('.'))

get_home_collection = helpers.home_collection if irods_version > (1,0,0) else \
                      lambda session: '/{ses.zone}/home/{ses.username}'.format(ses = session)

DEFAULTS = dict(host = 'localhost',
                port = 1247,
                user = 'rods',
                password = 'rods',
                zone = 'tempZone')

def get(**auth_options):
    options = DEFAULTS.copy()
    options.update(auth_options)
    ses = irods.session.iRODSSession(**options)
    return [
            ses,                             # session object
            get_home_collection(ses)         # string representing logical path to home collection
           ]
