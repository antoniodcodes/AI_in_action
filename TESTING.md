# Testing Documentation

This document describes the testing strategy and how to run tests for the Flask weather application.

## 🧪 Test Structure

The application includes comprehensive unit tests and integration tests covering all routes and edge cases.

### Test Files

- `tests.py` - Main test suite with unittest framework
- `run_tests.py` - Test runner script with command-line options
- `requirements-test.txt` - Additional testing dependencies

## 🚀 Running Tests

### Option 1: Using the test runner script

```bash
# Run all tests with default verbosity
python run_tests.py

# Run tests with verbose output
python run_tests.py -v

# Run tests with quiet output
python run_tests.py -q
```

### Option 2: Using unittest directly

```bash
# Run all tests
python -m unittest tests.py -v

# Run specific test class
python -m unittest tests.FlaskAppTestCase -v

# Run specific test method
python -m unittest tests.FlaskAppTestCase.test_index_route -v
```

### Option 3: Using pytest (if installed)

```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run tests with pytest
pytest tests.py -v

# Run with coverage
pytest tests.py --cov=app --cov-report=html
```

## 📋 Test Coverage

### FlaskAppTestCase

#### Route Tests

- **`test_index_route()`** - Tests the root endpoint (`/`)

  - Verifies 200 status code
  - Checks HTML content type
  - Validates "Hello World" content

- **`test_health_route()`** - Tests the health check endpoint (`/health`)

  - Verifies 200 status code
  - Checks JSON content type
  - Validates response structure with "status": "healthy"

- **`test_weather_route_success()`** - Tests weather endpoint with valid coordinates
  - Mocks external API response
  - Verifies 200 status code
  - Checks JSON content type
  - Validates response structure
  - Confirms API call parameters

#### Error Handling Tests

- **`test_weather_route_missing_parameters()`** - Tests missing coordinate parameters
- **`test_weather_route_api_error()`** - Tests external API failures
- **`test_weather_route_invalid_json()`** - Tests invalid JSON responses
- **`test_weather_route_invalid_coordinates()`** - Tests out-of-range coordinates

#### Edge Cases

- **`test_nonexistent_route()`** - Tests 404 for unknown routes
- **`test_weather_route_different_coordinates()`** - Tests with London coordinates
- **`test_weather_route_edge_cases()`** - Tests coordinates at origin (0,0)
- **`test_http_methods()`** - Tests HTTP method restrictions

### FlaskAppIntegrationTestCase

#### Integration Tests

- **`test_full_application_flow()`** - Tests complete application flow
  - Tests all endpoints in sequence
  - Validates expected status codes

## 🔧 Test Configuration

### Mocking Strategy

The tests use `unittest.mock` to mock external API calls:

```python
@patch('app.requests.get')
def test_weather_route_success(self, mock_get):
    # Mock the external API response
    mock_response = Mock()
    mock_response.json.return_value = {...}
    mock_get.return_value = mock_response
```

### Test Data

Test coordinates used:

- **New York City**: `latitude=40.7128, longitude=-74.0060`
- **London**: `latitude=51.5074, longitude=-0.1278`
- **Origin**: `latitude=0, longitude=0`

## 🐛 Known Issues

### Current Implementation Limitations

The tests document several areas where the current implementation could be improved:

1. **No Input Validation**: The weather endpoint doesn't validate coordinate parameters
2. **No Error Handling**: External API failures aren't handled gracefully
3. **No Parameter Validation**: Invalid coordinates aren't rejected
4. **No HTTP Method Validation**: All routes accept any HTTP method

### Test Expectations

Some tests expect the current behavior (which may not be ideal):

- Missing parameters return 200 instead of 400
- Invalid coordinates return 200 instead of 400
- API errors may cause 500 errors instead of proper error handling

## 📊 Test Results

### Expected Output

When tests pass successfully, you should see output like:

```
test_index_route (tests.FlaskAppTestCase) ... ok
test_health_route (tests.FlaskAppTestCase) ... ok
test_weather_route_success (tests.FlaskAppTestCase) ... ok
test_weather_route_missing_parameters (tests.FlaskAppTestCase) ... ok
...

----------------------------------------------------------------------
Ran 12 tests in 0.123s

OK
```

### Interpreting Results

- **OK**: All tests passed
- **FAIL**: One or more tests failed
- **ERROR**: Tests encountered exceptions

## 🔄 Continuous Integration

### GitHub Actions

The tests can be integrated into CI/CD pipelines:

```yaml
- name: Run Tests
  run: python run_tests.py
```

### Docker Testing

Tests can be run in the Docker container:

```bash
# Build and run tests in container
docker build -t flask-app .
docker run --rm flask-app python run_tests.py
```

## 📝 Adding New Tests

### Test Naming Convention

- Test methods should start with `test_`
- Use descriptive names that explain what is being tested
- Group related tests in the same test class

### Example Test Structure

```python
def test_new_feature(self):
    """Test description of what this test validates"""
    # Arrange - Set up test data
    # Act - Perform the action being tested
    # Assert - Verify the expected outcome
```

### Mocking Guidelines

- Mock external dependencies (APIs, databases)
- Use realistic test data
- Test both success and failure scenarios
- Verify mock calls when appropriate

## 🎯 Best Practices

1. **Test Isolation**: Each test should be independent
2. **Descriptive Names**: Test names should clearly describe what they test
3. **Arrange-Act-Assert**: Structure tests in three clear sections
4. **Mock External Dependencies**: Don't rely on external services in tests
5. **Test Edge Cases**: Include boundary conditions and error scenarios
6. **Maintain Test Data**: Keep test data realistic and up-to-date
