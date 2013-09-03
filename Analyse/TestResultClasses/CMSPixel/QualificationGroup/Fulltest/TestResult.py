import AbstractClasses
import ROOT
import os
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_TestResult'
        self.NameSingle='Fulltest'
        
        self.Title = str(self.Attributes['ModuleID']) + ' ' + self.Attributes['StorageKey']
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Attributes['NumberOfChips'] = 16
        
        if self.Attributes['ModuleVersion'] == 1:
            if self.Attributes['ModuleType'] == 'a':
                self.Attributes['StartChip'] = 0
            elif self.Attributes['ModuleType'] == 'b':
                self.Attributes['StartChip'] = 7
            else:
                self.Attributes['StartChip'] = 0
            
        elif self.Attributes['ModuleVersion'] == 2:
            self.Attributes['StartChip'] = 0
        elif self.Attributes['ModuleVersion'] == 3:
            self.Attributes['NumberOfChips'] = 1
            self.Attributes['StartChip'] = 0
        
        
        
        
        self.ResultData['SubTestResultDictList'] = [
            {
                'Key':'Chips',
                'DisplayOptions':{
                    'GroupWithNext':True,
                    'Order':1,
                },
                'InitialAttributes':{
                    'ModuleVersion':self.Attributes['ModuleVersion'],   
                },
            },
            {
                'Key':'AddressLevelOverview',
                'DisplayOptions':{
                    'Order':2,
                }
            },
            {
                'Key':'BumpBondingMap',
                'DisplayOptions':{
                    'Width':4,
                    'Order':5,
                }
            },
            
            {
                'Key':'VcalThreshold',
                'DisplayOptions':{
                    'Width':4,
                    'Order':3,
                }
            },
        ]
        
        if self.Attributes['IncludeIVCurve']:
            self.ResultData['SubTestResultDictList'] += [
                {
                    'Key':'IVCurve',
                    'DisplayOptions':{
                        'Order':8,
                        'Width':3,
                    }
                },
            ]
        else:
            self.ResultData['SubTestResultDictList'] += [
                {
                    'Key':'Dummy1',
                    'Module':'Dummy',
                    'DisplayOptions':{
                        'Order':8,
                        'Width':3,
                    }
                },
            ]
        
        self.ResultData['SubTestResultDictList'] += [
            {'Key':'Noise'},
            {'Key':'VcalThresholdWidth'},
            {'Key':'RelativeGainWidth'},
            {'Key':'PedestalSpread'},
        ]
        
        if self.Attributes['ModuleVersion'] == 1:
            self.ResultData['SubTestResultDictList'] += [
                {'Key':'Parameter1'},
            ]
            
        self.ResultData['SubTestResultDictList'] += [{'Key': 'TemperatureAnalysis'}]
            
        self.ResultData['SubTestResultDictList'] += [
            {
                'Key':'Summary1',
                'DisplayOptions':{
                    'Order':4,
                }
            },
            {
                'Key':'Summary2',
                'DisplayOptions':{
                    'Order':6,
                }
            },
            {
                'Key':'Summary3',
                'DisplayOptions':{
                    'Order':7,
                }
            },
            
        ]
            
        
    def OpenFileHandle(self):
        fileHandlePath = self.FullTestResultsPath+'/commander_Fulltest.root'
        self.FileHandle = ROOT.TFile.Open(fileHandlePath)
        if not self.FileHandle:
            print 'problem to find %s'%fileHandlePath
            files = [f for f in os.listdir(self.FullTestResultsPath) if f.endswith('.root')]
            i = 0
            if len(files)>1:
                print '\nPossible Candidates for ROOT files are:'
                for f in files:
                    print '\t[%3d]\t%s'%(i,f)
                    i += 1
                i = len(files)
                while i<0 or i>= len(files):
                    try:
                        rawInput = raw_input('There are more than one possbile candidate for the ROOT file. Which file should be used? [0-%d]\t'%(len(files)-1))
                        i =  int(rawInput)
                    except:
                        print '%s is not an integer, please enter a valid integer'%rawInput
                fileHandlePath = self.FullTestResultsPath+'/'+files[i]
                print "open '%s'"%fileHandlePath
                self.FileHandle = ROOT.TFile.Open(fileHandlePath)
            elif len(files) == 1:
                i = 0
                fileHandlePath = self.FullTestResultsPath+'/'+files[i]
                print "only one other ROOT file exists. Open '%s'"%fileHandlePath
                self.FileHandle = ROOT.TFile.Open(fileHandlePath)
            else:
                print 'There exist no ROOT file in "%s"'%self.FullTestResultsPath
            
    def PopulateResultData(self):
        
        self.ResultData['Table'] = {
            'HEADER':[
                [
                    'ROC',
                    'Total',
                    'Dead',
                    'Mask',
                    'Bumps',
                    'Trim(Bits)',
                    'Address',
                    'Noise',
                    'Thresh',
                    'Gain',
                    'Ped',
                    'Par1',
                ]
            ],
            'BODY':[],
            'FOOTER':[],
        }
        LinkHTMLTemplate = self.TestResultEnvironmentObject.HtmlParser.getSubpart(
            self.TestResultEnvironmentObject.OverviewHTMLTemplate,
            '###LINK###'
        )
        for i in self.ResultData['SubTestResults']['Chips'].ResultData['SubTestResultDictList']:
            self.ResultData['Table']['BODY'].append(
                [
                    self.TestResultEnvironmentObject.HtmlParser.substituteMarkerArray(
                        LinkHTMLTemplate,
                        {
                            '###LABEL###':'Chip '+str(i['TestResultObject'].Attributes['ChipNo']),
                            '###URL###':os.path.relpath(i['TestResultObject'].StoragePath, self.StoragePath)+'/TestResult.html'
                        }
                    ),
                    i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['Total']['Value'],
                    i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nDeadPixel']['Value'],
                    i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nMaskDefect']['Value'],
                    i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nDeadBumps']['Value'],
                    i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nDeadTrimbits']['Value'],
                    i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nAddressProblems']['Value'],
                    i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nNoisy1Pixel']['Value'],
                    i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nThrDefect']['Value'],
                    i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nGainDefect']['Value'],
                    i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nPedDefect']['Value'],
                    i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nPar1Defect']['Value'],
                ]   
            )
        
        self.FileHandle.Close()
    
        
    
    def CustomWriteToDatabase(self, ParentID):
        if self.ResultData['SubTestResults'].has_key('IVCurve'):
#             self.ResultData['KeyValueDictPairs']['recalculatedCurrentAtVoltage150V']
            if self.ResultData['SubTestResults']['IVCurve'].ResultData['KeyValueDictPairs'].has_key('recalculatedCurrentAtVoltage150V'):
                CurrentAtVoltage150 = float(self.ResultData['SubTestResults']['IVCurve'].ResultData['KeyValueDictPairs']['recalculatedCurrentAtVoltage150V']['Value'])
            else:
                CurrentAtVoltage150 = float(self.ResultData['SubTestResults']['IVCurve'].ResultData['KeyValueDictPairs']['CurrentAtVoltage150']['Value'])
            IVSlope = float(self.ResultData['SubTestResults']['IVCurve'].ResultData['KeyValueDictPairs']['Variation']['Value'])
        else:
            CurrentAtVoltage150 = 0
            IVSlope = 0
        initialCurrent = 0
        Row = {
            'ModuleID' : self.Attributes['ModuleID'],
            'TestDate': self.Attributes['TestDate'],
            'TestType': self.Attributes['TestType'],
            'QualificationType': self.ParentObject.Attributes['QualificationType'],
            'Grade':  self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['Grade']['Value'],
            'PixelDefects': self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['DeadPixels']['Value'],
            'ROCsMoreThanOnePercent': self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['BadRocs']['Value'],
            'Noise': self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['NoisyPixels']['Value'],
            'Trimming': self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['TrimProblems']['Value'],
            'PHCalibration': self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['PHGainDefects']['Value'],
            'CurrentAtVoltage150': CurrentAtVoltage150,
            'IVSlope': IVSlope,
            'Temperature': self.ResultData['SubTestResults']['Summary2'].ResultData['KeyValueDictPairs']['TempC']['Value'],
            'StorageFolder':os.path.relpath(self.TestResultEnvironmentObject.TestResultsPath, self.TestResultEnvironmentObject.OverviewPath),
            'RelativeModuleFulltestStoragePath':os.path.relpath(self.StoragePath, self.TestResultEnvironmentObject.TestResultsPath),
            'initialCurrent': initialCurrent,
            'Comments': '',
            'nCycles': None,
            'CycleTempLow': None,
            'CycleTempHigh':None,
        }
        if self.TestResultEnvironmentObject.Configuration['Database']['UseGlobal']:
            pass
        else:
            with self.TestResultEnvironmentObject.LocalDBConnection:
                self.TestResultEnvironmentObject.LocalDBConnectionCursor.execute('DELETE FROM ModuleTestResults WHERE ModuleID = :ModuleID AND TestType=:TestType AND QualificationType=:QualificationType AND TestDate <= :TestDate',Row)
                self.TestResultEnvironmentObject.LocalDBConnectionCursor.execute(
                    '''INSERT INTO ModuleTestResults 
                    (
                        ModuleID,
                        TestDate,
                        TestType,
                        QualificationType,
                        Grade,
                        PixelDefects,
                        ROCsMoreThanOnePercent,
                        Noise,
                        Trimming,
                        PHCalibration,
                        CurrentAtVoltage150,
                        IVSlope,
                        Temperature,
                        StorageFolder,
                        RelativeModuleFulltestStoragePath,
                        initialCurrent,
                        Comments,
                        nCycles,
                        CycleTempLow,
                        CycleTempHigh
                    )
                    VALUES (
                        :ModuleID,
                        :TestDate,
                        :TestType,
                        :QualificationType,
                        :Grade,
                        :PixelDefects,
                        :ROCsMoreThanOnePercent,
                        :Noise,
                        :Trimming,
                        :PHCalibration,
                        :CurrentAtVoltage150,
                        :IVSlope,
                        :Temperature,
                        :StorageFolder,
                        :RelativeModuleFulltestStoragePath,
                        :initialCurrent,
                        :Comments,
                        :nCycles,
                        :CycleTempLow,
                        :CycleTempHigh
                    )
                    ''', Row)
                return self.TestResultEnvironmentObject.LocalDBConnectionCursor.lastrowid
            
    
