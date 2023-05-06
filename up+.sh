#!/bin/bash
#set -e
##################################################################################################################
# Author    : Erik Dubois
# Website   : https://www.erikdubois.be
# Website   : https://www.alci.online
# Website   : https://www.ariser.eu
# Website   : https://www.arcolinux.info
# Website   : https://www.arcolinux.com
# Website   : https://www.arcolinuxd.com
# Website   : https://www.arcolinuxb.com
# Website   : https://www.arcolinuxiso.com
# Website   : https://www.arcolinuxforum.com
##################################################################################################################
#
#   DO NOT JUST RUN THIS. EXAMINE AND JUDGE. RUN AT YOUR OWN RISK.
#
##################################################################################################################
#tput setaf 0 = black
#tput setaf 1 = red
#tput setaf 2 = green
#tput setaf 3 = yellow
#tput setaf 4 = dark blue
#tput setaf 5 = purple
#tput setaf 6 = cyan
#tput setaf 7 = gray
#tput setaf 8 = light blue
##################################################################################################################

# reset - commit your changes or stash them before you merge
# git reset --hard - personal alias - grh

workdir=$(pwd)

if [ -d $workdir/usr/share/arcolinux-app/work ]; then
	echo "Removing work directory"
	sudo rm -rv $workdir/usr/share/arcolinux-app/work
fi

# checking if I have the latest files from github
echo "Checking for newer files online first"
git pull


echo "Keyring from ArcoLinux"
rm -v $workdir/usr/share/arcolinux-app/packages/arcolinux-keyring/*
cp -v /home/erik/ARCO/ARCOLINUX-REPO/arcolinux_repo/x86_64/arcolinux-keyring*pkg.tar.zst $workdir/usr/share/arcolinux-app/packages/arcolinux-keyring

echo "Mirror from ArcoLinux"
rm -v $workdir/usr/share/arcolinux-app/packages/arcolinux-mirrorlist/*
cp -v /home/erik/ARCO/ARCOLINUX-REPO/arcolinux_repo/x86_64/arcolinux-mirror*pkg.tar.zst $workdir/usr/share/arcolinux-app/packages/arcolinux-mirrorlist

#pacman.conf
echo "get the pacman.conf from ArchLinux"
wget https://gitlab.archlinux.org/archlinux/archiso/-/raw/master/configs/releng/pacman.conf -O $workdir/usr/share/arcolinux-app/data/arch/pacman.conf

echo "get the pacman.conf from ArcoLinux"
wget https://raw.githubusercontent.com/arcolinux/arcolinuxl-iso/master/archiso/airootfs/etc/pacman.conf -O $workdir/usr/share/arcolinux-app/data/arco/pacman.conf


echo "get the pacman.conf from EOS"
wget https://raw.githubusercontent.com/endeavouros-team/EndeavourOS-ISO/main/airootfs/etc/pacman.conf -O $workdir/usr/share/arcolinux-app/data/eos/pacman.conf

echo "get the pacman.conf from EOS"
wget https://gitlab.com/garuda-linux/tools/garuda-tools/-/raw/master/data/pacman-multilib.conf -O $workdir/usr/share/arcolinux-app/data/garuda/pacman.conf


# Below command will backup everything inside the project folder
git add --all .

# Give a comment to the commit if you want
echo "####################################"
echo "Write your commit comment!"
echo "####################################"

read input

# Committing to the local repository with a message containing the time details and commit text

git commit -m "$input"

# Push the local files to github

if grep -q main .git/config; then
	echo "Using main"
		git push -u origin main
fi

if grep -q master .git/config; then
	echo "Using master"
		git push -u origin master
fi

echo "################################################################"
echo "###################    Git Push Done      ######################"
echo "################################################################"
