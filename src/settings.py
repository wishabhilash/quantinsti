class Config(object):
    broker_url = "redis://localhost:6379/0"
    result_backend = "redis://localhost:6379/1"

    imports = (
        
    )

    ticker_channel = '__ticker__'