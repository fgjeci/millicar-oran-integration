# Millicar O-Ran Integration

This project includes an e2e setup and integration of [Millicar ns3 module](https://github.com/signetlabdei/millicar) with [OpenRAN](https://openrangym.com/) architecture.
It contains the deployment of [OpenRAN ns3 module](https://openrangym.com/tutorials/ns-o-ran) architecture, the adopted [Millicar ns3 module](https://github.com/signetlabdei/millicar) to be interfaced with OpenRAN and the simulation script. 

To run the project:
- Install the [ns3 packages](https://www.nsnam.org/wiki/Installation) needed to run ns3. 
- Configure & build ns3-mmwave-millicar
```
cd ../ns3-mmwave-millicar
./ns3 configure --build-profile=debug --disable-werror --enable-examples
./ns3 build
```
- Import docker images and setup docker containers of [OpenRAN RIC](https://openrangym.com/tutorials/ns-o-ran)
```
cd ../colosseum-near-rt-ric-2/setup-scripts
./import-wines-images.sh
./setup-ric-bronze.sh
```
- Create & install the shared library e2sim (Connects ns3-module with OpenRAN-RIC via SCTP/IP)
```
cd ../oran-e2sim/e2sim
./build_e2sim.sh
```
- Setup the xApp container
```
cd ../millicar-xapp/setup-scripts
./setup-xapp-base.sh # Downloads & install the base image with the updated needed libraries
./start-millicar-xapp-ns-o-ran.sh # Creates a secondary image with the python scripts of the logic
```



