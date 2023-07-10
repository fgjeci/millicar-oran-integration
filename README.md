# Millicar O-Ran Integration

This project includes an e2e setup and integration of [Millicar ns3 module](https://github.com/signetlabdei/millicar) with [OpenRAN](https://openrangym.com/) architecture.
It contains the deployment of [OpenRAN ns3 module](https://openrangym.com/tutorials/ns-o-ran) architecture, the adopted [Millicar ns3 module](https://github.com/signetlabdei/millicar) to be interfaced with OpenRAN and the simulation script. 

To run the project:
- Install the [ns3 packages](https://www.nsnam.org/wiki/Installation) needed to run ns3. 
- Build ns3-mmwave-millicar
```
./ns3 configure --build-profile=debug --disable-werror --enable-examples
./ns3 build
```
