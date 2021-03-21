#!/bin/bash

# remove existing log files
rm -f GAresults.log
rm -f LinearMM.log
rm -f LinearEN.log


# for each simulation duration
for x in {1..100}; do
    for type in 'GA' 'Linear MaxMin' 'Linear Entropy'; do
    # output the current simulation
        echo "[Testing " $type "for " $x " times ]"

        # run the simulation
        gnome-terminal -- mastermindbisTest.py $type
                
        sleep 7

        #Get the results 
        while read line  
        do   
            if $type == 'GA'
            then
                echo "$line">> GAresults.log
            fi
            if $type == 'Linear MaxMin'
            then
                echo "$line">> LinearMM.log
            fi
            if $type == 'Linear Entropy'
            then
                echo "$line">> LinearEN.log
            fi
        done
    done
done

# remove temporary trace and log file
#rm -f tracefile.lo