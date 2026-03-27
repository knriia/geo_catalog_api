#!/bin/bash
# Останавливаем выполнение при любой ошибке
set -e

# 1. Создаем тестовую базу данных, используя имя основной базы + суффикс _test
# Мы подключаемся к основной базе ($POSTGRES_DB), чтобы выполнить команду CREATE DATABASE
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "${POSTGRES_DB}_test";
EOSQL

# 2. Подключаемся непосредственно к свежесозданной тестовой базе
# и устанавливаем в ней расширение PostGIS, необходимое для работы тестов
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "${POSTGRES_DB}_test" <<-EOSQL
    CREATE EXTENSION IF NOT EXISTS postgis;
EOSQL
