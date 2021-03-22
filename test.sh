#!/bin/bash
GA="GA"
LIN="Linear"
EN="Entropy"
MM="MaxMin"

# remove existing log files
rm -f GAresults.log
rm -f LinearMM.log
rm -f LinearEN.log
rm -f results.txt


# for each simulation duration
for x in {1..100}; do
    for type in $LIN $GA; do
        if [ $type == $LIN ]; then

            for atype in $EN $MM; do
                while IFS= read -r line
                do
                     echo "[Testing " $type $atype "for " $x " times ]"
                    # take action on $line #
                    echo "line : $line"
                    if [ $atype == $MM ]; then
                            echo "$line">> LinearMM.log
                    elif [ $atype == $EN ]; then
                            echo "$line">> LinearEN.log
                    fi
                done <<< $(python3 ./mastermindbisTest.py $type $atype)
            done
        else :
            while IFS= read -r line
            do
                echo "[Testing " $type "for " $x " times ]"
                # take action on $line #
                echo "$line">> GAresults.log
            done <<< $(python3 ./mastermindbisTest.py $type)
        fi
    done
done
