#!/bin/bash

pth=~/research/vic/forcing/ascii # point to the directory where all the sub directories containing the ascii files are

cd $pth

for dir in ./*/; do
	bzip2 -d ./$dir/*
done

