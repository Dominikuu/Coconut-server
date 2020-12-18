#!/bin/bash

# docker-compose down -v
# docker-compose up --build

COUNT=$(docker ps -a | wc -l)
if (($COUNT > 0)); then
    echo 'container exists'
    echo $COUNT
fi