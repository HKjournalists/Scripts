IFS=''
echo "Auto install started" > $HOME/auto_install_script.log
cmd="apt-get install"
echo leo_123 | sudo -S echo "We have started the insatllation process"
while read pkg
do
 cmd="sudo apt-get install --assume-yes $pkg"
 echo $cmd >> $HOME/auto_install_script.log
 eval $cmd
 if [ $? -ne 0 ] ; then
    echo "Unable to install" $pkg
    echo "Unable to install" $pkg >> $HOME/auto_install_script.log
 fi
done < /home/phaniv/nirbhay/scripts/auto_install/pkg.txt

