import os
import socket
from six.moves import zip
from six import iteritems

class Configuration(object):
    DEVELOPMENT_ENVIRONMENTS = ['development', 'dev', 'test']

    OPTIONS = (
        ('api_key', str),
        ('project_root', str),
        ('environment', str),
        ('hostname', str),
        ('endpoint', str),
        ('params_filters', list),
        ('trace_threshold', int),
        ('force_report_data', bool),
    )

    def __init__(self, *args, **kwargs):
        self.api_key = ''
        self.project_root = os.getcwd()
        self.environment = 'production'
        self.hostname = socket.gethostname()
        self.endpoint = 'https://api.honeybadger.io'
        self.params_filters = ['password', 'password_confirmation', 'credit_card']
        self.trace_threshold = 2000
        self.force_report_data = False

        self.set_12factor_config()
        self.set_config_from_dict(kwargs)

    def set_12factor_config(self):
        for option in list(zip(*self.OPTIONS))[0]:
            val = os.environ.get('HONEYBADGER_{}'.format(option.upper()), getattr(self, option))
            option_types = dict(self.OPTIONS)

            try:
                if option_types[option] is list:
                    val = val.split(',')
                elif option_types[option] is int:
                    val = int(val)
            except:
                pass


            setattr(self, option, val)

    def set_config_from_dict(self, config):
        for (key, value) in iteritems(config):
            if key in list(zip(*self.OPTIONS))[0]:
                setattr(self, key, value)

    def is_dev(self):
        """Returns wether you are in a dev environment or not

        A dev environment is defined in the constant DEVELOPMENT_ENVIRONMENTS

        :rtype: bool
        """
        return self.environment in self.DEVELOPMENT_ENVIRONMENTS
