# iniciar docker compose
## criar rede externa

iniciar o docker swarm para utilizar networks de overlay
```bash
docker swarm init
```

criar network externa de overlay
```bash
docker network create --driver overlay --attachable profilesdashboard-rede
```

## docker build
para iniciar o docker compose 
```bash
docker compose up --build
```