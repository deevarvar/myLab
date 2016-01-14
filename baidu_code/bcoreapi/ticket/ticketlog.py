LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(created)s - %(name)s - %(levelname)s - %(module)s- %(process)d -%(thread)d - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': './ticket_debug.log',
            'mode': 'w+'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',

        }

    },
    'loggers': {
        'ticket': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        }
    }
}
