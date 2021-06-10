# Contributing

Please be sure to read the contribution guidelines before making or requesting a change.

## Development Environment

1. Create a virtual environment: `python3 -m venv venv`
2. Activate the virtual environment: `source venv/bin/activate`
3. Install development dependencies: `pip install -e '.[dev]'`
4. Hack away :tada:

## Running Tests

The tests make requests to the Smartcar API, so you'll need to create an application on Smartcar and get your client id
and client secret. You'll also need to add the testing redirect URI to your application.

1. Create an application on the [developer dashboard](https://dashboard.smartcar.com)
2. Add `https://example.com/auth` as a redirect URI
3. Pass the client id and client secret to the tests as environment variables

```
export E2E_SMARTCAR_CLIENT_ID='<YOUR CLIENT ID>'
export E2E_SMARTCAR_CLIENT_ID='<YOUR CLIENT SECRET>'
```

4. Run tests: `make test`

## Formatting

All code in this repository is formatted using [black](https://github.com/python/black). Please format all contributions
using the tool.

## Creating a pull request

Please make sure that your commits follow
the [Angular Commit Message Conventions](https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#-git-commit-guidelines)
and the "type" for each commit message conveys the intent with respect to releasing as defined
by [semantic-release](https://github.com/semantic-release/semantic-release#commit-message-format).
