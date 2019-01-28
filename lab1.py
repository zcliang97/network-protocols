import numpy as np
from DiscreteEventSimulator import DiscreteEventSimulator
from DiscreteEventBufferSimulator import DiscreteEventBufferSimulator
import time

def generateGraph(lines, p_loss):
    # for (x, y) in lines:
    #     plt.plot(x, y)
    # plt.show()
    print lines
    print p_loss

def question_3():
    rho_values = np.arange(0.25, 1.05, 0.1)
    for rho in rho_values:
        print(" --- Rho Value: %s --- " % rho)
        # Run simulator Passing in events and packets
        simulator = DiscreteEventSimulator(rho).run()

def question_4():
    # Run simulator Passing in events and packets
    rho = 1.2
    print(" --- Rho Value: %s --- " % rho)
    simulator = DiscreteEventSimulator(rho).run()

def question_6():
    lines = []
    packet_loss = []
    buffer_lengths = [10, 25, 50]
    rho_values = np.arange(0.5, 1.6, 0.1)
    for length in buffer_lengths:
        x, y, ploss = [], [], []
        for rho in rho_values:
            print " --- Buffer Length: {length}, Rho Value: {rho} --- ".format(length=length, rho=rho)
            avgPacketsInQueue, packetLoss = DiscreteEventBufferSimulator(rho, length).run()
            print("--- %s seconds to run range ---" % (time.time() - start_time))
            x.append(rho)
            y.append(avgPacketsInQueue)
	    ploss.append(packetLoss)
        lines.append((x, y))
        packet_loss.append(ploss)
    
    generateGraph(lines, packet_loss)

# main
question_number = raw_input("Enter Question Number [3, 4, 6] ")
question_number = int(question_number)

start_time = time.time()

if question_number == 3:
    question_3()
elif question_number == 4:
    question_4()
elif question_number == 6:
    question_6()
