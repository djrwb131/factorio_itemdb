#!/bin/bash
echo "Item name:"
read name
echo "Requirement name:"
read req
echo "Amount required:"
read amount
echo 'INSERT INTO item_requirement(itemID,reqID,amount) VALUES(
( SELECT id FROM item WHERE name="'$name'"),
( SELECT id FROM item WHERE name="'$req'"),
'$amount');' ;

mysql -u root -D factorio -e 'INSERT INTO crafting_req(itemID,reqID,amount) VALUES( ( SELECT id FROM item WHERE name='"\"$name\""'), ( SELECT id FROM item WHERE name='"\"$req\""'), '$amount');' ;
