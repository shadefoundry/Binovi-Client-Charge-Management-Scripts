import checkOliListPayments
import checkSessionCharges

#set up instances of the scripts to run
y = checkSessionCharges.checkSessionCharges()
x = checkOliListPayments.checkOliListPayments()

#run the scripts to generate their respective files
x.verifyMonthlyPaymentConsistency()
y.verifySessionCharges()