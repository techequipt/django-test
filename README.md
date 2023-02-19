# Django Test

A test project for potential new employees at TechEquipt

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Description

The task is to create a sample application include API that creates, updates, retrieves and deletes real estate properties (listings) from a local database.

A property should include:

- An address
- Whether it's for sale or lease
- It's price
- A property status (available/sold/leased/deleted)
- When it was created
- When it was last modified
- The user who created it

There should be an API that can filter (list) properties or retrieve a single property. Filtering options should include:

- It's Suburb
- Whether it's for sale or lease
- It's price (as a range)
- It's status
- Ordering for price, created and modified dates
- NOTE: Properties marked as "deleted" should not be returned unless the filter specifically asks for deleted properties

Only the user who created the property (or a superuser) should be able to modify or delete the property

There should be unit tests to confirm the filtering and permissions functionality.

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy django_test

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).
