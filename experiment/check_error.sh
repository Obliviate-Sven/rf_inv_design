#! /bin/bash

end_time=$(date -d "2025-03-30 00:00:00" +%s)

while [ $(date +%s) -lt $end_time ]; do

	grep -rH "ERROR" ./ --include="*.log"
	find ./ -type f -name "*data.csv" -exec wc -l {} + | awk '{sum += $1} END {print "Total lines:", sum}'
	echo "--$(date "+%Y-%m-%d %H:%M:%S")-- Check"
	sleep 30
done

