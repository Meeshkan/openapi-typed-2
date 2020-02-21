import yaml
from openapi_typed_2 import convert_from_openapi, convert_to_openapi

def test_stripe_schema():
    with open('test/stripe.yaml', 'r', encoding='utf8') as stripe_yaml:
        stripe = yaml.safe_load(stripe_yaml)
        o = convert_to_openapi(stripe)
        assert convert_from_openapi(o) == stripe
