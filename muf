#!/bin/bash

python fms.py $1 $2
echo ""
python procedures.py $1 $2
