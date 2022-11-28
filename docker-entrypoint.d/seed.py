import sqlalchemy
import json
import ckan.config.middleware
from ckan.common import config
from ckan.tests.helpers import CKANTestApp

from ckan.tests import factories

# Minimum config required for basic app
config["testing"] = True
config['__file__'] = '/srv/app/test.ini'
config['SECRET_KEY'] = 'asdf'
config['here'] = config['__file__']
config['who.config_file'] = '/srv/app/who.ini'
config['beaker.session.secret'] = 'asdf'

# Create app
app = ckan.config.middleware.make_app(config)
test_app = CKANTestApp(app)


def get_base_dataset():
    res = test_app.post('/api/action/organization_show', data={'id': 'myorg'})
    org_id = json.loads(res.body)['result']['id']
    # Create datasets
    return {
        'public_access_level': 'public',
        'unique_id': '',
        'contact_name': 'Jhon',
        'program_code': '018:001',
        'publisher': 'Publisher 01',
        'modified': '2019-01-27 11:41:21',
        'tag_string': 'tag01,tag02',
        'owner_org': org_id,
        'extras': [{'key': 'bureauCode', 'value': '010:00'},
                   {'key': 'contact-email', 'value': 'test@email.com'}]
    }


# Without the request context, db operations won't work
with test_app.flask_app.test_request_context():
    try:
        user = factories.Sysadmin(name='asdfs')
        user_name = user['name'].encode('ascii')
        print('User created')
    except sqlalchemy.exc.IntegrityError:
        print('User exists')

    # Create organization
    try:
        organization = factories.Organization(name='myorg')
        print('Org created')
    except sqlalchemy.exc.InvalidRequestError:
        print('Org exists')

    # Create datasets
    for x in range(1, 6):
        try:
            dataset = get_base_dataset()
            dataset['extras'].append({'key': 'unique identifier', 'value': f'id-{x}'})
            dataset.update({'title': f"test 0{x} dataset", 'id': f't{x}'})
            factories.Dataset(**dataset)
            print(f'Dataset {x} created')
        except Exception as er:
            print(f'exception: {er}')
