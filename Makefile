# Makefile para SuperStore-DataSet

# Levantar todos los servicios
up:
    docker compose up -d

# Apagar todos los servicios
down:
    docker compose down

# Reconstruir imágenes
build:
    docker compose build

# Ver logs del dashboard
logs-dashboard:
    docker compose logs -f dashboard

# Ver logs de Postgres
logs-postgres:
    docker compose logs -f postgres-lab

# Ver logs de Jupyter
logs-jupyter:
    docker compose logs -f jupyter

# Ejecutar el dashboard en modo interactivo
run-dashboard:
    docker compose run --service-ports dashboard

# Limpiar volúmenes y contenedores
clean:
    docker compose down -v --remove-orphans
