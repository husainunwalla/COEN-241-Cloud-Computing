#!/bin/bash
echo "***********************************************************************************************************"
echo "Running Experiment 2"
echo "***********************************************************************************************************"


for mode in seqwr seqrewr seqrd rndrd rndwr rndrw; do
 echo "Testing $mode mode..."
  sysbench fileio --file-test-mode=$mode prepare

  # Start iostat to monitor disk I/O
  iostat -dxk 1 &

  # Run sysbench fileio test
  sysbench fileio --file-test-mode=$mode run

  # Stop iostat
  kill $!

  sysbench fileio --file-test-mode=$mode cleanup
  echo "***********************************************************************************************************"
done

echo "All tests completed"