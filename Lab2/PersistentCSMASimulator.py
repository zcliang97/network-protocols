from __future__ import division
from Node import Node

SIMULATION_TIME = 1000 # 1000s

TRANSMISSION_RATE = 1000000 # 1 Mbps
PACKET_LENGTH = 1500 # assume all packets are the same length
TRANSMISSION_DELAY = PACKET_LENGTH / TRANSMISSION_RATE

DISTANCE_BETWEEN_NODES = 10
PROPAGATION_SPEED = (2/3) * 300000000
UNIT_PROPAGATION_DELAY = DISTANCE_BETWEEN_NODES / PROPAGATION_SPEED

class PersistentCSMASimulator:
    def __init__(self, numNodes, avgPacketArrivalRate):
        self.nodes = []

        self.numNodes = numNodes
        self.avgPacketArrivalRate = avgPacketArrivalRate

        # metrics
        self.transmittedPackets = 0
        self.successfullyTransmittedPackets = 0

    def run(self):
        self.createNodes()
        self.processPackets()
        self.printResults()

    def createNodes(self):
        for i in range(self.numNodes):
            self.nodes.append(Node(i, self.avgPacketArrivalRate, SIMULATION_TIME))

    def processPackets(self):
        currentTime = 0
        while True:
            # get the sender node which has the smallest packet arrival time
            txNode = min(self.nodes, key=lambda node: node.getFirstPacketTimestamp())
            if not txNode.queue:
                break

            # update the currentTime
            currentTime = txNode.getFirstPacketTimestamp()

            self.transmittedPackets += 1

            # For each node, calculate when the packet arrives + check collision
            transmissionSuccess = True
            for rxNode in self.nodes:
                offset = abs(rxNode.getNodePosition() - txNode.getNodePosition())
                if (offset == 0):
                    continue
                
                firstBitArrivalTime = currentTime + (offset * UNIT_PROPAGATION_DELAY)
                lastBitArrivalTime = firstBitArrivalTime + TRANSMISSION_DELAY

                # Carrier Sensing and if not busy check for collisions
                if rxNode.checkIfBusy(firstBitArrivalTime, lastBitArrivalTime):
                    rxNode.bufferPackets(firstBitArrivalTime, lastBitArrivalTime)
                elif rxNode.checkCollision(firstBitArrivalTime):
                    rxNode.waitExponentialBackoff()
                    self.transmittedPackets += 1
                    transmissionSuccess = False

            if not transmissionSuccess:
                txNode.waitExponentialBackoff()
            else:
                # self.transmittedPackets += 1 <- This gave good numbers. But doesnt make sense in code
                self.successfullyTransmittedPackets += 1
                txNode.removeFirstPacket()

    def getNumPacketsDropped(self):
        return sum(node.packets_dropped for node in self.nodes)

    def getTotalNumPackets(self):
        return sum(node.generated_packets for node in self.nodes)

    def printResults(self):
        print("================ RESULTS ================")
        print("Arrival Rate: %f, NumNodes: %f", self.avgPacketArrivalRate, self.numNodes)
        print("SuccessFully Transmitted Packets: {}".format(self.successfullyTransmittedPackets))
        print("Total Packets Dropped: {}".format(self.getNumPacketsDropped()))
        print("Total Generated Packets: {}".format(self.getTotalNumPackets()))
        print("Total Transmitted Packets: {}".format(self.transmittedPackets))
        print("Efficiency of CSMA/CD: {}".format((self.successfullyTransmittedPackets / self.transmittedPackets)))
        print("Throughput of CSMA/CD: {} Mbps".format(((self.successfullyTransmittedPackets * PACKET_LENGTH / 1000000) / SIMULATION_TIME)))
