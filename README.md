# memcached-k8s-client-test

## Description

This is a test charm that consumes the memcache relation and collect information on the memcached servers available.

## Usage

    juju deploy memcached-k8s
    juju deploy memcached-k8s-client-test 
    juju add-relation memcached-k8s memcached-k8s-client-test

Check in the logs for collected memcached servers endpoints with:

    juju debug-log -i memcached-k8s-client-test/0


## Developing

Create and activate a virtualenv with the development requirements:

    virtualenv -p python3 venv
    source venv/bin/activate
    pip install -r requirements-dev.txt

## Testing

The Python operator framework includes a very nice harness for testing
operator behaviour without full deployment. Just `run_tests`:

    ./run_tests
