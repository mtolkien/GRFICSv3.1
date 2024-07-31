# An hybrid framework for SCADA cyber attack dataset generation

## Table of contents
- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Initial Steps](#initial-steps)
- [Authors](#authors)

## Project Overview
...

## Architecture
The architecture of this project represents a simulation of an Industrial Control System consisting of the following virtual machines:  
- **ChemicalPlant**: runs a realistic simulation of a chemical plant that is controlled and monitored by simulated remote IO devices. These remote IO devices are monitored and controlled by the PLC;
- **plc_2**: represents the PLC and responds to Modbus/TCP requests;
- **ScadaBR**: represents a Human Machine Interface (HMI), used to monitor process measurements collected by the PLC and to send commands to the PLC;
- **Workstation**: virtual machine with software used for programming the OpenPLC
  
In addition to this section consisting of virtual machines, was also added a physical PLC from Siemens (specifically the LOGO! 24V model).


## Initial Steps
First of all you need to download the different virtual machines. This procedure assumes you're using VirtualBox.  
See [this document](vmware-fusion.md) if you're a macOS user who prefers to use VMWare Fusion, or encounters issues using VirtualBox.

1. **Download VMs**:
   - [Simulation VM](https://netorgft4230013-my.sharepoint.com/:u:/g/personal/dformby_fortiphyd_com/EaBeAxbF6xtEumdsJ7npVz0BeECJnseAMsfAbaLwV3sKOg?e=JRvkcS) - MD5=02af6c2502ecaab6c6d138deb560b27d
   - [HMI VM](https://www.mattrideout.com/courses/cs6263/GRFICSv3/ScadaBR.ova) - MD5=b951f5fbd896ace762537207de913393
   - [PLC VM](https://netorgft4230013-my.sharepoint.com/:u:/g/personal/dformby_fortiphyd_com/ER0pG_X5IRNCg477jf2ppo8BdN0t13t9vrNBH92_oOWOHA?e=hNeJ88) - MD5=0fbb1254fb166466496f2a48780ae774
   - [Workstation VM](https://www.mattrideout.com/courses/cs6263/GRFICSv3/workstation.ova) - MD5=8b41ee6597404b7c9e9acf7c2b1c3866

2. **Create Network**:  
   This procedure assumes you're using Linux.
   - Open *Wi-Fi & Network* section in System Settings
   - Click on *Add new connection*
   - Choose *Wired Ethernet (Shared)* connection
   - Rename as you like
   - In the section *Wired* > *Restrict to device* choose the MAC Address of the phisical PLC
   - Check if in the section *IPV4* > *Method* is selected *Shared to other computers*

3. **Configuration of the physical plc**  
   

5.  
## Architecture
