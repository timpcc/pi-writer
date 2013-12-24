#! /bin/sh

sudo apt-get install python-pip
sudo apt-get install python-requests


echo Making 'typesetter.py' executable
sudo chmod +x typesetter.py

echo Making 'pi-writer.py' executable
sudo chmod +x pi-writer.py

echo Making 'pi-writer-shutdown.sh' executable
sudo chmod +x pi-writer-shutdown.sh

echo Making symbolic link for pi-writer
sudo ln -s /home/pi/pi-writer/pi-writer.py /usr/bin/pi-writer

echo Making symbolic link for typesetter
sudo ln -s /home/pi/pi-writer/typesetter.py /usr/bin/typesetter

echo Making symbolic link for 'shutdown' in init.d
sudo ln -s /home/pi/pi-writer/shutdown /etc/init.d/pi-writer-shutdown

echo Setting up rc.d scripts
sudo update-rc.d pi-writer-shutdown start 20 0 6 .

echo Backing up lightdm.conf
sudo cp /etc/lightdm/lightdm.conf /etc/lightdm/lightdm.conf.old

echo Now change the 'session-setup-script' entry to be '/home/pi/start-writer.sh'
sudo leafpad /etc/lightdm/lightdm.conf