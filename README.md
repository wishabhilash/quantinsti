# quantinsti

## Deployment:
1. ./deploy.sh
2. Set mysql user as 'root' and password as 'chicken'
3. Login into mysql and create database:
    quantinsti

## Show help
Command parser is created using argparse. Hence nested helps are enabled by default.
    python src/run.py -h

## Prepare DB
Fire the command below:
    python src/run.py sync

## Start services
### Celery
    python src/run.py celery

### Ticker
    python src/run.py ticker -l=5 (optional)

### Strategy
    python src/run.py strategy {strategy_name} {instrument} {userid}
    use -h for additional parameters.
        Ex. python src/run.py strategy macrossover 121 wish

