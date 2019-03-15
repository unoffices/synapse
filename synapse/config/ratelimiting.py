# Copyright 2014-2016 OpenMarket Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ._base import Config


class RateLimitConfig(object):
    def __init__(self, config):
        self.per_second = config.get("per_second", 0.17)
        self.burst_count = config.get("burst_count", 3.0)


class RatelimitConfig(Config):

    def read_config(self, config):
        self.rc_messages_per_second = config["rc_messages_per_second"]
        self.rc_message_burst_count = config["rc_message_burst_count"]

        self.rc_registration = RateLimitConfig(config.get("rc_registration", {}))

        rc_login_config = config.get("rc_login", {})
        self.rc_login_address = RateLimitConfig(rc_login_config.get("address", {}))
        self.rc_login_account = RateLimitConfig(rc_login_config.get("account", {}))

        self.federation_rc_window_size = config["federation_rc_window_size"]
        self.federation_rc_sleep_limit = config["federation_rc_sleep_limit"]
        self.federation_rc_sleep_delay = config["federation_rc_sleep_delay"]
        self.federation_rc_reject_limit = config["federation_rc_reject_limit"]
        self.federation_rc_concurrent = config["federation_rc_concurrent"]

    def default_config(self, **kwargs):
        return """\
        ## Ratelimiting ##

        # Number of messages a client can send per second
        #
        rc_messages_per_second: 0.2

        # Number of message a client can send before being throttled
        #
        rc_message_burst_count: 10.0

        # Optional ratelimiting settings for registration and login.
        #
        # Each ratelimiting configuration is made of two parameters:
        #   - per_second: number of requests a client can send per second.
        #   - burst_count: number of requests a client can send before being throttled.
        #
        # If a ratelimiting configuration is omitted from Synapse's configuration,
        # its `per_second` value will default to 0.17 (1/min) and its `burst_count`
        # value will default to 3.0.
        #
        # Synapse currently uses three different configurations:
        #   - one for registration that ratelimits registration requests based on the
        #     client's IP address.
        #   - one for login that ratelimits login requests based on the client's IP
        #     address.
        #   - one for login that ratelimits login requests based on the account the
        #     client is attempting to log into.
        #
        # This configuration follows the following structure:
        #
        # rc_registration:
        #     per_second: 0.17
        #     burst_count: 3
        #
        # rc_login:
        #     address:
        #         per_second: 0.17
        #         burst_count: 3
        #     account:
        #         per_second: 0.17
        #         burst_count: 3

        # The federation window size in milliseconds
        #
        federation_rc_window_size: 1000

        # The number of federation requests from a single server in a window
        # before the server will delay processing the request.
        #
        federation_rc_sleep_limit: 10

        # The duration in milliseconds to delay processing events from
        # remote servers by if they go over the sleep limit.
        #
        federation_rc_sleep_delay: 500

        # The maximum number of concurrent federation requests allowed
        # from a single server
        #
        federation_rc_reject_limit: 50

        # The number of federation requests to concurrently process from a
        # single server
        #
        federation_rc_concurrent: 3
        """
