import os
import os.path
import pytest
from pytest_bdd import given, when, then, parsers
from utils.http import http_curl_request, http_response_attribute
from utils.parser import load_from_file, load_from_text, get_json_path
from utils.redis import new_redis_client, new_redis_client_from_text
from utils.text import replace_text, sanitise_list, sanitise_data


# hooks
def pytest_bdd_before_step_call(request, feature, scenario, step, step_func, step_func_args):
    context = request.getfixturevalue('context')
    if not context:
        return
    data = context.get('data', None)
    if not data:
        return
    for key in step_func_args:
        value = step_func_args[key]
        if type(value) is str:
            if value.count('%') > 1:
                step_func_args[key] = replace_text(data, value)


def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    print('\n-----Step Print Out-----')
    print(step)
    print('\n-----Step_func Print Out-----')
    print(step_func)
    print('\n-----Step_func_Args Print Out-----')
    print(step_func_args)
    print('\n-----Exception Print Out-----')
    print(exception)


# fixtures
@pytest.fixture(scope='session', autouse=True)
def environment_config():
    try:
        env = os.environ.get('ENV')
        if not env:
            env = os.environ.get('env')
        env = env.lower().strip() if env else ''
        root = os.path.dirname(__file__)
        target_config = os.path.join(root, '..', 'config', f'{env}_config.yaml')
        default_config = os.path.join(root, '..', 'config', 'default_config.yaml')
        if env and os.path.exists(target_config):
            return load_from_file('yaml', target_config)
        elif os.path.exists(default_config):
            return load_from_file('yaml', default_config)
        pytest.exit('fail to load environment config')
    except Exception as e:
        pytest.exit(e)


@pytest.fixture(scope='function', autouse=True)
def context(environment_config):
    try:
        if environment_config:
            return {'data': environment_config}
        return {}
    except Exception as e:
        raise e


# steps
@given(parsers.parse("redis client is init from environment config"))
def redis_client_is_init_from_environment_config(context):
    context['redis'] = next(new_redis_client(context['data']['redis']))


@given(parsers.parse("redis client is init from the following {parse_type} config:\n{text}"))
def redis_client_is_init_from_the_following_parse_type_config(context, parse_type, text):
    context['redis'] = next(new_redis_client_from_text(text, parse_type.lower()))


@given(parsers.parse("data is set from the following {parse_type} config:\n{text}"))
def data_is_set_from_the_following_parse_type_config(context, parse_type, text):
    try:
        data_dct = load_from_text(parse_type, text)
        context['data'] = {**context['data'], **data_dct} if context.get('data', None) else data_dct
    except Exception as e:
        raise e


@when(parsers.parse("the following http curl response is saved as {response_name}:\n{text}"))
def the_following_http_curl_response_is_save_as_response_name(context, response_name, text):
    res = http_curl_request(text)
    if not res.content:
        raise ValueError(f'response not returned from curl:{text}')
    context[response_name] = res


@when(parsers.parse("I delete redis keys {keys}"))
def i_delete_redis_keys(context, keys):
    redis = context.get('redis', None)
    if not redis:
        raise ValueError(f'redis not found in context')
    try:
        keys = keys.split(",")
        redis.delete(*keys)
    except Exception as e:
        raise e


@then(parsers.parse("the redis key {key} should {assert_existence}"))
def the_redis_key_should_assert_existence(context, key, assert_existence):
    redis = context.get('redis', None)
    if not redis:
        raise ValueError(f'redis not found in context')
    if assert_existence == "exist":
        assert redis.get(key) is not None
    else:
        assert redis.get(key) is None


@then(parsers.parse("the {attribute} for {response} should be {expected_value}"))
def the_attribute_for_response_should_be_expected_value(context, attribute, response, expected_value):
    res = context.get(response, None)
    if not res.content:
        raise ValueError(f'response:{response} not found in context')
    assert_statement = http_response_attribute(res, attribute, expected_value)
    if assert_statement is None:
        raise ValueError(f'attribute:{attribute} not found in response:{response}')
    assert assert_statement


@then(parsers.parse("the JSONPath {jsonpath} value for {response} should match {expected}"))
def the_jsonpath_value_for_response_should_match_expected(context, jsonpath, response, expected):
    res = context.get(response, None)
    if not res.content:
        raise ValueError(f'response:{response} not found in context')

    def compare(act, exp):
        if str(exp)[:1] in ['<', '>', '=']:
            return eval(str(act) + str(exp))
        else:
            return act == exp

    try:
        actual = get_json_path(jsonpath, res.json())
        data = sanitise_data(expected, output_type='raw')
        if len(actual) > 0:
            for i, expected_value in enumerate(data):
                assert compare(actual[i], expected_value)
        else:
            assert compare(actual, data)

    except Exception as e:
        raise e


@then(parsers.parse("the jsonpath {jsonpath} value for {response} {decision} contain {expected}"))
def the_jsonpath_value_for_response_should_not_contain_expected(context, jsonpath, response, decision, expected):
    res = context.get(response, None)
    if not res.content:
        raise ValueError(f'response:{response} not found in context')
    try:
        actual = get_json_path(jsonpath, res.json())
        data = sanitise_list(expected)
        if len(actual) > 0:
            if 'not' in decision.lower():
                assert data not in actual
            else:
                assert data in actual
        else:
            raise Exception("Empty data")
    except Exception as e:
        raise e


@then(parsers.parse("the jsonpath {jsonpath} value for {response} {decision} be empty"))
def the_jsonpath_value_for_response_should_not_be_empty(context, jsonpath, response, decision):
    res = context.get(response, None)
    if not res:
        raise ValueError(f'response:{response} not found in context')
    try:
        actual = get_json_path(jsonpath, res.json())
        if 'not' in decision.lower():
            assert actual
        else:
            assert not actual

    except Exception as e:
        raise e
