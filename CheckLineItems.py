
# coding: utf-8

# In[10]:


from pandas import DataFrame, read_excel
import matplotlib.pyplot as plt
import pandas as pd
from dateutil import parser
from pprint import pprint

# lists used throughout the class
toFlag = []
orgList = []
sortedList = []
toFlagNo0 = []

# order object
class order:
    data = []

    def __init__(self, Id, sku, regId, orgId, createdAt, actualCost):
        self.Id = Id
        self.sku = sku
        self.regId = regId
        self.orgId = orgId
        self.createdAt = createdAt
        self.actualCost = actualCost

class checkOliListPayments():

    def prepareInitialDataFrame(self):
        global df2
        # change location of data here
        packageFile = '/Users/student2/Desktop/2_646_OrderLineItems.xlsx'
        packageDf = pd.read_excel(packageFile, header=None, sheetname='OrderLineItems', skiprows=7)
        df2 = packageDf.set_index(1)
        print("Read Success")
        return df2

    def prepareLists(self,dataFrame):
        oliAll = []
        oliPackage = []
        global i
        for i in range(len(dataFrame.index)):
            # dateTimeCharge = parser.parse(df2.iloc[i,7])
            x = order(dataFrame.iloc[i, 0], dataFrame.iloc[i, 5], dataFrame.iloc[i, 11], dataFrame.iloc[i, 20],
                      dataFrame.iloc[i, 16], dataFrame.iloc[i, 2])
            oliAll.append(x)
        for i in range(len(oliAll)):
            # get everything with the sku we care about in its own list
            # change string to search by different packages
            if "PKG" in oliAll[i].sku:
                oliPackage.append(oliAll[i])
        for i in range(len(oliPackage)):
            if oliPackage[i].orgId not in orgList:
                orgList.append(oliPackage[i].orgId)
        # sort orgIds
        # they should be sorted already when generated, but just in case we sort here
        orgList.sort()

        # sort organizations in terms of the newly sorted orgIds
        for i in range(len(orgList)):
            for j in range(len(oliPackage)):
                if oliPackage[j].orgId == orgList[i]:
                    sortedList.append(oliPackage[j])

    def verifyDataConsistency(self):
        global i
        # go through all organizations
        for i in range(len(orgList)):
            # create temp list to hold individual organizations
            filteredList = []
            for k in range(len(orgList)):
                # populate filteredList
                if sortedList[k].orgId == orgList[i]:
                    filteredList.append(sortedList[k])
            # now go through filtered list and if something's wrong with months, flag it
            for j in range(len(filteredList)):
                if (j > 1):
                    delta = filteredList[j].createdAt - filteredList[j - 1].createdAt
                    # if delta is bigger/smaller than max/min length of a month
                    if 31536000 < delta or delta < 2419200:
                        # flag it
                        toFlag.append(filteredList[j])
                        if (filteredList[j].actualCost > 0):
                            toFlagNo0.append(filteredList[j])
                    else:
                        pass

    def outputFlaggedData(self):
        global i
        df = pd.DataFrame(columns=['Id', 'sku', 'regId', 'orgId', 'createdAt', 'actualCost', 'reasonToFlag'])
        # output with 0s
        for i in range(len(toFlag)):
            df = df.append({'Id': toFlag[i].Id,
                            'sku': toFlag[i].sku,
                            'regId': toFlag[i].regId,
                            'orgId': toFlag[i].orgId,
                            'createdAt': str(toFlag[i].createdAt),
                            'actualCost': toFlag[i].actualCost,
                            'reasonToFlag': "Charge less/more than once a month"},
                           ignore_index=True)
        writer = pd.ExcelWriter('flaggedCharges.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Flagged for Review')
        writer.save()
        dfx = pd.DataFrame(columns=['Id', 'sku', 'regId', 'orgId', 'createdAt', 'actualCost', 'reasonToFlag'])
        # output without 0s
        for i in range(len(toFlagNo0)):
            dfx = dfx.append({'Id': toFlag[i].Id,
                              'sku': toFlagNo0[i].sku,
                              'regId': toFlagNo0[i].regId,
                              'orgId': toFlagNo0[i].orgId,
                              'createdAt': str(toFlagNo0[i].createdAt),
                              'actualCost': toFlagNo0[i].actualCost,
                              'reasonToFlag': "Charge less/more than once a month"},
                             ignore_index=True)
        writer = pd.ExcelWriter('flaggedChargesNoZeros.xlsx', engine='xlsxwriter')
        dfx.to_excel(writer, sheet_name='Flagged for Review')
        writer.save()
        print("Write Success")

    def verifyMonthlyPaymentConsistency(self):
        # prepare all lists to be worked with
        self.prepareLists(self.prepareInitialDataFrame())
        # verify data and flag whatever is off
        self.verifyDataConsistency()
        # log our output before generating excel sheet
        print("total orders", len(sortedList), "\norders flagged for review", len(toFlag))
        # spit out what needs to be checked
        self.outputFlaggedData()

#declare class
x = checkOliListPayments()
#call function to ensure monthly payment consistency
x.verifyMonthlyPaymentConsistency()

