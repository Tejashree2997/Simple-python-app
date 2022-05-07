#!/bin/bash

echo "Hello world..!"
Custname='Prashant'
Environment='Production'
Region='Central India'
Address_Space='192.168.0.0/27'
Mongo_Subnet='192.168.0.1/28'
RelID_Subnet='192.168.0.13/28'

echo $n Enter Customer name: $Custname

echo $n Enter Environment Dev/Prod: $Environment

echo $n Enter Region: $Region

echo $n Address_Space: $Address_Space

echo $n Mongo_Subnet: $Mongo_Subnet

echo $n Rel-ID_Subnet: $RelID_Subnet

echo "Starting Deployment Process with $Custname $Environment $Region "

PackerName=$Custname-$Environment
