if [ $# -lt 1 ] ; then
    echo "help-------First paramter is Backup ID second is the Timestamp(ioptional)"
    echo "Pass Backup id as Paramter."
    echo "Run barman list-backup main"
    exit 1
fi
backup_id=$1

echo "Script Started" > /tmp/barman-script.log
mkdir -p  /tmp/backup
if [ $# -eq 2 ] ; then
    barman recover --target-time "$2" main $backup_id /tmp/backup
else
    barman recover main $backup_id /tmp/backup
fi
if [ $? -ne 0 ]
then
    echo "Error Occured copying backup" >> /tmp/barman-script.lo
fi
echo "==================Barman Recover step completed===================="
#ssh postgres@54.169.172.226 'rm -rf /var/lib/postgresql/9.3/main/*'
ssh postgres@54.169.172.226 "mkdir -p /var/lib/postgresql/9.3/backup/$backup_id/"
if [ $? -ne 0 ]
then
    echo "Error Occured creating directory " >> /tmp/barman-script.lo
fi
echo "==================Directory creation step completed===================="
scp -r /tmp/backup/* postgres@54.169.172.226:/var/lib/postgresql/9.3/backup/$backup_id > /dev/null
if [ $? -ne 0 ]
then
    echo "Error Occured performing scp" >> /tmp/barman-script.lo
fi
echo "==================SCP step completed===================="

cat /tmp/barman-script.log

echo "========================================================================"
echo "In case of error free runi please change data_directory variable to /var/lib/postgresql/9.3/backup/$backup_id"
echo "After this please run sudo service postgresql restart"
