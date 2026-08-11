import pyotp
from SmartApi import SmartConnect

from market_analytics.utils.config import config
from market_analytics.utils.logger import logger


class SmartAPIClient:

    def __init__(self):

        self.api_key = config.ANGEL_API_KEY
        self.client_code = config.ANGEL_CLIENT_CODE
        self.password = config.ANGEL_PASSWORD
        self.totp_secret = config.ANGEL_TOTP_SECRET

        self.smart_api = None
        self.jwt_token = None
        self.refresh_token = None
        self.feed_token = None


    def login(self):

        logger.info(
            "Logging in to Angel One SmartAPI."
        )

        try:

            totp = pyotp.TOTP(
                self.totp_secret
            ).now()

            self.smart_api = SmartConnect(
                api_key=self.api_key
            )

            response = self.smart_api.generateSession(
                self.client_code,
                self.password,
                totp
            )

            if not response["status"]:

                logger.error(
                    f"SmartAPI login failed: {response['message']}"
                )

                raise Exception(
                    response["message"]
                )

            self.jwt_token = response["data"]["jwtToken"]

            self.refresh_token = response["data"]["refreshToken"]

            self.feed_token = self.smart_api.getfeedToken()

            self.smart_api.generateToken(
                self.refresh_token
            )

            logger.info(
                "Successfully logged in to Angel One SmartAPI."
            )

            return True

        except Exception:

            logger.exception(
                "Failed to login to Angel One SmartAPI."
            )

            raise


    def logout(self):

        logger.info(
            "Logging out from Angel One SmartAPI."
        )

        try:

            if self.smart_api is not None:

                self.smart_api.terminateSession(
                    self.client_code
                )

            self.smart_api = None
            self.jwt_token = None
            self.refresh_token = None
            self.feed_token = None

            logger.info(
                "Successfully logged out from Angel One SmartAPI."
            )

        except Exception:

            logger.exception(
                "Failed to logout from Angel One SmartAPI."
            )

            raise