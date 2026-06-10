# Diplom_2 — API Tests for Stellar Burgers

Automated API tests for the [Stellar Burgers](https://stellarburgers.education-services.ru/) service,
written as part of the Yandex Practicum QA Automation course.

---

## What Is Tested

### User Registration
- Successfully create a new unique user
- Attempt to create a user that is already registered
- Attempt to create a user with a required field missing (parametrized: email, password, name)

### User Login
- Successfully log in with valid credentials
- Attempt to log in with a wrong password
- Attempt to log in with a non-existent account
- Attempt to log in with a required field missing (parametrized: email, password)

### Order Creation and Retrieval
- Create an order as an authorized user
- Create an order as an unauthorized user
- Attempt to create an order without ingredients
- Attempt to create an order with an invalid ingredient hash
- Retrieve the order list as an authorized user
- Attempt to retrieve the order list without authorization

---

## Tech Stack

- Python 3.x
- pytest
- requests
- allure-pytest

---

## How to Run

Install dependencies:
```bash
pip install -r requirements.txt
```

Run tests:
```bash
pytest -v
```

Generate an Allure report:
```bash
pytest --alluredir=allure_results
allure serve allure_results
```

---

## Project Structure

| Path | Description |
|------|-------------|
| `tests/test_user_create.py` | User registration tests |
| `tests/test_user_login.py` | User login tests |
| `tests/test_order_create.py` | Order creation and retrieval tests |
| `tests/conftest.py` | Fixtures: user, authorization, order, ingredients |
| `helpers/user_helper.py` | User API calls: register, login, delete |
| `helpers/order_helper.py` | Order API calls: create, get, ingredients |
| `data.py` | Constants: base URL, API paths, status codes, server messages |
| `requirements.txt` | Pinned project dependencies |
