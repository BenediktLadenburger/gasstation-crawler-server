#!/bin/bash

screen -ls | grep "crawler" | cut -d. -f1 | tr --delete "\t" | xargs kill -9
screen -wipe
