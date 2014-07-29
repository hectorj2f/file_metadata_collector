#!/bin/bash

INPUT_DIR=$1
OUTPUT_DIR=$2

gnuplot << EOF
set title "Privacy VS Time since last access"
set xlabel "Privacy (octal)"
set ylabel "Time since last access (hrs)"
set terminal postscript eps
set output "${OUTPUT_DIR}/privacy_access.eps"
plot [:] [:777] "${INPUT_DIR}/privacy_access_summary.dat"  using 2:1 with points title "Privacy VS Time since last access"
EOF

gnuplot << EOF
set title "Size VS Time since last access"
set xlabel "Size (mb)"
set ylabel "Time since last access (hrs)"
set terminal postscript eps
set output "${OUTPUT_DIR}/size_access.eps"
plot [0:] [:]"${INPUT_DIR}/size_access_summary.dat"  using 1:2 with points title "Size VS Time since last access"
EOF

gnuplot << EOF
set title "Size VS Privacy"
set xlabel "Size (mb)"
set ylabel "Privacy (octal)"
set terminal postscript eps
set output "${OUTPUT_DIR}/size_privacy.eps"
plot [0:] [:]"${INPUT_DIR}/size_privacy_summary.dat"  using 1:2 with points title "Size VS Privacy"
EOF

gnuplot << EOF
set title "Size VS Time since last modification"
set xlabel "Size (mb)"
set ylabel "Time since last modification (hrs)"
set terminal postscript eps
set output "${OUTPUT_DIR}/size_modification.eps"
plot [0:] [:]"${INPUT_DIR}/size_modification_summary.dat"  using 1:2 with points title "Size VS Time since last modification"
EOF

gnuplot << EOF
set title "Size VS Time diff creation-modification"
set xlabel "Size (mb)"
set ylabel "Time diff creation-modification (hrs)"
set terminal postscript eps
set output "${OUTPUT_DIR}/size_crea_mod.eps"
plot [0:] [:]"${INPUT_DIR}/size_crea_mod_summary.dat"  using 1:2 with points title "Size VS Time diff creation-modification"
EOF

