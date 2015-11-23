if [ $# -ne 1 ] 
then
  echo "Please enter database password\c"
  stty -echo
  read pawd
  stty echo
  echo ""
else
   pwd=$1
fi
while read line
do
echo "Creating dump for "$line
mysqldump -u root -p$pawd $line > $line.sql
if [ $? -ne 0 ]
        then
               echo $line
	       echo "Error while creating dump"
               exit
fi
done < temp
echo "Dump creation completed successfully"

