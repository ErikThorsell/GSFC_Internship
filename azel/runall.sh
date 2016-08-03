#!/bin/bash

LOGDIR=./logs/*
SKDDIR=./skds/*
SRCDIR=./script/*

for f in $SKDDIR; do
    SKDFILE="$f"
    echo "$f"
    for l in $LOGDIR; do
        echo "$l"
    done
done
