#!/bin/bash

INPUT_DIR=$1
OUTPUT_DIR=$2

gnuplot << EOF
set title "Privacy and Access"
set xlabel "Access time (min)"
set ylabel "Privacy level (octal)"
set terminal postscript eps
set output "${OUTPUT_DIR}/privacy_access_summary.eps"
plot [0:] [0:] "${INPUT_DIR}/privacy_access_summary.dat"  using 2:1 with points title "Privacy and Access"
EOF
