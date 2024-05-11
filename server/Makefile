.PHONY: dev-build
dev-build:
	docker compose -f docker-compose-dev.yml build

.PHONY: dev-up-d
dev-up-d:
	docker compose -f docker-compose-dev.yml up -d

.PHONY: dev
dev:
	@make dev-build
	@make dev-up-d

.PHONY: down
down:
	docker compose -f docker-compose-dev.yml down

.PHONY: blueup
blueup:
	docker compose -f docker-compose-dev.yml up -d --no-deps --build django-blue

.PHONY: bluestop
bluestop:
	docker compose -f docker-compose-dev.yml stop django-blue

.PHONY: greenup
greenup:
	docker compose -f docker-compose-dev.yml up -d --no-deps --build django-green

.PHONY: greenstop
greenstop:
	docker compose -f docker-compose-dev.yml stop django-green

.PHONY: logs
logs:
	docker compose -f docker-compose-dev.yml logs -f

.PHONY: logsblue
logsblue:
	docker compose -f docker-compose-dev.yml logs -f django-blue


.PHONY: logsgreen
logsgreen:
	docker compose -f docker-compose-dev.yml logs -f django-green

.PHONY: test
test:
	docker compose -f docker-compose-dev.yml exec django-green python manage.py test

.PHONY: black
black:
	docker compose -f docker-compose-dev.yml exec django-green black .

.PHONY: isort
isort:
	docker compose -f docker-compose-dev.yml exec django-green isort .

.PHONY: flake8
flake8:
	docker compose -f docker-compose-dev.yml exec django-green flake8 .

.PHONY: lint
lint:
	@make black
	@make isort
	@make flake8

.PHONY: execblue
execblue:
	docker compose -f docker-compose-dev.yml exec django-blue bash

.PHONY: delete
delete:
	rm -rf db/



.PHONY: prod-build
prod-build:
	docker compose -f docker-compose-prod.yml build

.PHONY: prod-up-d
prod-up-d:
	docker compose -f docker-compose-prod.yml up -d

# .PHONY: prod
# prod:
# 	@make prod-build
# 	@make prod-up-d

.PHONY: proddown
proddown:
	docker compose -f docker-compose-prod.yml down


.PHONY: prodblueup
prodblueup:
	docker compose -f docker-compose-prod.yml up -d --no-deps --build django-blue

.PHONY: prodbluestop
prodbluestop:
	docker compose -f docker-compose-prod.yml stop django-blue

.PHONY: prodgreenup
prodgreenup:
	docker compose -f docker-compose-prod.yml up -d --no-deps --build django-green

.PHONY: prodgreenstop
prodgreenstop:
	docker compose -f docker-compose-prod.yml stop django-green


.PHONY: prodlogs
prodlogs:
	docker compose -f docker-compose-prod.yml logs -f

.PHONY: prodlogsblue
prodlogsblue:
	docker compose -f docker-compose-prod.yml logs -f django-blue

.PHONY: prodlogsgreen
prodlogsgreen:
	docker compose -f docker-compose-prod.yml logs -f django-green

.PHONY: prodexecblue
prodexecblue:
	docker compose -f docker-compose-prod.yml exec django-blue bash

