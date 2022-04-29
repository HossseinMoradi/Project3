import math
import ast
from math import e
from decimal import *
import time
import random



getcontext().prec = 28


# first we have defined functions to access signals and vehicles data

def toList(NestedTuple):
    return list(map(toList, NestedTuple)) if isinstance(NestedTuple, (list, tuple)) else NestedTuple

# we want to access vehicles information. In the first part of the below function, we determine the pieces of data that are collected. In the secoond part we determine that which types of vehicles are CV/special (i.e, sending information) 
def GetVissimDataVehicles():
    global vehsAttributes
    global vehsAttNames
    vehsAttributesNames = ['No', 'VehType\No', 'Pos', 'VehType\No', 'Lane\Link', 'Speed', 'DistanceToSigHead','InQueue']
    vehsAttributes = toList(Vissim.Net.Vehicles.GetMultipleAttributes(vehsAttributesNames))
    vehsAttNames = {}
    cnt = 0
    for att in vehsAttributesNames:
        vehsAttNames.update({att: cnt})
        cnt += 1
    global vehTypesEquipped
    global vehTypesSpecial
    vehTypesAttributes = Vissim.Net.VehicleTypes.GetMultipleAttributes(['No', 'IsCV', 'IsSpecial'])
    vehTypesEquipped = [x[0] for x in vehTypesAttributes if x[1] == True]
    vehTypesSpecial = [x[0] for x in vehTypesAttributes if x[2] == True]









def Signal():
    #we define a user attributre to access SimSec
    Vissim.Net.SignalControllers.ItemByKey(1).SetAttValue('SimSec',Vissim.Net.Simulation.SimulationSecond)
    Seconds = Vissim.Net.SignalControllers.ItemByKey(1).AttValue('CycSec')
    SimSec = Vissim.Net.SignalControllers.ItemByKey(1).AttValue('SimSec')
    CLength = 60
    GetVissimDataVehicles()
    deltaT=1
    #we should correlate deltaT with the simulation resolution. In other words, number of simulation per second should be one here. 
    Starting_time=0
    Ending_time=1000
    
    TimeNo=[]
    i=Starting_time
    k=0
    while i< Ending_time:
        TimeNo.append(k)
        k+=1
        i=i+deltaT



    # The operation of our actuated signal is as follows: we start with a minimum green time. If there is a vehicles still reamining on our detectors, we add an extention time to our green time. WE also consider a maximum green time.

    MinG=5
    MaxG=35
    ExG=3
    deterctor=35
    loc=25
    for i in TimeNo:
        if SimSec > (i)*deltaT and SimSec <= (i+1)*deltaT:
            # this is anexample of a case where green time durations and cycles are varying at each time step
            if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('SigState')=='RED':
                if SimSec <= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenStart'):
                    G1=MinG
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('GreenTimeDuration', G1)                
            
            k=[]
            for vehAttributes in vehsAttributes:
                if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('SigState')=='GREEN':
                    if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenEnd')-SimSec <=3:
                        if vehAttributes[vehsAttNames['Lane\Link']] == '1':
                            DistanceToSigHead = vehAttributes[vehsAttNames['DistanceToSigHead']]
                            if DistanceToSigHead >= loc and DistanceToSigHead <= loc+deterctor and vehAttributes[vehsAttNames['No']] not in k:
                                k.append(vehAttributes[vehsAttNames['No']])
                                G1=min((Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenTimeDuration')+ExG),MaxG)                                                  
                                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('GreenTimeDuration', G1)
                continue



            if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('SigState')=='RED':
                if SimSec < Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('GreenStart'):               
                    G2=MinG
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('GreenTimeDuration', G2)
            k2=[]
            for vehAttributes in vehsAttributes:
                if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('SigState')=='GREEN':
                    if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('GreenEnd')-SimSec <=3:
                        if vehAttributes[vehsAttNames['Lane\Link']] == '8':
                            DistanceToSigHead = vehAttributes[vehsAttNames['DistanceToSigHead']]
                            if DistanceToSigHead >= loc and DistanceToSigHead <= loc+deterctor and vehAttributes[vehsAttNames['No']] not in k2:
                                k2.append(vehAttributes[vehsAttNames['No']])
                                G2=min((Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('GreenTimeDuration')+ExG),MaxG)                                                  
                                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('GreenTimeDuration', G2)
                continue



            if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('SigState')=='RED':
                if SimSec < Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenStart'):
                    G3=MinG
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('GreenTimeDuration', G3)
            k3=[]
            for vehAttributes in vehsAttributes:
                if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('SigState')=='GREEN':
                    if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenEnd')-SimSec <=3:
                        if vehAttributes[vehsAttNames['Lane\Link']] == '4':
                            DistanceToSigHead = vehAttributes[vehsAttNames['DistanceToSigHead']]
                            if DistanceToSigHead >= loc and DistanceToSigHead <= loc+deterctor and vehAttributes[vehsAttNames['No']] not in k3:
                                k3.append(vehAttributes[vehsAttNames['No']])
                                G3=min((Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenTimeDuration')+ExG),MaxG)                                                  
                                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('GreenTimeDuration', G3)
                continue

            if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('SigState')=='RED':
                if SimSec < Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('GreenStart'):
                    G4=MinG
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('GreenTimeDuration', G4)
            k4=[]
            for vehAttributes in vehsAttributes:
                if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('SigState')=='GREEN':
                    if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('GreenEnd')-SimSec <=3:
                        if vehAttributes[vehsAttNames['Lane\Link']] == '5':
                            DistanceToSigHead = vehAttributes[vehsAttNames['DistanceToSigHead']]
                            if DistanceToSigHead >= loc and DistanceToSigHead <= loc+deterctor and vehAttributes[vehsAttNames['No']] not in k4:
                                k4.append(vehAttributes[vehsAttNames['No']])
                                G4=min((Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('GreenTimeDuration')+ExG),MaxG)                                                  
                                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('GreenTimeDuration', G4)
                continue

    if SimSec >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('GreenEnd')-2:
        if SimSec <= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('GreenEnd')+2:
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('GreenStart', Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('GreenEnd')+2)
            Vissim.Net.SignalControllers.ItemByKey(1).SetAttValue('CycleStart', Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenStart')-2)
    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('GreenEnd', Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenStart') + Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenTimeDuration'))
    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenEnd') + 2)
    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('GreenEnd',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('GreenStart') + Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('GreenTimeDuration'))
    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('GreenEnd') + 2)
    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('GreenEnd',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenStart') + Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenTimeDuration'))
    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenEnd') + 2)
    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('GreenEnd',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('GreenStart') + Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('GreenTimeDuration'))




    # you have to make a use of simsec to define variable cycle time
    # To this end, we firs, define three attributes in the current signal controller with the names of CycleStart, CycleEnd, CycleDuration. 

    
    SimSec = Vissim.Net.SignalControllers.ItemByKey(1).AttValue('SimSec')
    #we determine Initial values OF CYCLE START
    if SimSec<=1:
        Vissim.Net.SignalControllers.ItemByKey(1).SetAttValue('CycleStart', 0)



    # When we start the simulation, we determine that the signals are operating upon com script.
    if SimSec<=1:

        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('ContrByCOM', True)
        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('ContrByCOM', True)
        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('ContrByCOM', True)
        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('ContrByCOM', True)
        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('GreenStart',2)



    if SimSec >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenStart') - 1:
        if SimSec <= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenEnd') - 1:
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('SigState', 'GREEN')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('SigState', 'RED')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('SigState', 'RED')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('SigState', 'RED')
        if SimSec >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenEnd') - 1:
            if SimSec < Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenEnd') + 1:
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('SigState', 'RED')
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('SigState', 'RED')
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('SigState', 'RED')
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('SigState', 'RED')

    if SimSec >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('GreenStart') - 1:
        if SimSec <= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('GreenEnd') - 1:
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('SigState', 'GREEN')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('SigState', 'RED')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('SigState', 'RED')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('SigState', 'RED')

        if SimSec >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('GreenEnd') - 1:
            if SimSec < Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('GreenEnd') + 1:
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('SigState', 'RED')
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('SigState', 'RED')
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('SigState', 'RED')
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('SigState', 'RED')

    if SimSec >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenStart') - 1:
        if SimSec <= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenEnd') - 1:
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('SigState', 'GREEN')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('SigState', 'RED')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('SigState', 'RED')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('SigState', 'RED')

        if SimSec >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenEnd') - 1:
            if SimSec < Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenEnd') + 1:
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('SigState', 'RED')
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('SigState', 'RED')
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('SigState', 'RED')
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('SigState', 'RED')

    if SimSec >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('GreenStart') - 1:
        if SimSec <= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('GreenEnd') - 1:
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('SigState', 'GREEN')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('SigState', 'RED')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('SigState', 'RED')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('SigState', 'RED')

        if SimSec >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('GreenEnd') - 1:
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('SigState', 'RED')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('SigState', 'RED')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('SigState', 'RED')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('SigState', 'RED')

