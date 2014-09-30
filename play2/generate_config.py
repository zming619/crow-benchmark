#!/usr/bin/env python

import collections, json, textwrap

# This script generates the benchmark_config and setup_*.py files.
# To add new tests, modify the `configurations` and `test_urls` tables.

# Each line corresponds to a test application.
# Format is: (language, orm, (os, ...), (test, ...))
# See the dir_name logic below to see the directory name for each test application.
configurations = [
  ('Java',  None,    ['Linux'],            ['json']),
  ('Scala', None,    ['Linux'],            ['json']),
  ('Java',  'Ebean', ['Linux'],            ['db', 'query']),
  ('Scala', 'Anorm', ['Linux', 'Windows'], ['db', 'query', 'fortune', 'update']),
]

# All play2 test applications must use the same URLs.
test_urls = {
  'json': '/json',
  'db': '/db',
  'query': '/queries?queries=',
  'fortune': '/fortunes',
  'update': '/update?queries=',
}

tests_config_json = collections.OrderedDict()

for lang, orm, oses, tests in configurations:
  dir_name = 'play2-' + lang.lower() + (('-'+orm.lower()) if orm else '')
  print 'Generating tests for test application '+dir_name
  setup_name = 'setup_' + lang.lower() + (('_'+orm.lower()) if orm else '')
  for os in oses:
    if len(oses) == 1:
      test_name = lang.lower() + (('-'+orm.lower()) if orm else '')
    else:
      test_name = lang.lower() + (('-'+orm.lower()) if orm else '') + '-'+os.lower()
    test_config_json = collections.OrderedDict([
      ('display_name', 'play2-'+test_name),
      ('setup_file', setup_name),
      ('framework', 'play2'),
      ('language', lang),
      ('orm', orm if orm else 'Raw'),
      ('os', os),
      ('database', 'MySQL' if orm else 'None'),
      ('approach', 'Realistic'),
      ('classification', 'Fullstack'),
      ('platform', 'Netty'),
      ('webserver', 'None'),
      ('database_os', 'Linux'),
      ('notes', ''),
      ('versus', 'netty'),
      ('port', '9000'),
    ])
    for test in tests:
      test_config_json[test+'_url'] = test_urls[test]
      tests_config_json[test_name] = test_config_json
    with open(setup_name+'.py', 'w') as f:
      f.write(textwrap.dedent("""
        # This file was generated by generate_config.py.
        # Do not edit this file directly.
        from .setup_common import make_setup_for_dir

        make_setup_for_dir(globals(), '"""+dir_name+"""')
      """))

with open('benchmark_config', 'w') as f:
  json_str = json.dumps({
    'framework': 'play2',
    'tests': [tests_config_json]
  }, indent=2)
  f.write(json_str)