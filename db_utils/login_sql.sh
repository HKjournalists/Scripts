db=`echo $1`
mysql -u root -proot `echo $db` 2>/dev/null
if [ $? -ne 0 ] ; then
    echo "show databases" > /tmp/temp_script_output_script_outputmysql.txt
    mysql -u root -proot  < /tmp/temp_script_output_script_outputmysql.txt > /tmp/temp_script_output_script_outputmysql_result.txt
    cnt=`cat /tmp/temp_script_output_script_outputmysql_result.txt | grep $db | wc -l`
    if [ $cnt -gt 1 ] ; then
       echo "Unable to find unique match for database.Below are choices"
       cat /tmp/temp_script_output_script_outputmysql_result.txt | grep $db
    elif [ $cnt -eq 1 ] ; then
        echo "Using Database" `cat /tmp/temp_script_output_script_outputmysql_result.txt | grep $db`
        mysql -u root -proot `cat /tmp/temp_script_output_script_outputmysql_result.txt | grep $db`
    else
        print "No match for given database"
    fi 
fi
rm -f /tmp/temp_script_output_mysql.txt /tmp/temp_script_output_mysql_result.txt
        
        
  
