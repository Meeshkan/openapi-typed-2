import yaml
from openapi_typed_2.openapi import Parameter
from openapi_typed_2.converters import convert_from_openapi, convert_to_openapi

def test_slack_schema():
    with open('test/slack.yaml', 'r', encoding='utf8') as slack_yaml:
        slack = yaml.safe_load(slack_yaml)
        o = convert_to_openapi(slack)
        assert convert_from_openapi(o) == slack
