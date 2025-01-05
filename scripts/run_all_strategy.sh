#!/bin/bash

for param3 in {1..8}; do
    for param4 in {1..8}; do
        output=$(./run_strategy.sh 0 31 "$param3" "$param4" | grep "Successo" | awk '{ok += $5; ko += $8} END {if (ko > 0) {ratio = ok / ko} else {ratio = "Inf"}; print "Totale OK:", ok, "Totale KO:", ko, "Rapporto:", ratio}')
        echo "[$param3, $param4] $output"
    done
done
