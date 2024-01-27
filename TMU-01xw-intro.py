import QuantLib as ql ; import xlwings as xw
import myUtil as mu   ; from myABBR import *
@xw.func

def tiborDF(r3m, r6m, r12m, tgtDT):
    
    mu.setEvDT(mu.jDT(2022,8,1))
    tbr3m  = ql.Tibor(pdFreqQ )
    tbr6m  = ql.Tibor(pdFreqSA)
    tbr12m = ql.Tibor(pdFreqA )

    rate3mHDL  = mu.sqHDL( r3m)
    rate6mHDL  = mu.sqHDL( r6m)
    rate12mHDL = mu.sqHDL(r12m)        

    helper3m  = ql.DepositRateHelper(rate3mHDL,  tbr3m)
    helper6m  = ql.DepositRateHelper(rate6mHDL,  tbr6m) 
    helper12m = ql.DepositRateHelper(rate12mHDL,tbr12m)
    helpers   = [helper3m, helper6m, helper12m ]

    curveOBJ = ql.PiecewiseLogLinearDiscount(Tp2, calJP, helpers, dcA365)
    curveOBJ.enableExtrapolation()
    return curveOBJ.discount(mu.iDT(tgtDT)) 

@xw.func
@xw.arg('data', ndim=1)
def tiborDF2(data):
    r3m, r6m, r12m, tgtDT = data
    mu.setEvDT(mu.jDT(2022,8,1))
    tbr3m  = ql.Tibor(pdFreqQ )
    tbr6m  = ql.Tibor(pdFreqSA)
    tbr12m = ql.Tibor(pdFreqA )

    rate3mHDL  = mu.sqHDL( r3m)
    rate6mHDL  = mu.sqHDL( r6m)
    rate12mHDL = mu.sqHDL(r12m)        

    helper3m  = ql.DepositRateHelper(rate3mHDL,  tbr3m)
    helper6m  = ql.DepositRateHelper(rate6mHDL,  tbr6m) 
    helper12m = ql.DepositRateHelper(rate12mHDL,tbr12m)
    helpers   = [helper3m, helper6m, helper12m ]

    curveOBJ = ql.PiecewiseLogLinearDiscount(Tp2, calJP, helpers, dcA365)
    curveOBJ.enableExtrapolation()
    return curveOBJ.discount(mu.iDT(tgtDT)) 