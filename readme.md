# iniciar docker compose
## criar rede externa
essa rede deve ser criada antes de qualquer um dos serviços, pois os conecta ao nginx

```bash
docker network create gateway-shared-net
```

## docker build
para iniciar o docker compose 
```bash
docker compose up --build
```