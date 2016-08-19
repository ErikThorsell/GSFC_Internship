#!bin/sh
test $# -ne 1 && { echo "\nUsage: $0 <schedule>";exit 1; }
echo "\nStarting sked...\n"
sked <<EOF
$1
xl wrap
unit $1.azel over
li
unit screen
quit
