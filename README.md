# An hybrid framework for SCADA cyber attack dataset generation

## Table of contents
- [Project Overview](#project-overview)
- [Initial Steps](#initial-steps)
- [Architecture](#architecture)
- [Authors](#authors)

## Project Overview
...

## Initial Steps
First of all you need to download the different virtual machines. This procedure assumes you're using VirtualBox. 
See [this document](vmware-fusion.md) if you're a macOS user who prefers to use VMWare Fusion, or encounters issues using VirtualBox.

1. Download VMs:
   - [Simulation VM](https://netorgft4230013-my.sharepoint.com/:u:/g/personal/dformby_fortiphyd_com/EaBeAxbF6xtEumdsJ7npVz0BeECJnseAMsfAbaLwV3sKOg?e=JRvkcS) - MD5=02af6c2502ecaab6c6d138deb560b27d
   - [HMI VM](https://www.mattrideout.com/courses/cs6263/GRFICSv3/ScadaBR.ova) - MD5=b951f5fbd896ace762537207de913393
   - [PLC VM](https://netorgft4230013-my.sharepoint.com/:u:/g/personal/dformby_fortiphyd_com/ER0pG_X5IRNCg477jf2ppo8BdN0t13t9vrNBH92_oOWOHA?e=hNeJ88) - MD5=0fbb1254fb166466496f2a48780ae774
   - [Workstation VM](https://www.mattrideout.com/courses/cs6263/GRFICSv3/workstation.ova) - MD5=8b41ee6597404b7c9e9acf7c2b1c3866

2. Create Network:
   This procedure assumes you're using Linux.
   - Open *Wi-Fi & Network* section in System Settings
   - Click on *Add new connection*
   - Choose *Wired Ethernet (Shared)* connection
   - Rename as you like
   - In the section *Wired* > *Restrict to device* choose the MAC Address of the phisical PLC
   - Check if in the section *IPV4* > *Method* is selected *Shared to other computers*

4. 
## Architecture
