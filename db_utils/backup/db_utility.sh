#How to use this script
#Write the databases name in file.
#File name should be temp
#Dump should have name as database_name.sql
#Eg: If database name is test then dump name should be test.sql in same folder 
#where script is present.

clear
echo "\n\n\n\n\n\n\n"
echo "=========================Welcome to create and load dump utility========================="
echo "                         1) Create dump File                          "
echo "                         2) Load dump file (Revert)                          "
echo "                         Enter any other key to quit \c"
read choice

case $choice in
    1|2)
       echo "Please enter database password \c"
       stty -echo
       read pawd
       stty echo
       echo ""
       if [ $choice -eq 1 ] ; then
           while read line
           do
               echo "Creating dump for "$line
               mysqldump -u root -p$pawd $line > $line.sql
               if [ $? -ne 0 ] ; then
                   echo "Error while creating dump for "$line
                   exit
               fi
           done < temp
           echo "Dump creation completed successfully"
       fi
       
       if [ $choice -eq 2 ] ; then
           echo "=============Database Creation started(if not present)============="
           #Loop for creating database it not present
           while read line
           do
               #echo "SET TERMOUT OFF ;" > tmp_dbfile
               echo "create database "$line > tmp_dbfile
               mysql -u root -p$pawd < tmp_dbfile > tmp_db_error 2>tmp_db_error
               if [ $? -ne 0 ] ; then
                   count=`cat tmp_db_error | grep -i "database exists" | wc -l`
                   if [ $count -gt 0 ] ; then
                       echo $line" Database already present. No need to create again"
                       continue
                   else
                       cat tmp_db_error | grep -i "Access denied"
                       if [ $? -ne 0 ] ; then
                           echo "Password for user root is incorrect"
                           exit
                       fi
                       echo "Database Creation error for "$line
                       cat tmp_db_error
                       #rm -f tmp_dbfile tmp_db_error #Remove temporary file
                       exit
                   fi
               fi
           done < temp
        rm -f tmp_dbfile tmp_db_error #Remove temporary file
        echo "=============Dump loading process started============="
        while read line
        do
            echo "Loading dump for "$line
            mysql -u root -p$pawd $line < $line.sql
             if [ $? -ne 0 ] ; then
	         echo "Error while loading dump for "$line
                 exit
             fi
        done < temp
        echo "=============Dump load completed successfully============="
        fi
        ;;
   '*') echo "Quiting "
        ;;
esac
