ard=$(dmesg | grep tty | grep ACM | tr -s ' ' | cut -d ' ' -f 5 | tr -s ':' | cut -d ':' -f 1);
fullArd="/dev/$ard" ;
echo $fullArd ;

python app.py $fullArd "web-dev" "5050" 5


