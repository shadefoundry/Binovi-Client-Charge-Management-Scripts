import checkOliListPayments
import checkSessionCharges

x = checkOliListPayments.checkOliListPayments()
x.verifyMonthlyPaymentConsistency()

y = checkSessionCharges.checkSessionCharges()
y.verifySessionCharges()