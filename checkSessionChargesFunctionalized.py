
# coding: utf-8

# In[2]:


# DraganKov 2/9/2018

from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import pandas as pd

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

sessionfile = '/Users/student2/Desktop/2-650/646_Sessions.csv'
orderLineItemFile = '/Users/student2/Desktop/2-650/646_OrderLineItems.csv'
seshdf = pd.read_csv(sessionfile, header=None, skiprows=0)
OLIdf = pd.read_csv(orderLineItemFile, header=None, skiprows=0)
print("READ SUCCESS")

####CREATE LISTS
seshList = []  # list of unique patient ID's
oliList = []  # list of unique clinic ID's


def populateLists():
    h = 1
    for h in range(len(seshdf.index)):
        seshList.append(sessionItem(seshdf.iloc[h, 0], seshdf.iloc[h, 2], seshdf.iloc[h, 16], seshdf.iloc[h, 20]))
    h = 1  # indexer
    for h in range(len(OLIdf.index)):  # for each line in the spreadsheet
        oliList.append(
            orderLineItem(OLIdf.iloc[h, 0], OLIdf.iloc[h, 17], OLIdf.iloc[h, 3], OLIdf.iloc[h, 21], OLIdf.iloc[h, 6],
                          OLIdf.iloc[h, 12]))


####POPULATE LISTS
populateLists()


def prepOLIDCAList():
    global q, regInfos, x
    oliDCAList = []
    regInfos = []
    q = 0
    for q in range(len(oliList)):
        if 'DCA' in oliList[q].SKU:  # TODO: read only first three chars

            oliDCAList.append(oliList[q])
    
    p = 0
    for p in range(len(oliDCAList)):
        x = oliRegInfo(oliDCAList[p].regId, oliDCAList[p].OLId)
        regInfos.append(x)
    return regInfos


###compute charges
prepOLIDCAList()

# populate nonZeroRegInfos with elements from regInfos with reg with regId != 0
def populateNonZeros(regInfos):
    global nonZeroRegInfos, q
    nonZeroRegInfos = []
    q = 0
    for q in range(len(regInfos)):

        if regInfos[q].regId != '0':
            nonZeroRegInfos.append(regInfos[q])
            # print(nonZeroRegInfos[q-1].regId)
    return nonZeroRegInfos

def populateRegIDs(nonZeroRegInfos):
    global regIds, q, x
    # populate regIds with nonZeroRegInfos, no duplicate ids allowed
    regIds = []
    q = 0
    regIds.append(nonZeroRegInfos[0].regId)
    for q in range(len(nonZeroRegInfos)):
        uCount = 0
        tempId = nonZeroRegInfos[q].regId

        x = 0
        for x in range(len(regIds)):

            if tempId != regIds[x]:
                uCount += 1
                if uCount >= len(regIds):
                    regIds.append(nonZeroRegInfos[q].regId)
    return regIds


populateRegIDs(populateNonZeros(prepOLIDCAList))


def checkSessionCompletion(regIds):
    global x, threeSessionRegIds
    x = 0
    threeSessionRegIds = []
    for x in range(len(regIds)):
        completedSessions = 0
        i = 0
        for i in range(len(seshList)):
            if seshList[i].regId == regIds[x]:
                completedSessions += 1

                if completedSessions == 3:
                    threeSessionRegIds.append(regIds[x])
    return threeSessionRegIds


# check for session completion for each regId
checkSessionCompletion(populateRegIDs(populateNonZeros(prepOLIDCAList)))


def flagOlis(threeSessionRegIds):
    global flaggedOlis, x, q
    flaggedOlis = []
    x = 0
    for x in range(len(threeSessionRegIds)):
        olisForRegId = []
        q = 1
        for q in range(len(oliList)):

            if oliList[q].regId == threeSessionRegIds[x]:
                olisForRegId.append(oliList[q])

        if len(olisForRegId) > 1:
            flaggedOlis.append(olisForRegId[0])
    return flaggedOlis


flagOlis(threeSessionRegIds)


def outputData(flaggedOlis):
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


outputData(flagOlis())

