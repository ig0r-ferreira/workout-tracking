import requests


class Request(requests.Request):

    def check_method(self) -> None:
        allowed_methods = (
            "POST", "GET", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"
        )

        if self.method not in allowed_methods:
            raise AttributeError(
                f"Invalid method '{self.method}' for request. "
                f"Only the following methods are allowed: "
                f"{', '.join(allowed_methods)}."
            )

    def send(self) -> requests.Response:
        self.check_method()

        with requests.Session() as session:
            try:
                prepped = session.prepare_request(self)
                response = session.send(prepped)
                response.raise_for_status()
            except requests.exceptions.RequestException as err:
                raise Request.get_approp_exception(err)

            return response

    @staticmethod
    def get_approp_exception(
            exception: requests.exceptions.RequestException
    ) -> requests.exceptions.RequestException:
        try:
            raise exception
        except requests.exceptions.ConnectionError:
            return requests.exceptions.ConnectionError(
                "A connection error has occurred. "
                "Check your internet connection."
            )
        except (
            requests.exceptions.HTTPError,
            requests.exceptions.InvalidHeader,
            requests.exceptions.InvalidSchema,
            requests.exceptions.InvalidURL,
            requests.exceptions.MissingSchema,
            requests.exceptions.Timeout,
            requests.exceptions.TooManyRedirects,
            requests.exceptions.URLRequired
        ) as err:
            return err
        except requests.exceptions.RequestException:
            return requests.exceptions.RequestException(
                "An unexpected error has occurred."
            )
