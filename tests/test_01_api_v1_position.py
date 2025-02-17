from typing import Any

import pytest
from fastapi import Response
from fastapi.testclient import TestClient

from tests.fixtures.position import (
    correct_data_1,
    correct_data_2,
    correct_data_3,
    correct_data_4,
    correct_data_5,
    incorrect_data_1,
    incorrect_data_2,
    incorrect_data_3,
    incorrect_data_4,
    incorrect_data_5,
)

POSITION_URL = "/api/v1/company/position/"


@pytest.mark.parametrize(
    "data_position, status_code",
    (
        (correct_data_1, 201),
        (correct_data_2, 201),
        (correct_data_3, 201),
        (correct_data_4, 201),
        (correct_data_5, 201),
        (incorrect_data_1, 422),
        (incorrect_data_2, 422),
        (incorrect_data_3, 422),
        (incorrect_data_4, 422),
        (incorrect_data_5, 422),
    ),
)
def test_create_position(
    test_client: TestClient,
    data_position: dict[str, Any],
    status_code: int,
):
    response: Response = test_client.post(POSITION_URL, json=data_position)

    assert response.status_code == status_code, (
        f"POST запрос на url {POSITION_URL} с json {data_position} "
        f"должен вернуть status code {status_code}"
    )

    if response.status_code == 201:
        data = response.json()
        data.pop("id")

        missing_keys = data_position.keys() - data.keys()
        assert not missing_keys, (
            f"В ответе на корректный POST-запрос к эндпоинту "
            f"`{POSITION_URL}` не хватает следующих ключей"
            f": `{'`, `'.join(missing_keys)}`"
        )
        assert data == data_position, (
            "При создании Position тело ответа"
            " API отличается от ожидаемого."
        )


@pytest.mark.parametrize(
    "data_position",
    (
        correct_data_1,
        correct_data_2,
        correct_data_3,
        correct_data_4,
        correct_data_5,
    ),
)
def test_create_repeat_position(
    test_client: TestClient,
    data_position: dict[str, Any],
):
    response: Response = test_client.post(POSITION_URL, json=data_position)

    assert response.status_code == 400, (
        f"POST запрос на url {POSITION_URL} с json {data_position} c "
        f"повторными данными должен вернуть status code 400"
    )


def test_get_all(test_client: TestClient):
    response: Response = test_client.get(POSITION_URL)

    assert (
        response.status_code == 200
    ), f"GET запрос на url {POSITION_URL} должен вернуть 200 status code."

    data = response.json()

    assert (
        len(data) > 0
    ), f"json ответа должен возвращать несколько объектов, а не {len(data)}"

    for rs_data in data:
        rs_data.pop("id")

        missing_keys = rs_data.keys() - correct_data_1.keys()
        assert not missing_keys, (
            f"В ответе на корректный POST-запрос к эндпоинту "
            f"`{POSITION_URL}` не хватает следующих ключей"
            f": `{'`, `'.join(missing_keys)}`"
        )


def test_get_for_id(test_client: TestClient):
    response: Response = test_client.get(POSITION_URL)

    all_rs_data = response.json()

    for rs_data in all_rs_data:
        id_ = rs_data.pop("id")
        url = f"{POSITION_URL}{id_}/"
        response: Response = test_client.get(url)

        assert response.status_code == 200, (
            f"GET запрос на url {url} " f"должен вернуть 200 status code."
        )

        missing_keys = rs_data.keys() - correct_data_1.keys()
        assert not missing_keys, (
            f"В ответе на корректный get-запрос к эндпоинту "
            f"`{url}` не хватает следующих ключей"
            f": `{'`, `'.join(missing_keys)}`"
        )


@pytest.mark.parametrize("id_", (9999, 1999, 99999))
def test_get_invalid_id(test_client: TestClient, id_: int):
    url = f"{POSITION_URL}{id_}/"
    response: Response = test_client.get(url)

    assert response.status_code == 400, (
        f"GET запрос на url {url} на несуществующий id"
        f"должен вернуть 400 status code."
    )


def test_update_positions(
    test_client: TestClient,
):
    response: Response = test_client.get(POSITION_URL)

    data_positions = response.json()

    for position in data_positions:
        id_ = position.pop("id")
        url = POSITION_URL + f"{id_}/"
        update_data = {
            "name": "new" + position.get("name")[3:],
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
            f"`{POSITION_URL}` не хватает следующих ключей"
            f": `{'`, `'.join(missing_keys)}`"
        )
        assert data == update_data, (
            "При изменении Position тело ответа"
            " API отличается от ожидаемого."
        )


@pytest.mark.parametrize("id_", (9999, 1999, 99999))
def test_update_invalid_id(test_client: TestClient, id_: int):
    url = f"{POSITION_URL}{id_}/"
    response: Response = test_client.patch(url, json=correct_data_1)

    assert response.status_code == 400, (
        f"Delete запрос на url {url} на несуществующий id"
        f"должен вернуть 400 status code."
    )


def test_delete_for_id(test_client: TestClient):
    response: Response = test_client.get(POSITION_URL)

    all_rs_data = response.json()

    for rs_data in all_rs_data:
        id_ = rs_data.pop("id")
        url = f"{POSITION_URL}{id_}/"
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
    url = f"{POSITION_URL}{id_}/"
    response: Response = test_client.delete(url)

    assert response.status_code == 400, (
        f"Delete запрос на url {url} на несуществующий id"
        f"должен вернуть 400 status code."
    )
