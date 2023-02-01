0ls#!/bin/bash
echo "***********************************************************************************************************"
echo "Running Experiment 1"
echo "***********************************************************************************************************"

echo "Running sysbench CPU test 1"
sysbench --test=cpu --cpu-max-prime=20000 --num-threads=4 run &
PID=$!

echo "Collecting performance data using top while sysbench test is running"
top -b -d1 -p $PID >> cpu_one.log &
TOP_PID=$!

wait $PID
kill $TOP_PID
echo "***********************************************************************************************************"

echo "Running sysbench CPU test 2"
sysbench --test=cpu --cpu-max-prime=30000 --num-threads=4 run &
PID=$!

echo "Collecting performance data using top while sysbench test is running"
top -b -d1 -p $PID >> cpu_two.log &
TOP_PID=$!

wait $PID
kill $TOP_PID
echo "***********************************************************************************************************"

echo "Running sysbench CPU test 3"
sysbench --test=cpu --cpu-max-prime=20000 --num-threads=2 run &
PID=$!

echo "Collecting performance data using top while sysbench test is running"
top -b -d1 -p $PID >> cpu_three.log &
TOP_PID=$!

wait $PID
kill $TOP_PID
echo "***********************************************************************************************************"
echo "Tests Done"

echo "Tests Done"