# How to setup OpanLane Setup for ASIC

## Installation
Follow the instruction on the below markdown file to acces the ASIC files in your macine
[OpenLane](https://github.com/The-OpenROAD-Project/OpenLane/blob/master/README.md)

## Asic Flow Commands
Run the following commands in your command-line prompt:

```sh
cd openlane
make mount
```
Name your Folder in `your_folder_name`
```sh
./flow.tcl -design your_folder_name -add_to_designs -init_design_config
```

```sh
cd designs
cd dff_ram_4x72
```
Set the Config file according to your design
```sh
vi config.json	
```

```sh
cd src
```
Create a file and name your file 
```sh
touch file.v
```
### If you want to run directly, run the following commands
```sh
./flow.tcl -design your_file_name -tag tag_name
```
If above command is not working use the below command. Give the path.
```sh
/openlane/flow.tcl -design your_file_name -tag tag_name
```
use `-overwrite` to run again
```sh
/openlane/flow.tcl -design file_name -tag tag_name -overwrite
```
### If you want to run Step by step, run the following commands
```sh
/openlane/flow.tcl -design file_name -tag tag_name -interactive -overwrite
```

```sh
run_synthesis
```
```sh
run_floorplan
```
```sh
run_placement
```
```sh
run_cts
```
```sh
run_routing
```
```sh
run_magic
```
```sh
run_rc
```
