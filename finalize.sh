#!/bin/bash
read -p "Comment: " cm
git add -A
git commit -am "$cm"
git push origin master
