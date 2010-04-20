#!/bin/sh

# Write down the current git version just for future reference as coverage
# progresses or regresses.
git log | head -1 > .coverage-version-stamp

# This script depends on trialcoverage >= 0.3 and on coverage.py >= 3.3.2a1z8.
# The following lines will print an ugly warning message if those two are not
# installed.
python -c 'import pkg_resources;pkg_resources.require("trialcoverage>=0.3")' &&
python -c 'import pkg_resources;pkg_resources.require("coverage>=3.3.2a1z8")' &&

python setup.py flakes && python setup.py trial --reporter=bwverbose-coverage --rterrors && 

( echo "SUCCESS"
echo
echo "To see coverage details run 'coverage report' or run 'coverage html' and look at htmlcov/index.html." )
