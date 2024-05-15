# From the node you wish to join to this cluster, run the following:
microk8s join 192.168.244.131:25000/321ee67f4e009e1b9548ed86e9fdbe5d/b3f7897c8fc7

# Use the '--worker' flag to join a node as a worker not running the control plane, eg:
microk8s join 192.168.244.131:25000/321ee67f4e009e1b9548ed86e9fdbe5d/b3f7897c8fc7 --worker

#If the node you are adding is not reachable through the default interface you can use one of the following:
microk8s join 192.168.244.131:25000/321ee67f4e009e1b9548ed86e9fdbe5d/b3f7897c8fc7
microk8s join 192.168.28.128:25000/321ee67f4e009e1b9548ed86e9fdbe5d/b3f7897c8fc7
microk8s join 172.17.0.1:25000/321ee67f4e009e1b9548ed86e9fdbe5d/b3f7897c8fc7

# Final
microk8s join 192.168.28.128:25000/321ee67f4e009e1b9548ed86e9fdbe5d/b3f7897c8fc7 --worker