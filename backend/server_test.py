from server import app
import pytest


@pytest.fixture # Context for the tests
def fixture():
    with app.test_client() as fixture:
        yield fixture # Execute test


# Upload tests
# Test /upload POST
#
def test_upload_good_input(fixture):
    test_file_name = 'test_file_good.pdf' # Valid file to upload in our test.
    file_binary = open(test_file_name, "rb") # Get binary.
    data = {
        'file': (file_binary, test_file_name)
    }
    response = fixture.post( # Send request to the server and get response
        '/upload',
        content_type="multipart/form-data",
        data=data
    )
    assert response.status_code == 200 # Check status is OK.
    response_json_as_dictionary = response.json
    assert response_json_as_dictionary # Assert condition is true if dictionary is not empty, ie. if JSON is returned.
#
def test_upload_bad_input_wrong_file_extension(fixture):
    test_file_name = 'test_file_bad.txt' # Valid file to upload in our test.
    file_binary = open(test_file_name, "rb") # Get binary.
    data = {
        'file': (file_binary, test_file_name)
    }
    response = fixture.post( # Send request to the server and get response
        '/upload',
        content_type="multipart/form-data",
        data=data
    )
    assert response.status_code == 400 # Check status is 'Bad Request'.
#
def test_upload_bad_input_no_file(fixture):
    data = {
    }
    response = fixture.post( # Send request to the server and get response
        '/upload',
        content_type="multipart/form-data",
        data=data
    )
    assert response.status_code == 400 # Check status is 'Bad Request'.


# Generate test
# Test /generate GET
#
def test_generate(fixture):

    # First upload file:
    # (Re-using code despite DRY principle.)
    test_file_name = 'test_file_good.pdf' # Valid file to upload in our test.
    file_binary = open(test_file_name, "rb") # Get binary.
    data = {
        'file': (file_binary, test_file_name)
    }
    upload_response = fixture.post( # Send request to the server and get response
        '/upload',
        content_type="multipart/form-data",
        data=data
    )

    # The test.
    if upload_response.status_code == 200:
        generate_response = fixture.get('/generate')
        assert generate_response.status_code == 200 # Check status is OK.
        response_json_as_dictionary = generate_response.json
        assert response_json_as_dictionary # Assert condition is true if dictionary is not empty, ie. if JSON is returned.
