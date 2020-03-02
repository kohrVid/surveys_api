if [[ -z $(which inotifywait) ]]
  then
    whichDistro=$(uname)
    case $OS in
      'debian')
        sudo aptitude install inotify-tools
        ;;
      'arch')
        sudo pacman -S inotify-tools --no-confirm
        ;;
      *)
        echo "Please install inotify"
        ;;
    esac
fi

inotifywait -e close_write,moved_to,create -mr ./ | grep '\.py$' --line-buffered |
while read directory events filename; do
  echo $events
  if [ "$events" == "CLOSE_WRITE,CLOSE" ]
    then
      DATABASE_NAME=test_surveys_api make db-drop
      make test
  fi
done


whichDistro() {
  if [[ "`hostnamectl`" =~ 'Ubuntu' ]]
  then
    echo "debian"
  elif [[ "`hostnamectl`" =~ 'Debian' ]]
  then
    echo "debian"
  elif [[ "`hostnamectl`" =~ 'Arch' ]]
  then
    echo "arch"
  elif [[ "`hostnamectl`" =~ 'Manjaro' ]]
  then
    echo "arch"
  else
    echo "Unknown distro" 1>&2
    exit 1
  fi
}

main
