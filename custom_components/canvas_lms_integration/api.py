"""Sample API Client."""

from __future__ import annotations

import socket
from typing import Any

import aiohttp
import async_timeout

from .const import LOGGER


class CanvasLmsApiClientError(Exception):
    """Exception to indicate a general API error."""


class CanvasLmsApiClientCommunicationError(
    CanvasLmsApiClientError,
):
    """Exception to indicate a communication error."""


class CanvasLmsApiClientAuthenticationError(
    CanvasLmsApiClientError,
):
    """Exception to indicate an authentication error."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    if response.status in (401, 403):
        msg = "Invalid credentials"
        raise CanvasLmsApiClientAuthenticationError(
            msg,
        )
    response.raise_for_status()


class CanvasLmsApiClient:
    """Sample API Client."""

    def __init__(
        self,
        canvas_base_url: str,
        api_key: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Sample API Client."""
        self._canvas_base_url = canvas_base_url
        self._apiKey = api_key
        self._session = session

    async def async_get_user(self, user_id:str) -> Any:
        """Get the specified user."""
        return await self._api_wrapper(
            method="get",
            path=f"v1/users/{user_id}",
            headers={"Content-type": "application/json; charset=UTF-8",
                     "Authorization": f"Bearer {self._apiKey}"},
        )

    async def async_get_observees(self, user_id: str) -> Any:
        """Get the observees for the specified user."""
        return await self._api_wrapper(
            method="get",
            path=f"v1/users/{user_id}/observees",
            headers={"Content-type": "application/json; charset=UTF-8",
                     "Authorization": f"Bearer {self._apiKey}"},
        )

    async def async_get_missing_assignments(self, user_id: str) -> Any:
        """Get the missing assignments for specified user."""
        assignments = await self._api_wrapper(
            method="get",
            path=f"v1/users/{user_id}/missing_submissions?include[]=course&filter[]=submittable",
            headers={"Content-type": "application/json; charset=UTF-8",
                     "Authorization": f"Bearer {self._apiKey}"},
        )

        results = []
        for assignment in assignments:
            result = {
                "id": assignment["id"],
                "name": assignment["name"],
                "description": assignment["description"],
                "due_date": assignment["due_at"],
                "locks_at": assignment["lock_at"],
                "course": assignment["course"]["name"],
                "course_og_name": assignment["course"]["original_name"],
            }
            results.append(result)

        return results

    async def async_get_courses(self, user_id: str) -> Any:
        """Get courses for specified user."""
        courses = await self._api_wrapper(
            method="get",
            path=f"v1/users/{user_id}/courses?include[]=teachers&include[]=term&include[]=syllabus_body&enrollment_state=active",
            headers={"Content-type": "application/json; charset=UTF-8",
                     "Authorization": f"Bearer {self._apiKey}"},
        )

        results = []
        for course in courses:
            result = {
                "id": course["id"],
                "name": course["name"],
                "friendlyName": course["friendly_name"],
                "syllabus": course["syllabus_body"],
                "teacher": course["teachers"][0]["display_name"],
                "calendar_ics": course["calendar"]["ics"],
                "term": course["term"],
            }
            results.append(result)

        LOGGER.info(f"mapped courses to results {results}")
        return results

    async def _api_wrapper(
        self,
        method: str,
        path: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> Any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=f"{self._canvas_base_url}{path}",
                    headers=headers,
                    json=data,
                )
                _verify_response_or_raise(response)
                return await response.json()

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise CanvasLmsApiClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise CanvasLmsApiClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise CanvasLmsApiClientError(
                msg,
            ) from exception
