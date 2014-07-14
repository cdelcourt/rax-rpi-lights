![](http://img.photobucket.com/albums/v234/Anode/rackspacecloudpi_zpsf51fe63d.jpg)

**Preface:**

Hi! This is a basic script that I’ve created for people to be able to monitor their Rackspace Cloud servers via the Rackspace Cloud API which can then change states of the GPIO on the Raspberry Pi.

What could you use this for? You could connect LEDs to the pins on the RPi to make a Red-Amber-Green status, or you could go a bit further and connect some relays to a proper traffic light to get a much larger version of the same thing for the status of your Rackspace Cloud server(s). You could even modify the script to sound an alarm with a buzzer connected to one of the pin outputs.. I'm currently using one of these boards to test everything out:

http://www.rapidonline.com/Electronic-Components/Pi-O-Raspberry-Pi-Input-Output-Board-73-5230

The only limit is your imagination! Modify the script, rip it apart, make it do what you want - just have fun with it :)

**Ingredients:**

Cloud server hosted with Rackspace!

Raspberry Pi w/ LEDs connected to the GPIO pins

**Method:**

Install the Cloud Monitoring Agent on your server:

http://www.rackspace.com/knowledge_center/article/install-the-cloud-monitoring-agent

Once the package is installed, run the following command to do the initial setup:

```
sudo rackspace-monitoring-agent --setup
```

It will ask for your username (the one you use to log into the Cloud Control Panel with) and your API key, which can be found via the 'Account Settings' section of the Cloud Control Panel by clicking your username up the top-right when logged in to the CCP.

Make sure you start the service once it's been installed:

```
[root@lon-raxmon-01 ~]# service rackspace-monitoring-agent start
Starting /usr/bin/rackspace-monitoring-agent:              [  OK  ]
```

Take the Raspberry Pi (or other device) that you want to use to monitor and then:

Install python-pip and python if you haven't already. This script runs on Python2 for reference.

```
refx@peach:~$ sudo apt-get install python-pip python
```

Install any dependancies if needed.

Install the **rackspace-monitoring-cli**  module for python as per the instructions on the Rackspace Knowledge Center:

http://www.rackspace.com/knowledge_center/article/getting-started-with-rackspace-monitoring-cli

```
refx@peach:~$ sudo pip install rackspace-monitoring-cli
Downloading/unpacking rackspace-monitoring-cli
  Downloading rackspace-monitoring-cli-0.6.2.tar.gz (155Kb): 155Kb downloaded
  Running setup.py egg_info for package rackspace-monitoring-cli
    
Downloading/unpacking rackspace-monitoring>=0.6.0 (from rackspace-monitoring-cli)
  Downloading rackspace-monitoring-0.6.0.tar.gz
  Running setup.py egg_info for package rackspace-monitoring
    
Downloading/unpacking apache-libcloud>=0.12.4,<=0.13 (from rackspace-monitoring>=0.6.0->rackspace-monitoring-cli)
  Downloading apache-libcloud-0.13.0.tar.bz2 (395Kb): 395Kb downloaded
  Running setup.py egg_info for package apache-libcloud
    
Installing collected packages: rackspace-monitoring-cli, rackspace-monitoring, apache-libcloud
  Running setup.py install for rackspace-monitoring-cli
    changing mode of build/scripts-2.7/raxmon-monitoring-zones-list from 644 to 755
    changing mode of build/scripts-2.7/raxmon-checks-delete from 644 to 755

    <SNIP> omitting all of the output because it was hooge.

    changing mode of /usr/local/bin/raxmon-entities-update to 755
  Running setup.py install for rackspace-monitoring
    
  Running setup.py install for apache-libcloud
    
Successfully installed rackspace-monitoring-cli rackspace-monitoring apache-libcloud
Cleaning up...
refx@peach:~$ 
```

Once this is done, you can verify it working by running raxmon-agents-list to see if it's talking to your account correctly.

If you get this, it may be due to having no agents installed and working on your servers:

```
refx@peach:~$ raxmon-agents-list
[]
```

This is what you should see if you get a response:

```
refx@peach:~$ raxmon-agents-list
<Agent: id=xxxx9051-xxxx-xxxx-xxxx-d9d6a67134ae, last_connected=1395515533003>

Total: 1
```

Add some alerts to the system and use the following command to get the state of your overall environment

```
refx@peach:~$ raxmon-views-overview
[{'alarms': [], 'latest_alarm_states': [], 'checks': [], 'entity': <Entity: id=enFXXXA4A1 label=lon-webirc-01 provider=Rackspace Monitoring ...>}, {'alarms': [], 'latest_alarm_states': [], 'checks': [], 'entity': <Entity: id=enXXXKC0Ox label=lon-learn-01 provider=Rackspace Monitoring ...>}, {'alarms': [<Alarm: id=alXXXxzM6C, label=CPU Usage ...>, <Alarm: id=alYXXXja8l, label=Connection time ...>, <Alarm: id=aluaXXX7YB, label=Status code ...>], 'latest_alarm_states': [<**LatestAlarmState: entity_id=enrXXXBckj, check_id=ch1XXXlmXa, alarm_id=alXXXxzM6C, state=CRITICAL** ...>, <LatestAlarmState: entity_id=enrXXXBckj, check_id=chNXXXriop, alarm_id=alYAXXXa8l, state=OK ...>, <LatestAlarmState: entity_id=enrXXXBckj, check_id=chNXXXriop, alarm_id=aluaXXX7YB, state=OK ...>], 'checks': [<Check: id=ch1XXXlmXa label=CPU...>, <Check: id=chNXXXriop label=Avocado Monitorix...>], 'entity': <Entity: id=enrXXXBckj label=lon-raxmon-01 provider=Rackspace Monitoring ...>}, {'alarms': [], 'latest_alarm_states': [], 'checks': [], 'entity': <Entity: id=enuXXXO17R label=lon-learn-02 provider=Rackspace Monitoring ...>}]
```

If this returns an output like the above, then you should be good to go! Please contact me if you’ve got any issues with the above.

~cdelcourt
