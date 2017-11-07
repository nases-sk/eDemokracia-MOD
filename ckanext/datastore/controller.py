import StringIO
import unicodecsv as csv
import os

import pylons

import ckan.plugins as p
import ckan.lib.base as base
import ckan.model as model

from ckan.common import request, response

import logging
log = logging.getLogger(__name__)

def _get_filename(resource_id, storage_path):
    directory = os.path.join(storage_path, 'resources', resource_id[0:3], resource_id[3:6])
    filepath = os.path.join(directory, resource_id[6:])
    return filepath

class DatastoreController(base.BaseController):
    def dump(self, resource_id):
        limit = int(pylons.config.get('datastore.dump.limit', 10000))
        context = {
            'model': model,
            'session': model.Session,
            'user': p.toolkit.c.user
        }

        data_dict = {
            'resource_id': resource_id,
            'limit': 1,
            'offset': request.GET.get('offset', 0)
        }
        
        small_resource = False
        action = p.toolkit.get_action('datastore_search')
        try:
            result = action(context, data_dict)
            if result.get('total', 0) <= limit:
                small_resource = True
        except p.toolkit.ObjectNotFound:
            base.abort(404, p.toolkit._('DataStore resource not found'))
        
        request_all = request.GET.get('all', False)
        
        #handle big resources if requested all data
        if request_all and not small_resource:
            #try to provide file instead of generating CSV
            storage_path = pylons.config.get('ckan.storage_path')
            filepath = _get_filename(resource_id, storage_path)
            if os.path.isfile(filepath):
                file_size = os.path.getsize(filepath)
                headers = [('Content-Disposition', 'attachment; filename=\"' + resource_id+'.fs.csv' + '\"'),
                       ('Content-Type', 'text/csv; charset=UTF-8; header=present'),
                       ('Content-Length', str(file_size))]
        
                from paste.fileapp import FileApp
                fapp = FileApp(filepath, headers=headers)
                return fapp(request.environ, self.start_response)
            else:
                base.abort(404, p.toolkit._('Resource consists of more than {0} records. Therefore this resource will be converted to CSV file in order to provided for users. Conversion will be executed within 24 hours from upload. Please try it again later.').format(limit))

        data_dict = {
            'resource_id': resource_id,
            'limit': limit,
            'offset': request.GET.get('offset', 0)
        }
        try:
            result = action(context, data_dict)
        except p.toolkit.ObjectNotFound:
            base.abort(404, p.toolkit._('DataStore resource not found'))

        pylons.response.headers['Content-Type'] = 'text/csv; charset=UTF-8; header=present'
        pylons.response.headers['Content-disposition'] = \
            'attachment; filename="{name}.csv"'.format(name=resource_id)
        f = StringIO.StringIO()
        wr = csv.writer(f, encoding='utf-8')

        header = [x['id'] for x in result['fields']]
        wr.writerow(header)

        for record in result['records']:
            wr.writerow([record[column] for column in header])
        return f.getvalue()
