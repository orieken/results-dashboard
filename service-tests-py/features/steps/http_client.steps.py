from behave import given, when, then
import json

from lib.http_client import HTTPClient


@given('I have a url "{url}"')
def step_impl(context, url):
    context.url = url
    context.client = HTTPClient()


@given(u'I have Headers')
def step_impl(context):
    new_headers = {}
    for row in context.table:
        print(row['key'], row['value'])
        new_headers[row['key']] = row['value']

    context.client.set_headers(new_headers)


@given(u'I POST a payload of "{payload}"')
def step_impl(context, payload):
    context.payload = payload
    print('payload', context.payload)
    context.response = context.client.post(context.url, payload)
    print(context.response.status_code, context.response.json())


@then('I should get a "{status_code:d}" status code')
def step_impl(context, status_code):
    assert context.response.status_code == status_code, f"Expected {status_code}, got {context.response.status_code}"


@then('the response body should be "{body}"')
def step_impl(context, body):
    assert context.response.json() == json.loads(body), f"Expected {body}, got {context.response.json()}"

