from typing import Any

import pytest
from fastapi import Response
from fastapi.testclient import TestClient

# from src.company.models import Division

from tests.fixtures.division import (
    correct_data_1,
    correct_data_2,
    correct_data_3,
    correct_data_4,
    correct_data_5,
    correct_data_6,

    incorrect_data_1,
    incorrect_data_2,
    incorrect_data_3,
    incorrect_data_4,
    incorrect_data_5,
    incorrect_data_6,

    child_department
)

DIVISION_URL = "/api/v1/company/division/"


@pytest.mark.parametrize(
    "data_division, status_code",
    (
        (correct_data_1, 201),
        (correct_data_2, 201),
        (correct_data_3, 201),
        (correct_data_4, 201),
        (correct_data_5, 201),
        (correct_data_6, 201),

        (correct_data_1, 400),
        (correct_data_2, 400),
        (correct_data_3, 400),
        (correct_data_4, 400),
        (correct_data_5, 400),
        (correct_data_6, 400),

        (incorrect_data_1, 422),
        (incorrect_data_2, 422),
        (incorrect_data_3, 422),
        (incorrect_data_4, 422),
        (incorrect_data_5, 422),
        (incorrect_data_6, 422),
    ),
)
def test_create_division(
    test_client: TestClient,
    data_division: dict[str, Any],
    status_code: int,
):
    response: Response = test_client.post(DIVISION_URL, json=data_division)

    assert response.status_code == status_code, (
        f"POST запрос на url {DIVISION_URL} с json {data_division} "
        f"должен вернуть status code {status_code}"
    )

    if response.status_code == 201:
        data = response.json()
        data.pop("id")

        missing_keys = data_division.keys() - data.keys()
        assert not missing_keys, (
            f"В ответе на корректный POST-запрос к эндпоинту "
            f"`{DIVISION_URL}` не хватает следующих ключей"
            f": `{'`, `'.join(missing_keys)}`"
        )


def test_create_division_incorrect_id(
    test_client: TestClient,
):
    child_department["parent_id"] = 9999
    response: Response = test_client.post(DIVISION_URL, json=child_department)
    assert response.status_code == 400, (
        f"POST запрос на url {DIVISION_URL} с json {child_department} "
        f"должен вернуть status code 400"
    )


def test_create_division_for_parent(
    test_client: TestClient, division
):
    child_department["parent_id"] = division.id
    response: Response = test_client.post(DIVISION_URL, json=child_department)
    assert response.status_code == 201, (
        f"POST запрос на url {DIVISION_URL} с json {child_department} "
        f"должен вернуть status code 201"
    )
    data = response.json()
    data.pop("id")

    missing_keys = child_department.keys() - data.keys()
    assert not missing_keys, (
        f"В ответе на корректный POST-запрос к эндпоинту "
        f"`{DIVISION_URL}` не хватает следующих ключей"
        f": `{'`, `'.join(missing_keys)}`"
    )
    assert data == child_department, (
        "При создании Position тело ответа"
        " API отличается от ожидаемого."
    )


def test_get_all(test_client: TestClient):
    response: Response = test_client.get(DIVISION_URL)

    assert (
        response.status_code == 200
    ), f"GET запрос на url {DIVISION_URL} должен вернуть 200 status code."

    data = response.json()

    assert (
        len(data) > 0
    ), f"json ответа должен возвращать несколько объектов, а не {len(data)}"

    for rs_data in data:
        keys = {"id", "name", "parent_id"}
        missing_keys = rs_data.keys() - keys
        assert not missing_keys, (
            f"В ответе на корректный POST-запрос к эндпоинту "
            f"`{DIVISION_URL}` не хватает следующих ключей"
            f": `{'`, `'.join(missing_keys)}`"
        )


def test_get_for_id(test_client: TestClient):
    response: Response = test_client.get(DIVISION_URL)

    all_rs_data = response.json()

    for rs_data in all_rs_data:
        id_ = rs_data.pop("id")
        url = f"{DIVISION_URL}{id_}/"
        response: Response = test_client.get(url)

        assert response.status_code == 200, (
            f"GET запрос на url {url} " f"должен вернуть 200 status code."
        )

        keys = {"id", "name", "parent_id"}
        missing_keys = rs_data.keys() - keys
        assert not missing_keys, (
            f"В ответе на корректный get-запрос к эндпоинту "
            f"`{url}` не хватает следующих ключей"
            f": `{'`, `'.join(missing_keys)}`"
        )


@pytest.mark.parametrize("id_", (9999, 1999, 99999))
def test_get_invalid_id(test_client: TestClient, id_: int):
    url = f"{DIVISION_URL}{id_}/"
    response: Response = test_client.get(url)

    assert response.status_code == 400, (
        f"GET запрос на url {url} на несуществующий id"
        f"должен вернуть 400 status code."
    )


def test_update_division(
    test_client: TestClient, division
):
    response: Response = test_client.get(DIVISION_URL)

    data_division = response.json()

    for data_div in data_division:
        id_ = data_div.pop("id")
        if id_ == division.id:
            continue
        url = DIVISION_URL + f"{id_}/"
        update_data = {
            "name": "new" + data_div.get("name")[3:],
            "parent_id": division.id
        }
        response: Response = test_client.patch(url, json=update_data)
        assert response.status_code == 201, (
            f"PATCH запрос на url {url} с json {update_data} "
            f"должен вернуть status code 201."
        )

        data = response.json()
        data.pop("id")

        missing_keys = update_data.keys() - data.keys()
        assert not missing_keys, (
            f"В ответе на корректный POST-запрос к эндпоинту "
            f"`{DIVISION_URL}` не хватает следующих ключей"
            f": `{'`, `'.join(missing_keys)}`"
        )
        assert data == update_data, (
            "При изменении division тело ответа"
            " API отличается от ожидаемого."
        )


@pytest.mark.parametrize("id_", (9999, 1999, 99999))
def test_update_invalid_id(test_client: TestClient, id_: int):
    url = f"{DIVISION_URL}{id_}/"
    response: Response = test_client.patch(url, json=correct_data_1)

    assert response.status_code == 400, (
        f"Delete запрос на url {url} на несуществующий id"
        f"должен вернуть 400 status code."
    )


def test_update_division_id_equal_and_parent_id(
    test_client: TestClient,
):
    response: Response = test_client.get(DIVISION_URL)

    data_division = response.json()

    for division in data_division:
        id_ = division.pop("id")
        url = DIVISION_URL + f"{id_}/"
        update_data = {
            "name": "wew" + division.get("name")[3:],
            "parent_id": id_
        }
        response: Response = test_client.patch(url, json=update_data)
        assert response.status_code == 400, (
            f"PATCH запрос на url {url} с json {update_data} "
            f"должен вернуть status code 400."
        )


def test_update_division_incorrect_id(
    test_client: TestClient,
):
    response: Response = test_client.get(DIVISION_URL)

    data_division = response.json()

    for division in data_division:
        id_ = division.pop("id")
        url = DIVISION_URL + f"{id_}/"
        update_data = {
            "name": "wew" + division.get("name")[3:],
            "parent_id": 50020
        }
        response: Response = test_client.patch(url, json=update_data)
        assert response.status_code == 400, (
            f"PATCH запрос на url {url} с json {update_data} "
            f"должен вернуть status code 400."
        )


def test_delete_for_id(test_client: TestClient):
    response: Response = test_client.get(DIVISION_URL)

    all_rs_data = response.json()

    for rs_data in all_rs_data:
        id_ = rs_data.pop("id")
        url = f"{DIVISION_URL}{id_}/"
        response: Response = test_client.delete(url)

        assert response.status_code == 204, (
            f"Delete запрос на url {url} " f"должен вернуть 204 status code."
        )

        response: Response = test_client.delete(url)
        assert response.status_code == 400, (
            f"Повторный DELETE запрос на url {url} "
            f"должен вернуть 400 status code."
        )


@pytest.mark.parametrize("id_", (9999, 1999, 99999))
def test_delete_invalid_id(test_client: TestClient, id_: int):
    url = f"{DIVISION_URL}{id_}/"
    response: Response = test_client.delete(url)

    assert response.status_code == 400, (
        f"Delete запрос на url {url} на несуществующий id"
        f"должен вернуть 400 status code."
    )
