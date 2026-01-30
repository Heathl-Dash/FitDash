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

ESSA BRANCH SERÁ UTILIZADA APENAS PARA TESTES E NÃO DEVE TER MERGES

executar o comando abaixo para gerar dados falsos para testes de estresse
```bash
docker compose exec django_fitdashboard python manage.py seed_data
```
