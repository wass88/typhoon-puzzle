#!/bin/bash -ex
FILE=$1
if [ -z "$FILE" ]; then
	echo "Usage: run.sh <file>"
	exit 1
fi

SUGAR="./sugar-2.3.4/bin/sugar -jar sugar-2.3.4/bin/sugar-2.3.4.jar -solver z3"

echo Genearete csp
./solve_fast.py < $FILE > "${FILE}.csp"

echo Solve csp with sugar
$SUGAR "${FILE}.csp" > "${FILE}.res"

echo Parse output of suger
./parse_output_fast.py < "${FILE}.res" > "${FILE}.parsed.csp"

echo Check uniqueness
cat "${FILE}.csp" "${FILE}.parsed.csp" > "${FILE}.uniq.csp"
$SUGAR "${FILE}.uniq.csp" > "${FILE}.uniq.res"
./parse_output_fast.py uniq < "${FILE}.uniq.res" > "${FILE}.uniq.parsed.csp"
