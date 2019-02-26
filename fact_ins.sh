#!/bin/bash
echo "Item name:"
read name
echo "Crafting speed:"
read speed
echo "Amount crafted:"
read amount
echo "Max stack:"
read stack
echo 'INSERT INTO item(name,craft_speed,craft_amount,max_stack) VALUES("'$name'",'$speed','$amount','$stack');' ;
mysql -u factorio --password=password123 -D factorio -e 'INSERT INTO item(name,craft_speed,craft_amount,max_stack) VALUES('"\"$name\""','$speed','$amount','$stack');' ;
