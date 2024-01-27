import QuantLib as ql ; import xlwings as xw 
import myUtil as mu   ; from myABBR import * 
@xw.func
def bsOption(putcall, tradeDT, matDT, spotPRC, strkPRC,
             volRT=0.01, dvdRT=0.01, rfRT=0.001, Premium=0.0, Greek='NPV'):
    ''' putcall: ql.Option.Call=1, Put=-1 '''
    # 初期値 (xlwingsの為、putcallを整数とした)
    tradeDT,         matDT,           putcall                         =\
    mu.iDT(tradeDT), mu.iDT(matDT), int(putcall) ;  mu.setEvDT(tradeDT)
    # ハンドルと確率過程
    spotHDL  = mu.sqHDL(spotPRC)
    _,dvdHDL = mu.ffTSH  (tradeDT, dvdRT)    
    _,rfHDL  = mu.ffTSH  (tradeDT,  rfRT)
    volHDL   = mu.bVolTSH(tradeDT, volRT)
    bsmPROC  = ql.BlackScholesMertonProcess(spotHDL, dvdHDL, rfHDL, volHDL)
    # オプション オブジェクト    
    optOBJ  = ql.VanillaOption(ql.PlainVanillaPayoff(putcall, strkPRC), 
                                              ql.EuropeanExercise(matDT))
    optOBJ.setPricingEngine(ql.AnalyticEuropeanEngine(bsmPROC))
    #プレミアムの初期値調整 - vol計算の為
    if Premium == 0.0: Premium = optOBJ.NPV()  
    # 計算
    greeks = {"NPV": optOBJ.NPV(), "delta": optOBJ.delta(), "gamma": optOBJ.gamma(),
             "vega": optOBJ.vega(),"theta": optOBJ.thetaPerDay(),
              "vol": optOBJ.impliedVolatility(Premium, bsmPROC)}
    return greeks[Greek]