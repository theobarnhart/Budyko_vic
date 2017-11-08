#!/bin/bash

pth=~/research/vic/fluxes/ascii # point to the directory where all the sub directories containing the ascii files are

cd $pth

for dir in ./*/; do
	bzip2 ./$dir/*
done

