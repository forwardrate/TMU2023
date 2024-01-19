# 短縮形リスト(abbreviation list)
import QuantLib as ql

# Calendar
calJP   =  ql.Japan()
calEU   =  ql.TARGET()
calUSf  =  ql.UnitedStates(ql.UnitedStates.FederalReserve)
calUSg  =  ql.UnitedStates(ql.UnitedStates.GovernmentBond)
calUSs  =  ql.UnitedStates(ql.UnitedStates.SOFR)
calWK   =  ql.WeekendsOnly()
calNL   =  ql.NullCalendar()
# DayCounter
dcA365  =  ql.Actual365Fixed()
dcA360  =  ql.Actual360()       # includeLastDay=false
dcA360t =  ql.Actual360(True)  # for CDS
dc30    =  ql.Thirty360(ql.Thirty360.BondBasis)
dcAA    =  ql.ActualActual(ql.ActualActual.ISDA)
# T+ days (settle days)
Tp0     =  0
Tp1     =  1
Tp2     =  2
Tp3     =  3
# payment freqency
freqA   =  ql.Annual
freqSA  =  ql.Semiannual
freqQ   =  ql.Quarterly
freqD   =  ql.Daily
# period version for pay freq
pdFreqA =  ql.Period(ql.Annual)
pdFreqSA=  ql.Period(ql.Semiannual)
pdFreqQ =  ql.Period(ql.Quarterly)
pdFreqD =  ql.Period(ql.Daily)
# schedule
mFLLW   =  ql.ModifiedFollowing
FLLW    =  ql.Following
unADJ   =  ql.Unadjusted
# date gene rule
dgRULEb =  ql.DateGeneration.Backward
dgRULEf =  ql.DateGeneration.Forward
dgRULEc =  ql.DateGeneration.CDS
# end of month
EoMf    =  False
EoMt    =  True
# compound
cmpdCMP =  ql.Compounded
cmpdCNT =  ql.Continuous
cmpdSPL =  ql.Simple
# currency
jpyFX   =  ql.JPYCurrency()
usdFX   =  ql.JPYCurrency()
# CDS : recovery rate / coupon
rcvRTz  = 0.0     # zero
rcvRTj  = 0.35    # Japan
rcvRTu  = 0.40    # US
rcvRTs  = 0.20    # subordinate
cpn025  = 0.0025
cpn100  = 0.01
cpn500  = 0.05