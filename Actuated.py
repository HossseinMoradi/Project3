import math

def factorial(f):
    if f == 0:
        return 1
    else:
        return f * factorial(f-1)

def toList(NestedTuple):
    return list(map(toList, NestedTuple)) if isinstance(NestedTuple, (list, tuple)) else NestedTuple
def Init():
    global minSpeed
    global MaxSpeed
    global MaximumNumber
    global MaximumHeadway 
    global vehTypesEquipped
    global sigTypesAttributes
    global LinkTypesAttributes
    global GV
    global EV
    global GVCAV
    global SCAV
    global LinkA
    global LinkB
    global LinkC
    global LinkD
    global SignalA
    global SignalB
    global SignalC
    global SignalD
    
    minSpeed = CurrentScript.AttValue('minSpeed')
    MaxSpeed = CurrentScript.AttValue('MaxSpeed')
    MaximumNumber = CurrentScript.AttValue('MaximumNumber')
    MaximumHeadway = CurrentScript.AttValue('MaximumHeadway')
    vehTypesAttributes = Vissim.Net.VehicleTypes.GetMultipleAttributes(['No', 'ReceiveSignalInformation','GV','EV','GVCAV','SCAV'])
    
    vehTypesEquipped = [x[0] for x in vehTypesAttributes if x[1] == True]
    GV = [x[0] for x in vehTypesAttributes if x[2] == True]
    EV = [x[0] for x in vehTypesAttributes if x[3] == True]
    GVCAV = [x[0] for x in vehTypesAttributes if x[4] == True]
    SCAV = [x[0] for x in vehTypesAttributes if x[5] == True]



    LinkTypesAttributes =  Vissim.Net.Links.GetMultipleAttributes(['No', 'LinkA', 'LinkB', 'LinkC', 'LinkD'])
    LinkA = [x[0] for x in LinkTypesAttributes if x[1] == True]
    LinkB = [x[0] for x in LinkTypesAttributes if x[2] == True]
    LinkC = [x[0] for x in LinkTypesAttributes if x[3] == True]
    LinkD = [x[0] for x in LinkTypesAttributes if x[4] == True]
    
    
    
    
    sigTypesAttributes =  Vissim.Net.SignalControllers.ItemByKey(1).SGs.GetMultipleAttributes(['No', 'SignalA', 'SignalB', 'SignalC', 'SignalD'])
    SignalA = [x[0] for x in sigTypesAttributes if x[1] == True]
    SignalB = [x[0] for x in sigTypesAttributes if x[2] == True]
    SignalC = [x[0] for x in sigTypesAttributes if x[3] == True]
    SignalD = [x[0] for x in sigTypesAttributes if x[4] == True]
    # This functions gets and updates each vehicle state at the network

def GetVissimDataVehicles():
    global vehsAttributes
    global vehsAttNames
    vehsAttributes = []
    vehsAttNames = []
    vehsAttributesNames = ['No', 'VehType\No','Speed' , 'DesSpeed', 'OrgDesSpeed', 'DistanceToSigHead', 'SpeedMaxForGreenStart', 'SpeedMinForGreenEnd', 'Acceleration', 'Lane\Link']
    vehsAttributes = toList(Vissim.Net.Vehicles.GetMultipleAttributes(vehsAttributesNames))
    vehsAttNames = {}
    cnt = 0
    for att in vehsAttributesNames:
        vehsAttNames.update({att: cnt})
        cnt += 1



# This function takes the specification of each signal
def GetSignalsData():
    global SignalAttributes
    global SigAttNames
    SignalAttributes = []
    SigAttNames = []
    SignalAttributesNames = ['No','Name', 'GreenStart', 'GreenEnd','TimeUntilNextGreen','TimeUntilNextRed', 'SignalA', 'SignalB', 'SignalC', 'SignalD','SigState', 'GreenTimeDuration' ,'LastCAVPos','SigState', 'SC\CycSec', 'Seconds']
    SignalAttributes = toList(Vissim.Net.SignalControllers.ItemByKey(1).SGs.GetMultipleAttributes(SignalAttributesNames))
    SigAttNames = {}
    ctt = 0
    for ftt in SignalAttributesNames:
        SigAttNames.update({ftt: ctt})
        ctt+=1


def GetLinksData():
    global LinkAttributes
    global LinAttNames
    LinkAttributes = []
    LinkAttributes = []
    LinkAttributesNames = ['No','LinkA', 'LinkB', 'LinkC', 'LinkD']
    LinkAttributes = toList(Vissim.Net.Links.GetMultipleAttributes(LinkAttributesNames))
    LinAttNames = {}
    ppc = 0
    for ftt in LinkAttributesNames:
        LinAttNames.update({ftt: ppc})
        ppc+=1


def GetTrafficFleetData():
    global trafficAttributes
    global traAttNames
    trafficAttributes = []
    traAttNames = []
    TrafficAttributesNames = ['VehType\No','RelFlow']
    trafficAttributes = toList(Vissim.Net.VehicleCompositions.ItemByKey(5).VehCompRelFlows.GetMultipleAttributes(TrafficAttributesNames))
    traAttNames = {}
    gtp = 0
    for ptg in TrafficAttributesNames:
        traAttNames.update({ptg: gtp})
        gtp+=1

# This calculates the number of queued up vehicles based on the Commert's formula and the corresponding green time
def NumberOfQueuedVehicles():
    GetVissimDataVehicles()
    GetTrafficFleetData()
    GetSignalsData()
    GetLinksData()

    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('Seconds',Vissim.Net.Simulation.SimulationSecond)
    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('Seconds',Vissim.Net.Simulation.SimulationSecond)
    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('Seconds',Vissim.Net.Simulation.SimulationSecond)
    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('Seconds',Vissim.Net.Simulation.SimulationSecond)
    C = []
    B = []
    A = []
    D = []

    for sig in SignalAttributes:
            if  sig[SigAttNames['No']] ==3 and sig[SigAttNames['SigState']] !='Red':  
                for vehAttributes in vehsAttributes:
                    Link = vehAttributes[vehsAttNames['Lane\Link']]
                    DistanceToSigHead = vehAttributes[vehsAttNames['DistanceToSigHead']]
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('LinkNo',Link)
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('LinkNo',Link)
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('LinkNo',Link)
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('LinkNo',Link)
                    if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('LinkNo')==5:
                        if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('Seconds') > Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('GreenStart')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('GreenTimeDuration')-3:
                            if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('Seconds') <= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('GreenStart')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('GreenTimeDuration')-2:
                                if vehAttributes[vehsAttNames['DistanceToSigHead']] <=30 and vehAttributes[vehsAttNames['DistanceToSigHead']] >= 10:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('GreenTimeDuration',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenTimeDuration')+2)
                                    if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenTimeDuration')>=25:
                                        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('GreenTimeDuration',25)
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('GreenEnd',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('GreenTimeDuration')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('GreenStart'))         
                if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('Seconds') >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('GreenEnd'):
                    if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('Seconds') < Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('GreenEnd')+2:
                        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('SigState','Red')
                        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('GreenEnd')+4)
                        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('GreenEnd')+4)
                        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('GreenEnd')+4)      
                if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('Seconds') >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('GreenEnd')+4:                   
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('SigState','Green')
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('SigState','Red')
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('SigState','Red')
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('SigState','Red')
                    if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('Seconds') < Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('GreenEnd')+5:
                        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('GreenTimeDuration',7)
                        
                
                
            if  sig[SigAttNames['No']] ==6 and sig[SigAttNames['SigState']] !='Red':
                for vehAttributes in vehsAttributes:
                    Link = vehAttributes[vehsAttNames['Lane\Link']]
                    DistanceToSigHead = vehAttributes[vehsAttNames['DistanceToSigHead']]
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('LinkNo',Link)
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('LinkNo',Link)
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('LinkNo',Link)
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('LinkNo',Link)
                    if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('LinkNo')==7:
                        if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('Seconds') > Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('GreenStart')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('GreenTimeDuration')-3:
                            if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('Seconds') <= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('GreenStart')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('GreenTimeDuration')-2:
                                if vehAttributes[vehsAttNames['DistanceToSigHead']] <=30 and vehAttributes[vehsAttNames['DistanceToSigHead']] >= 10:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('GreenTimeDuration',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue('GreenTimeDuration')+2)
                                    if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue('GreenTimeDuration')>=25:
                                        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('GreenTimeDuration',25)
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('GreenEnd',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('GreenTimeDuration')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('GreenStart'))
                if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('Seconds') >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('GreenEnd'):
                    if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('Seconds') < Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('GreenEnd')+2:
                        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('SigState','Red')
                        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('GreenEnd')+4)
                        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('GreenEnd')+4)
                        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('GreenEnd')+4)
                if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('Seconds') >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('GreenEnd')+4:
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('SigState','Green')
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('SigState','Red')
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('SigState','Red')
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('SigState','Red')
                    if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('Seconds') < Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('GreenEnd')+5:
                        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('GreenTimeDuration',7)
                        

               
 



            if  sig[SigAttNames['No']] ==9 and sig[SigAttNames['SigState']] !='Red':
                for vehAttributes in vehsAttributes:
                    Link = vehAttributes[vehsAttNames['Lane\Link']]
                    DistanceToSigHead = vehAttributes[vehsAttNames['DistanceToSigHead']]
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('LinkNo',Link)
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('LinkNo',Link)
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('LinkNo',Link)
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('LinkNo',Link)
                    if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('LinkNo')==1:
                        if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('Seconds') >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('GreenStart')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('GreenTimeDuration')-3:
                            if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('Seconds') <= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('GreenStart')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('GreenTimeDuration')-2:
                                if vehAttributes[vehsAttNames['DistanceToSigHead']] <=30 and vehAttributes[vehsAttNames['DistanceToSigHead']] >= 10:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('GreenTimeDuration',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue('GreenTimeDuration')+2)
                                    if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue('GreenTimeDuration')>=25:
                                        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('GreenTimeDuration',25)



                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('GreenEnd',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('GreenTimeDuration')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('GreenStart'))
                if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('Seconds') >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('GreenEnd'):
                    if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('Seconds') < Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('GreenEnd')+2:
                        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('SigState','Red')
                        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('GreenEnd')+4)
                        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('GreenEnd')+4)
                        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('GreenEnd')+4)
                if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('Seconds') >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('GreenEnd')+4:
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('SigState','Green')
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('SigState','Red')
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('SigState','Red')
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('SigState','Red')
                    if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('Seconds') < Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('GreenEnd')+5:
                            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('GreenTimeDuration',7)

                        


            if  sig[SigAttNames['No']] ==12 and sig[SigAttNames['SigState']] !='Red':
                for vehAttributes in vehsAttributes:
                    Link = vehAttributes[vehsAttNames['Lane\Link']]
                    DistanceToSigHead = vehAttributes[vehsAttNames['DistanceToSigHead']]
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('LinkNo',Link)
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('LinkNo',Link)
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('LinkNo',Link)
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('LinkNo',Link)
                    if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('LinkNo')==3:
                        if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('Seconds') > Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('GreenStart')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('GreenTimeDuration')-3:
                            if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('Seconds') <= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('GreenStart')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('GreenTimeDuration')-2:
                                if vehAttributes[vehsAttNames['DistanceToSigHead']] <=30 and vehAttributes[vehsAttNames['DistanceToSigHead']] >= 10:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('GreenTimeDuration',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue('GreenTimeDuration')+2)
                                    if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue('GreenTimeDuration')>=25:
                                        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('GreenTimeDuration',25)


                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('GreenEnd',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('GreenTimeDuration')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('GreenStart'))

                if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('Seconds') >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('GreenEnd'):
                    if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('Seconds') < Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('GreenEnd')+2:
                        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('SigState','Red')
                        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('GreenEnd')+4)
                        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('GreenEnd')+4)
                        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('GreenEnd')+4)
                if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('Seconds') >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('GreenEnd')+4:
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('SigState','Green')
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('SigState','Red')
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('SigState','Red')
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('SigState','Red')
                    if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('Seconds') < Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('GreenEnd')+5:
                        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('GreenTimeDuration',7)


 


                
