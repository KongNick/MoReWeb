# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_PHCalibrationPedestal_TestResult'
        self.NameSingle='PHCalibrationPedestal'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        

        
    def PopulateResultData(self):
        
        ROOT.gPad.SetLogy(0);
        self.ResultData['Plot']['ROOTObject_hPedestal'] =  self.ParentObject.ResultData['SubTestResults']['PHCalibrationGain'].ResultData['Plot']['ROOTObject_hPedestal']
        self.ResultData['Plot']['ROOTObject_rPedestal'] =  self.ParentObject.ResultData['SubTestResults']['PHCalibrationGain'].ResultData['Plot']['ROOTObject_rPedestal']
        
        #mP
        MeanPedestal = self.ResultData['Plot']['ROOTObject_hPedestal'].GetMean()
        #sP
        RMSPedestal = self.ResultData['Plot']['ROOTObject_hPedestal'].GetRMS()
        #nP
        IntegralPedestal = self.ResultData['Plot']['ROOTObject_hPedestal'].Integral(
            self.ResultData['Plot']['ROOTObject_hPedestal'].GetXaxis().GetFirst(), 
            self.ResultData['Plot']['ROOTObject_hPedestal'].GetXaxis().GetLast()
        )
        #nP_entries
        IntegralPedestal_Entries = self.ResultData['Plot']['ROOTObject_hPedestal'].GetEntries()
        
        # Calculation of area where are XX% of the events inside... 
        # starting from pred. mean bin.
        if IntegralPedestal > 0:
            
            # -- restricted RMS
            MeanPedestal_bin = -1000
            xLow = -1000
            xUp = 1000
            over = 0. 
            under = 0.
            tmpIntegral = 0
            extra = 0
            
            MeanPedestal_bin = self.ResultData['Plot']['ROOTObject_hPedestal'].GetXaxis().FindBin(MeanPedestal)
            i = 0
            while tmpIntegral < self.TestResultEnvironmentObject.GradingParameters['pedDistribution']: 
                
                xLow = MeanPedestal_bin-i
                xUp = MeanPedestal_bin+i
                tmpIntegral = self.ResultData['Plot']['ROOTObject_hPedestal'].Integral(xLow, xUp)/IntegralPedestal
                    
        
                
                extra = xUp - xLow
                i += 1
        else:
            xLow = -300 
            xUp = 600 
            extra = 0
            over = 0. 
            under = 0.

    
        under = self.ResultData['Plot']['ROOTObject_hPedestal'].Integral(0, xLow - extra)
        #print self.Name + ' Warning!! Line 64 needs to be fixed'
        over = self.ResultData['Plot']['ROOTObject_hPedestal'].Integral(int(xUp + 1.5*extra), self.ResultData['Plot']['ROOTObject_hPedestal'].GetNbinsX())
        
        
        self.ResultData['Plot']['ROOTObject_hPedestal'].GetXaxis().SetRange(int(xLow - extra), int(xUp + 1.5*extra))
    
        IntegralPedestal = self.ResultData['Plot']['ROOTObject_hPedestal'].Integral(
            self.ResultData['Plot']['ROOTObject_hPedestal'].GetXaxis().GetFirst(), 
            self.ResultData['Plot']['ROOTObject_hPedestal'].GetXaxis().GetLast()
        )
    
        self.ResultData['HiddenData']['PedestalMin'] = self.ResultData['Plot']['ROOTObject_hPedestal'].GetBinCenter(int(xLow-extra)) #pedMin
        self.ResultData['HiddenData']['PedestalMax'] = self.ResultData['Plot']['ROOTObject_hPedestal'].GetBinCenter(int(xUp+1.5*extra)) #pedMax
        
        self.ResultData['Plot']['ROOTObject_hPedestal'].GetXaxis().SetTitle("ADC counts");
        self.ResultData['Plot']['ROOTObject_hPedestal'].GetYaxis().SetTitle("No. of Entries");
        self.ResultData['Plot']['ROOTObject_hPedestal'].GetXaxis().CenterTitle();
        self.ResultData['Plot']['ROOTObject_hPedestal'].GetYaxis().SetTitleOffset(1.2);
        self.ResultData['Plot']['ROOTObject_hPedestal'].GetYaxis().CenterTitle();
        
        self.ResultData['Plot']['ROOTObject_hPedestal'].Draw()
    
        self.ResultData['Plot']['ROOTObject_rPedestal'].Add(self.ResultData['Plot']['ROOTObject_hPedestal'])
        self.ResultData['Plot']['ROOTObject_rPedestal'].GetXaxis().SetRange(xLow, xUp)
    
        MeanPedestal = self.ResultData['Plot']['ROOTObject_rPedestal'].GetMean()
        RMSPedestal = self.ResultData['Plot']['ROOTObject_rPedestal'].GetRMS()
    
        self.ResultData['Plot']['ROOTObject_rPedestal'].SetFillColor(ROOT.kRed)
        self.ResultData['Plot']['ROOTObject_rPedestal'].SetFillStyle(3002)
        self.ResultData['Plot']['ROOTObject_rPedestal'].Draw("same")
        
        Line = ROOT.TLine()
        line1 = Line.DrawLine(
            self.ResultData['Plot']['ROOTObject_rPedestal'].GetBinCenter(xLow), 0, 
            self.ResultData['Plot']['ROOTObject_rPedestal'].GetBinCenter(xLow), 
            0.8*self.ResultData['Plot']['ROOTObject_rPedestal'].GetMaximum()
        )
        line1.SetLineColor(ROOT.kBlue)
        line1.SetLineWidth(3)
        line1.SetLineStyle(2)
        line2 = Line.DrawLine(
            self.ResultData['Plot']['ROOTObject_rPedestal'].GetBinCenter(xUp), 0, 
            self.ResultData['Plot']['ROOTObject_rPedestal'].GetBinCenter(xUp), 
            0.8*self.ResultData['Plot']['ROOTObject_rPedestal'].GetMaximum()
        )
        line2.SetLineColor(ROOT.kBlue)
        line2.SetLineWidth(3)
        line2.SetLineStyle(2)
        
        if self.SavePlotFile:
            self.Canvas.SaveAs(self.GetPlotFileName())      
        self.ResultData['Plot']['Enabled'] = 1
        self.ResultData['Plot']['Caption'] = 'PH Calibration: Pedestal (DAC)'
        self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()
        
        
        
        self.ResultData['KeyValueDictPairs'] = {
            'N': {
                'Value':'{0:1.0f}'.format(IntegralPedestal), 
                'Label':'N'
            },
            'mu': {
                'Value':'{0:1.2f}'.format(MeanPedestal), 
                'Label':'μ'
            },
            'sigma':{
                'Value':'{0:1.2f}'.format(RMSPedestal), 
                'Label':'σ'
            }
        }
        self.ResultData['KeyList'] = ['N','mu','sigma']
        
        if under:
            self.ResultData['KeyValueDictPairs']['under'] = {'Value':'{0:1.2f}'.format(under), 'Label':'<='}
            self.ResultData['KeyList'].append('under')
        if over:
            self.ResultData['KeyValueDictPairs']['over'] = {'Value':'{0:1.2f}'.format(over), 'Label':'>='}
            self.ResultData['KeyList'].append('over')
