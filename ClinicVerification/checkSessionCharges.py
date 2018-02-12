# DraganKov 2/9/2018
import os
from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import pandas as pd

####CREATE LISTS
seshList = []  # list of unique patient ID's
oliList = []  # list of unique clinic ID's
regInfos = []
nonZeroRegInfos = []
regIds = []
oliDCAList = []
threeSessionRegIds = []
flaggedOlis = []
olisForRegId = []

class sessionItem:
    def __init__(self, seshId, regId, created, orgId):
        self.seshId = seshId
        self.regId = regId
        self.created = created
        self.orgId = orgId

class orderLineItem:
    def __init__(self, OLId, created, cost, orgId, SKU, regId):
        self.OLId = OLId
        self.created = created
        self.cost = cost
        self.orgId = orgId
        self.SKU = SKU
        self.regId = regId

class oliRegInfo:
    def __init__(self, regId, OLId):
        self.regId = regId
        self.OLId = OLId

class checkSessionCharges():
    def prepForSession(self):
        global seshdf, OLIdf
        sessionfile = '/Users/student2/Desktop/2_646_Sessions.xlsx'
        orderLineItemFile = '/Users/student2/Desktop/2_646_OrderLineItems.xlsx'
        seshdf = pd.read_excel(sessionfile, header=None, skiprows=7)
        OLIdf = pd.read_excel(orderLineItemFile, header=None, skiprows=7)
        print("READ SUCCESS")

    def populateLists(self):
        h = 1
        for h in range(len(seshdf.index)):
            seshList.append(sessionItem(seshdf.iloc[h, 0], seshdf.iloc[h, 2], seshdf.iloc[h, 16], seshdf.iloc[h, 20]))
        h = 1  # indexer
        for h in range(len(OLIdf.index)):  # for each line in the spreadsheet
            oliList.append(
                orderLineItem(OLIdf.iloc[h, 0], OLIdf.iloc[h, 17], OLIdf.iloc[h, 3], OLIdf.iloc[h, 21],
                              OLIdf.iloc[h, 6],
                              OLIdf.iloc[h, 12]))

    def prepOLIDCAList(self):

        for q in range(len(oliList)):
            if 'DCA' in oliList[q].SKU:
                oliDCAList.append(oliList[q])

        p = 0
        for p in range(len(oliDCAList)):
            x = oliRegInfo(oliDCAList[p].regId, oliDCAList[p].OLId)
            regInfos.append(x)

    # populate nonZeroRegInfos with elements from regInfos with reg with regId != 0
    def populateNonZeros(self):
        global nonZeroRegInfos, q

        q = 0
        for q in range(len(regInfos)):
            if regInfos[q].regId != '0':
                nonZeroRegInfos.append(regInfos[q])
                # print(nonZeroRegInfos[q-1].regId)

    def populateRegIDs(self):
        global regIds, q, x
        # populate regIds with nonZeroRegInfos, no duplicate ids allowed

        regIds.append(nonZeroRegInfos[0].regId)
        for q in range(len(nonZeroRegInfos)):
            uCount = 0
            tempId = nonZeroRegInfos[q].regId

            for x in range(len(regIds)):

                if tempId != regIds[x]:
                    uCount += 1
                    if uCount >= len(regIds):
                        regIds.append(nonZeroRegInfos[q].regId)

    def checkSessionCompletion(self):
        global x, threeSessionRegIds
        x = 0

        for x in range(len(regIds)):
            completedSessions = 0
            i = 0
            for i in range(len(seshList)):
                if seshList[i].regId == regIds[x]:
                    completedSessions += 1

                    if completedSessions == 3:
                        threeSessionRegIds.append(regIds[x])

    def flagOlis(self):
        global flaggedOlis, x, q

        x = 0
        for x in range(len(threeSessionRegIds)):

            q = 1
            for q in range(len(oliList)):

                if oliList[q].regId == threeSessionRegIds[x]:
                    olisForRegId.append(oliList[q])

            if len(olisForRegId) > 1:
                flaggedOlis.append(olisForRegId[0])

    def outputData(self):

        #clean up any preexisting files before operation
        try:
            os.remove("OrderLineItemsMoreThanThreeSessionRegIds.xlsx")
        except OSError:
            pass

        outputfilename = "OrderLineItemsMoreThanThreeSessionRegIds.xlsx"
        outputdf = pd.DataFrame(columns=['OLId', 'created', 'cost', 'orgId', 'SKU', 'regId'])
        for u in range(len(flaggedOlis)):
            # append each item to df
            outputdf = outputdf.append({"OLId": flaggedOlis[u].OLId, 'created': flaggedOlis[u].created,
                                        'cost': flaggedOlis[u].cost, 'orgId': flaggedOlis[u].orgId,
                                        'SKU': flaggedOlis[u].SKU, 'regId': flaggedOlis[u].regId}, ignore_index=True)
        writer = pd.ExcelWriter(outputfilename, engine='xlsxwriter')
        outputdf.to_excel(writer, index=False)
        writer.save()
        print("WRITE SUCCESS")

    def verifySessionCharges(self):
        self.prepForSession()
        self.populateLists()
        self.prepOLIDCAList()
        self.populateNonZeros()
        self.populateRegIDs()
        self.checkSessionCompletion()
        self.flagOlis()
        self.outputData()