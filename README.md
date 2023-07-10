# Millicar O-Ran Integration

This project includes an e2e setup and integration of [Millicar ns3 module](https://github.com/signetlabdei/millicar) with [OpenRAN](https://openrangym.com/) architecture.
It contains the deployment of [OpenRAN ns3 module](https://openrangym.com/tutorials/ns-o-ran) architecture, the adopted [Millicar ns3 module](https://github.com/signetlabdei/millicar) to be interfaced with OpenRAN and the simulation script. 

To run the project:
- Install the [ns3 packages](https://www.nsnam.org/wiki/Installation) needed to run ns3. 
- Configure & build [ns3-mmwave-millicar](https://github.com/fgjeci/ns3-mmwave-millicar)
```
cd ../ns3-mmwave-millicar
./ns3 configure --build-profile=debug --disable-werror --enable-examples
./ns3 build
```
- Import docker images and setup docker containers of [OpenRAN RIC](https://github.com/fgjeci/colosseum-near-rt-ric-2)
```
cd ../colosseum-near-rt-ric-2/setup-scripts
./import-wines-images.sh
./setup-ric-bronze.sh
```
- Create & install the shared library [e2sim](https://github.com/fgjeci/oran-e2sim) (E2-interface connecting ns3-module with OpenRAN-RIC via SCTP/IP)
```
cd ../oran-e2sim/e2sim
./build_e2sim.sh
```
- Setup the xApp container
```
cd ../millicar-xapp/setup-scripts
./setup-xapp-base.sh # Downloads & install the base image with the updated needed libraries
./start-millicar-xapp-ns-o-ran.sh # Creates a secondary image with the python scripts of the logic
# if outside the xapp container, access bash mode of the container -> docker exec -it millicar-xapp-24 bash
# Once inside the xapp container, go to /home/xapp-sm-connector directory
cd /home/xapp-sm-connector
./ric_message_sl.sh # ***** Run 2 times to create the shared library which encodes the E2 RIC control messages
./ric_message_sl.sh # ***** Run 2 times to create the shared library which encodes the E2 RIC control messages
```
Following the aforementioned steps, the xApp is configured to receive E2 messages, decode the xml format of the these messages and send back E2-Ric encoded messages.

## Simulation steps
The simulation involves these steps:
1. Starting the xApp Agent in the xApp container: It starts the SCTP/IP server and binds to local address and accepts connection from the RIC
2. Starting the ns3 simulation instances: Inside the ns3 it is started the ns3-E2-Termination endpoint, which connects ns3 to RIC via SCTP/IP. This simulation instance waits for Subscription Requests coming from RIC to start sending reports to the xApp.
3. Starting RIC-E2-endpoint: The end point responsible to decode the incoming E2 messages, route them to the appropriate xApp and maintain the Service Model paradigm.

It is crucial to execute the steps as shown above: ns3 simulation instances (2) before the RIC-E2-endpoint(3), so that the ns3-E2-Termination endpoint can received and decode the Subscribe Requests generated by the RIC-E2-endpoint; start xApp-Agent (1) before the RIC-E2-endpoint, as the last opens a TCP/IP socket connection to the xApp and if xApp has not started and bind to the receiving address, the RIC won't be able to forward the incoming control messages

### Commands
1. Start xApp-Aggent
```
# Enter inside xApp container
docker exec -it millicar-xapp-24 bash
cd /home/millicar-xapp
python3 run_xapp_multi_sim.py
```
2. Starting ns3 simulation instances
```
cd ../millicar-oran-integration
python millicar_load.py # Launches multiple processes in parallel, one per each simulation scenario
```
3. Starting RIC-E2-endpoint
```
docker exec -it millicar-xapp-24 bash
cd /home/xapp-sm-connector
./run_xapp.sh
```
