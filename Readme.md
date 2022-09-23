## Usage
Commands to run application
```bash
docker-compose up -d build
docker-compose exec backend python3 manage.py migrate
docker-compose logs -f backend
```

## Testing 
Command to run tests
```bash
docker-compose exec backend python3 manage.py test
```
