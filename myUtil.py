import numpy as np    ; import pandas as pd ; import datetime as dt 
import QuantLib as ql ; import myUtil as mu ; from myABBR import *

##### 日付関連 #####
# japan日付
def jDT(yyyy,mm,dd):
  '''jDT(yyyy,mm,dd)=ql.Date(dd,mm,yyyy)'''
  return ql.Date(dd,mm,yyyy)
# iso日付
def iDT(isoDT): 
  '''iDT(isoDT)=ql.Date(isoDT,'%Y-%m-%d')'''
  return ql.Date(isoDT, '%Y-%m-%d')
# (付録) シリアル値から日付クラス変換
def sDT(serialDT): 
    """serial to QL Date class"""      
    return ql.Date().from_date(dt.datetime(1899,12,30)+ dt.timedelta(serialDT))
    
##### ショートカット #####
# ブラックコンスタントボラTSハンドル
def bVolTSH(tradeDT, vol, cal=calWK, dc=dcA365):   
  '''bVolTSH(tradeDT, vol, cal=calWK, dc=dcA365)
                                    =ql.BlackVolTSH(ql.BlackConstantVol(...))''' 
  return ql.BlackVolTermStructureHandle(
                    ql.BlackConstantVol(tradeDT, cal, vol, dc))
# フラットフォワード ** OBJとTSHの2つを戻す点に注意  **
def ffTSH(tradeDT, rate, dc=dcA365, cmpd=2, freq=1):   
  '''ffTSH(tradeDT,rate,dc=dcA365,cmpd=2,freq=1) 
                                    = ffCrvOBJ,ql.YTS(ql.FlatForward(...))
     cmpd=2:ql.Continuous, 1:Compounded freq=1:ql.Annual 2:Semiannual''' 
  ffCrvOBJ = ql.FlatForward(tradeDT, rate, dc, cmpd, freq)
  return (ffCrvOBJ, ql.YieldTermStructureHandle(ffCrvOBJ))
# SettingクラスevaluationDate設定
def setEvDT(evaluationDT):  
  '''Settings.instance().evaluationDate = evaluationDT'''
  ql.Settings.instance().evaluationDate = evaluationDT
# シンプルクォート
def sqHDL(rt):   
  '''sqHDL(rt)=ql.QuoteHandle(ql.SimpleQuote(rt))''' 
  return ql.QuoteHandle(ql.SimpleQuote(rt))
  
##### 各種カーブオブジェクト作成 #####
# SOFRカーブ
def makeSofrCurve(crvDATA):
    '''makeSofrCurve(crvDATA)->[sofrIX,sfCrvOBJ,sfCrvHDL,sfParRATE]'''      
  # 1.指標金利オブジェクトと初期値設定
    sfCrvHDL = ql.RelinkableYieldTermStructureHandle()  
    sofrIX = ql.Sofr(sfCrvHDL)
  # 2. HelperとSOFRカーブオブジェクト
    cHelper, sfParRATE = [], []
    for knd, tnr, rt in crvDATA:
        if knd == 'depo':
            if ql.Period(tnr).length() == 1:
                cHelper.append(ql.DepositRateHelper(mu.sqHDL(rt/100),sofrIX)) 
        if knd == 'swap': cHelper.append(
            ql.OISRateHelper(Tp2, ql.Period(tnr),mu.sqHDL(rt/100),sofrIX))
        sfParRATE.append(rt/100)                             # パーレート用リスト
    sfCrvOBJ = ql.PiecewiseLogLinearDiscount(Tp0, calUSs, cHelper, dcA360)
    sfCrvHDL.linkTo(sfCrvOBJ) ; sfCrvOBJ.enableExtrapolation()
    return [sofrIX, sfCrvOBJ, sfCrvHDL, sfParRATE]      # 4つのオブジェクトを戻す
  
# TONAカーブ
def makeTonaCurve(crvDATA):
    '''makeTonaCurve(crvDATA)->[tonaIX,tnCrvOBJ,tnCrvHDL,tnParRATE]'''
  # 1.指標金利オブジェクト
    tnCrvHDL = ql.RelinkableYieldTermStructureHandle()  
    tonaIX = ql.OvernightIndex('TONA', Tp0,   jpyFX, calJP, dcA365, tnCrvHDL)
    tonaTN = ql.OvernightIndex('TONA', Tp0+1, jpyFX, calJP, dcA365, tnCrvHDL)
  # 2. HelperとTONAカーブオブジェクト
    cHelper, tnParRATE = [], []
    for knd, tnr, rt in crvDATA:
       if knd == 'depo':
          if ql.Period(tnr).length() == 1:
              cHelper.append(ql.DepositRateHelper(mu.sqHDL(rt/100),tonaIX)) 
          if ql.Period(tnr).length() == 2:
              cHelper.append(ql.DepositRateHelper(mu.sqHDL(rt/100),tonaTN)) 
       if knd == 'swap': cHelper.append(
            ql.OISRateHelper(Tp2, ql.Period(tnr),mu.sqHDL(rt/100),tonaIX))
       tnParRATE.append(rt/100)                            # パーレート用リスト
    tnCrvOBJ = ql.PiecewiseLogLinearDiscount(Tp0, calJP, cHelper, dcA365)
    tnCrvHDL.linkTo(tnCrvOBJ) ; tnCrvOBJ.enableExtrapolation()
    return [tonaIX, tnCrvOBJ, tnCrvHDL, tnParRATE]    # 4つのオブジェクトを戻す
  
# TIBORカーブ
def makeTiborCurve(crvDATA):
    '''makeTiborCurve(crvDATA)->[tbrIX,tbCrvOBJ,tbCrvHDL,tbParRATE]'''
  # 1.指標金利オブジェクト
    tbCrvHDL = ql.RelinkableYieldTermStructureHandle() 
    tbrIX    = ql.Tibor(pdFreqSA, tbCrvHDL)
  # 2. HelperとTONAカーブオブジェクト
    cHelper, tbParRATE = [], []
    for knd, tnr, rt in crvDATA:
       if knd == 'depo': cHelper.append(ql.DepositRateHelper(mu.sqHDL(rt/100),tbrIX)) 
       if knd == 'swap': cHelper.append(ql.SwapRateHelper(   mu.sqHDL(rt/100),
                                ql.Period(tnr), calJP, freqSA, mFLLW, dcA365, tbrIX))
       tbParRATE.append(rt/100)                            # パーレート用リスト
    tbCrvOBJ = ql.PiecewiseLogLinearDiscount(Tp2, calJP, cHelper, dcA365)
    tbCrvHDL.linkTo(tbCrvOBJ) ; tbCrvOBJ.enableExtrapolation()
    return [tbrIX, tbCrvOBJ, tbCrvHDL, tbParRATE]  # 4つのオブジェクトを戻す  
  
##### アニュイティ計算 #####
def calcAnnuity(schdOBJ, crvOBJ, dc=dcA365): 
    '''calcAnnuity(scheduleOBJ, curveOBJ, dc=dcA365) -> Annuity)'''
    discFCT = np.array([crvOBJ.discount(d) for d in schdOBJ][1:])
    tnrLST  = np.diff([dc.yearFraction(schdOBJ.startDate(), d) for d in schdOBJ]) 
    return np.sum(tnrLST * discFCT) 

##### Swap/債券キャッシュフロー表 #####
# Swap
def swapCashFlow(swapOBJ, curveOBJ, leg=1, dc=dcA365): 
    '''swapCashFlow(swapOBJ, curveOBJ, leg=1:FLoat  0:Fix)-> DataFrame)'''  
    if leg == 1:  # 変動ﾚｸﾞ leg(1)
        dfSWP = pd.DataFrame({
            'fixingDate': cpn.fixingDate().ISO(),
            'accruStart': cpn.accrualStartDate().ISO(),
            'accruEnd':   cpn.accrualEndDate().ISO(),
            'payDate':    cpn.date(),                            # No ISO form
            'days':       dc.dayCount(cpn.accrualStartDate(),cpn.accrualEndDate()),
            'rate':       cpn.rate(),
            'spread':     cpn.spread(),
            'amount':     cpn.amount(),
            } for cpn in map(ql.as_floating_rate_coupon, swapOBJ.leg(1)))
    else:          # 固定ﾚｸﾞ leg(0)
        dfSWP = pd.DataFrame({
            'nominal':    cpn.nominal(),
            'accruStart': cpn.accrualStartDate().ISO(),
            'accruEnd':   cpn.accrualEndDate().ISO(),
            'payDate':    cpn.date(),
            'days':       dc.dayCount(cpn.accrualStartDate(),cpn.accrualEndDate()),
            'rate':       cpn.rate(),
            'amount':     cpn.amount()
            } for cpn in map(ql.as_fixed_rate_coupon, swapOBJ.leg(0)))
    # ディスカウントファクター(DF)
    settleDT = curveOBJ.referenceDate()
    psDF = [1.0                   for dt in dfSWP.payDate if dt <= settleDT] # past   DF
    fuDF = [curveOBJ.discount(dt) for dt in dfSWP.payDate if settleDT < dt ] # future DF
    dfSWP = pd.concat([dfSWP, pd.DataFrame(psDF+fuDF, columns=['DF']) ], axis=1)
    dfSWP.payDate = dfSWP.payDate.map(lambda x: x.ISO())                        # ISOへ
    return dfSWP

# 債券 (past=0は過去キャッシュフローを表示)
def bondCashFlow(bondOBJ, irt='', yts='', past=0):    
    '''1:(irt='',yts='')=No DF      2:(irt=irOBJ, yts='')=ir DF
       3:(irt='', yts=ytOBJ)=yt DF  
       4:( , ,past=0)=futureCF      5:( , ,past=1)=past+futureCF    '''
    dfBND = pd.DataFrame({
        'payDate':    cpn.date(),          # no ISO
        'coupon':     cpn.rate(),
        'accruStart': cpn.accrualStartDate().ISO(),
        'accruEnd':   cpn.accrualEndDate().ISO(),
        'amount':     cpn.amount(),
        } for cpn in map(ql.as_coupon, bondOBJ.cashflows()) if cpn is not None )
    # 元本
    dfPRN = pd.DataFrame({'payDate': cf.date(), 'amount':cf.amount()} 
                for cf, cpn in zip(bondOBJ.cashflows(),
                map(ql.as_coupon, bondOBJ.cashflows())) if cpn is None )
    dfBND = dfBND.append(dfPRN, ignore_index=True )
    # ディスカウントファクター列作成
    settleDT = bondOBJ.settlementDate()
    psDF = [1.0       for dt in dfBND.payDate if dt <= settleDT]     #past DF
    # future DF
    if irt != '' and yts == '' :                                     # irtOBJ
      fuDF = [irt.discountFactor(settleDT, dt)
                      for dt in dfBND.payDate if settleDT < dt ] 
      dfBND = pd.concat([dfBND, pd.DataFrame(psDF+fuDF, columns=['DF']) ], axis=1)
    elif yts != '' :                                                  # ytsOBJ
      fuDF = [yts.discount(dt)
                      for dt in dfBND.payDate if settleDT < dt ] 
      dfBND = pd.concat([dfBND, pd.DataFrame(psDF+fuDF, columns=['DF']) ], axis=1)
    # 将来キャッシュフローの抽出
    if past == 0: 
      dfBND = dfBND[dfBND.payDate >= settleDT]
      dfBND = dfBND.reset_index(drop=True)              #インデックス番号リセット
    dfBND.payDate  =  dfBND.payDate.map(lambda x: x.ISO())  # ISOフォーマットへ
    return dfBND
  