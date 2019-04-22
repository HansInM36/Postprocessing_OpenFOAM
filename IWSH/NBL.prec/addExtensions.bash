#!/bin/bash

find postProcessing/surfaces -type f | xargs -i mv {} {}.csv
