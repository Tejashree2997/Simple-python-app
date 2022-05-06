
echo $n Enter Customer name: $c
read $name
#sed -i "/$Custname/" "$filename"
echo $n Enter Environment Dev/Prod: $c
read $envtype
#sed -i "/$Envname/" "$filename"
echo $n Enter Region: $c
read $Region
#sed -i "s/Central India/$Regionname/" "$filename"
#echo "Starting Deployment Process with $Custname $Envname $Regionname "
#PackerName=${Custname}"-"${Envname}
#sed -i "s/myPackerImage_15-11-2021-v3/${PackerName}_$(date +%d-%m-%Y)-v3/" "$filename"
#cd /home/azureuser/amit/relid-saas/Packer/Ops_Full_Build_Setup/
#source=variables.json
#sed -i "s/myPackerImage_200827-v2/${PackerName}_$(date +%d-%m-%Y)-v3/" "$source"
#sed -i "s/Central India/$Regionname/" "$source"
