from constants import BASE_URL_API, MOVIES_ENDPOINT
from custom_requester.custom_requester import CustomRequester


class MovieAPI(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=BASE_URL_API)

    def get_movies(self, params=None, expected_status=200):
        return self.send_request(
            method="GET",
            endpoint=MOVIES_ENDPOINT,
            params=params,
            expected_status=expected_status
        )

    def get_movie_by_id(self, params=None, expected_status=200, movie_id=None):
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            params=params,
            expected_status=expected_status
        )

    def create_movie(self, movie_data, expected_status=None):
        if expected_status is None:
            expected_status = [200, 201]

        return self.send_request(
            method="POST",
            endpoint=MOVIES_ENDPOINT,
            data=movie_data,
            expected_status=expected_status
        )

    def delete_movie(self, expected_status=200, movie_id=None, params=None):
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            expected_status=expected_status,
            params=params
        )

    def update_movie(self, movie_data, movie_id=None, expected_status=200):
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            data=movie_data,
            expected_status=expected_status
        )
