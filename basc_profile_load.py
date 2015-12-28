alias c="clear"
alias wd="cd $HOME/IN_workplace"
alias r="python manage.py runserver"
alias py="python manage.py shell"
alias ll="ls -ltr"
for scr in `ls -1 /home/phaniv/nirbhay/scripts/load_alias`
do
  alias `echo $scr | cut -d "." -f1 | cut -c1-3 | tr -d " "`=". $HOME/nirbhay/scripts/load_alias/$scr"
done 
export VISUAL=vi
