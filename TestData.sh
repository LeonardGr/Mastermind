#!/bin/bash
# # remove existing log files
rm -f PSOensembleGA.log

# for each simulation duration
for x in {1..200};do
    for Couleur in '4 8'; do
        echo "[Testing PSO with " $Couleur" positions/couleurs for " $x " times ]"
        while IFS= read -r line
        do
            # take action on $line #
            echo "$Couleur $line">> PSOensembleGA.log
        done <<< $(timeout 30 python3 ./mastermindbisTest.py 'PSO' $Couleur)
    done
done

