#!/bin/bash
# $1=arduino
# $2=host
# $3=port
# $4=ds size


ard=$(dmesg | grep tty | grep ACM | tr -s ' ' | cut -d ' ' -f 5 | tr -s ':' | cut -d ':' -f 1);
fullArd="/dev/$ard" ;
echo $fullArd ;

python app.py $fullArd $1 $2 $3 ;


