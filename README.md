# Routing manager

Prototype of service for routing management

## Service contains microservices

- api gateway
- routing
- users

## Microservices dependencies

### api gateway

- routing service
- users service

### routing service

- users service
- PostgresSQL

### users service

- PostgresSQL


## Running

```bash
docker-compose up -d --build
```

- api gateway -> http://localhost:8001/docs

Routing and users services containers are also published for easy testing
- routing -> http://localhost:8002/docs
- users -> http://localhost:8003/docs