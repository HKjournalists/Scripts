IFS=''
echo "" > not_install
while read line
do
	pip install $line
	if [ $? -ne 0 ] 
	then
		pip install --allow-all-external $line
		if [ $? -ne 0 ] 
		then
			pip install --allow-all-external $line --allow-unverified $line 
		fi
		if [ $? -ne 0 ]
		then
			echo $line >> not_install 
		fi
	fi
	echo $a
done < temp
echo "-----------Unable to install file list ----------\n"
cat not_install
rm -f not_install
