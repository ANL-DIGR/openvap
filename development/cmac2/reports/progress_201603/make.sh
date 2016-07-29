#!/usr/bin/env bash

#change the below to your complilers.. these should work for people with tex on osx

ytex=/usr/local/texlive/2015/bin/universal-darwin/pdflatex
btex=/usr/local/texlive/2015/bin/universal-darwin/bibtex
infile=cmac2p0_progress 
echo $mytex
echo $infile

rm $infile.aux $infile.pdf $infile.bbl $infile.dvi

$ytex $infile
$btex $infile
$ytex $infile
$ytex $infile


