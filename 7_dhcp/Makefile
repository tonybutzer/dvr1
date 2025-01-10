cat:
	cat Makefile

install:
	sudo apt-get install isc-dhcp-server


configure:
	sudo cp ./dhcpd.conf /etc/dhcp/dhcpd.conf
	sudo service isc-dhcp-server restart
 	#sudo service isc-dhcp-server start
 	#sudo service isc-dhcp-server stop 

notes:

	echo Your /etc/default/isc-dhcp-server file should have INTERFACES="eth0"


