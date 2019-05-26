from numpy import inf

from cbsqt.data.prod.cbaas import FundStatsHF, FundStatsMF
from cbsqt.data.dev.quant import StaticRiskRatingMF, StaticRiskRatingHF

RatingCategory = ['fwd', 'bkwd', 'rsk']

FwdFactorDict = {
    'MF': {'Stock': [FundStatsMF.TM_Alpha6M,
                     FundStatsMF.appraisalRatio1Y,
                     FundStatsMF.appraisalRatio6M,
                     FundStatsMF.informationRatio1Y],
           'Blend': [FundStatsMF.TM_Alpha6M,
                     FundStatsMF.MH_Alpha6M,
                     FundStatsMF.TM_Alpha6M,
                     FundStatsMF.returnsYTD,
                     FundStatsMF.riskAdjustedReturnsYTD,
                     (-1 * FundStatsMF.standardDeviationRatio6M).label('standardDeviationRatio6M')],
           'Bond': [FundStatsMF.CAPM_Alpha3M,
                    FundStatsMF.MH_Alpha3M,
                    FundStatsMF.TM_Alpha3M,
                    FundStatsMF.TM_Alpha6M,
                    FundStatsMF.mean3M,
                    FundStatsMF.returns3M,
                    FundStatsMF.riskAdjustedReturns3M],
           'QDII': [FundStatsMF.MH_Alpha3Y,
                    FundStatsMF.TM_Alpha3Y,
                    FundStatsMF.appraisalRatio1Y],
           'Commodity': [FundStatsMF.autoCorrelation1Y,
                         FundStatsMF.d5Ratio1Y,
                         FundStatsMF.nav],
           'Index': [FundStatsMF.conditionalVar_nonParametric3M,
                     FundStatsMF.ff3_sysrisk3M,
                     (-1 * FundStatsMF.standardDeviationRatio3M).label('standardDeviationRatio3M'),
                     (-1 * FundStatsMF.tailRisk_nonParametric3M).label('tailRisk_nonParametric3M')],
           'Absolute': [FundStatsMF.MH_Alpha3M,
                        FundStatsMF.TM_Alpha3M,
                        FundStatsMF.informationRatio3M],
           'Currency': [FundStatsMF.TM_Alpha6M,
                        FundStatsMF.informationRatio6M,
                        FundStatsMF.mean6M,
                        FundStatsMF.median6M,
                        FundStatsMF.returns6M,
                        FundStatsMF.riskAdjustedReturns6M]
           },
    'HF': {'event_driven': [FundStatsHF.GII_gamma_tstat6M,
                            FundStatsHF.GII_Beta6M,
                            FundStatsHF.var_nonParametric6M,
                            FundStatsHF.GII_gamma_tstat1Y,
                            FundStatsHF.GII_Beta1Y,
                            FundStatsHF.var_nonParametric1Y],
           'stock_long': [FundStatsHF.GII_Alpha6M,
                          FundStatsHF.appraisalRatio6M,
                          FundStatsHF.ff3_alpha6M,
                          FundStatsHF.GII_Alpha1Y,
                          FundStatsHF.appraisalRatio1Y,
                          FundStatsHF.ff3_alpha1Y],
           'cta_macro': [FundStatsHF.r3Ratio6M,
                         FundStatsHF.informationRatio6M,
                         FundStatsHF.r3Ratio1Y,
                         FundStatsHF.informationRatio1Y],
           'relative': [FundStatsHF.MH_Alpha6M,
                        FundStatsHF.TM_Alpha6M,
                        FundStatsHF.autoCorrelation6M,
                        (-1*FundStatsHF.maxDrawdownRatio6M).label('maxDrawdownRatio6M'),
                        FundStatsHF.MH_Alpha1Y,
                        FundStatsHF.TM_Alpha1Y,
                        FundStatsHF.autoCorrelation1Y,
                        (-1 * FundStatsHF.maxDrawdownRatio1Y).label('maxDrawdownRatio1Y')],
           'stock_long_short': [FundStatsHF.GII_Gamma6M,
                                FundStatsHF.informationRatio6M,
                                FundStatsHF.returns6M,
                                FundStatsHF.GII_Gamma1Y,
                                FundStatsHF.informationRatio1Y,
                                FundStatsHF.returns1Y],
           'bond': [FundStatsHF.GII_Alpha_tstat6M,
                    FundStatsHF.informationRatio6M,
                    FundStatsHF.GII_Alpha_tstat1Y,
                    FundStatsHF.informationRatio1Y],
           'fof': [FundStatsHF.GII_gamma_tstat6M,
                   FundStatsHF.MH_Alpha6M,
                   FundStatsHF.sortinoRatio6M,
                   FundStatsHF.GII_gamma_tstat1Y,
                   FundStatsHF.MH_Alpha1Y,
                   FundStatsHF.sortinoRatio1Y],
           'multi': [FundStatsHF.TM_Gamma6M,
                     FundStatsHF.GII_Beta6M,
                     FundStatsHF.ff3_alpha6M,
                     FundStatsHF.TM_Gamma1Y,
                     FundStatsHF.GII_Beta1Y,
                     FundStatsHF.ff3_alpha1Y]
           }
}

BaseColDic = {'MF': {'fund_id': FundStatsMF.fund_id,
                     'date': FundStatsMF.as_of_date_},
              'HF': {'fund_id': FundStatsHF.fund_id,
                     'date': FundStatsHF.as_of_date_}
              }

AssetCol = {'MF': 'strategy_category',
            'HF': 'strategy'}

StrategyCode = {
    'MF': {15: 'Stock',
           16: 'Blend',
           14: 'Bond',
           12: 'QDII',
           13: 'Commodity',
           17: 'Index',
           18: 'Absolute',
           19: 'Currency'
           },
    'HF': {31: 'event_driven',
           32: 'stock_long',
           33: 'cta_macro',
           34: 'relative',
           35: 'stock_long_short',
           36: 'bond',
           37: 'fof',
           38: 'multi'
           }
}

BwdFactors = {'MF': {'bkwd_relative': FundStatsMF.activePremium1Y,
                     'bkwd_absolute': FundStatsMF.returns1Y,
                     'bkwd_risk_adj': FundStatsMF.sharpRatio1Y,
                     'bkwd_mdd': (-1 * FundStatsMF.maxDrawdownRatio1Y).label('maxDrawdownRatio1Y'),
                     'bkwd_vol': (-1 * FundStatsMF.standardDeviationRatio1Y).label('standardDeviationRatio1Y'),
                     'bkwd_sys_risk': FundStatsMF.conditionalVar_nonParametric1Y
                     },
              'HF': {'bkwd_relative': FundStatsHF.activePremium1Y,
                     'bkwd_absolute': FundStatsHF.returns1Y,
                     'bkwd_risk_adj': FundStatsHF.sharpRatio1Y,
                     'bkwd_mdd': (-1 * FundStatsHF.maxDrawdownRatio1Y).label('maxDrawdownRatio1Y'),
                     'bkwd_vol': (-1 * FundStatsHF.standardDeviationRatio1Y).label('standardDeviationRatio1Y'),
                     'bkwd_sys_risk': FundStatsHF.conditionalVar_nonParametric1Y
                     }
              }

StaticRiskRatingDict = {'MF': {'rsk_regulatory': StaticRiskRatingMF.regulatory,
                               'rsk_credit': StaticRiskRatingMF.credit,
                               'rsk_operational': StaticRiskRatingMF.operational,
                               'rsk_liquidity': StaticRiskRatingMF.liquidity
                               },
                        'HF': {'rsk_regulatory': StaticRiskRatingHF.regulatory,
                               'rsk_credit': StaticRiskRatingHF.credit,
                               'rsk_operational': StaticRiskRatingHF.operational,
                               'rsk_liquidity': StaticRiskRatingHF.liquidity
                               }
                        }

InvsRiskFactorsDict = {'MF': {'rsk_investing_vol': FundStatsMF.standardDeviationRatio6M,
                              'rsk_investing_cvar': (-1*FundStatsMF.conditionalVar_nonParametric6M).
                              label('conditionalVar_nonParametric6M'),
                              'rsk_investing_tailr': FundStatsMF.tailRisk_nonParametric6M,
                              'rsk_investing_mdd': FundStatsMF.maxDrawdownRatio6M
                              },
                       'HF': {'rsk_investing_vol': FundStatsHF.standardDeviationRatio6M,
                              'rsk_investing_cvar': (-1*FundStatsHF.conditionalVar_nonParametric6M).
                              label('conditionalVar_nonParametric6M'),
                              'rsk_investing_tailr': FundStatsHF.tailRisk_nonParametric6M,
                              'rsk_investing_mdd': FundStatsHF.maxDrawdownRatio6M
                              }
                       }

SupplementOrderDict = {'MF': ['manager_id', 'company_id', 'strategy_category'],
                       'HF': ['company_id', 'strategy']
                       }

Splition = {'bkwd': ('qcut', [-inf, .1, .325, .675, .9, inf]),
            'fwd': ('qcut', [-inf, .1, .325, .675, .9, inf]),
            'rsk': ('cut', [0.3, 0.7])
            }

ColumnNaming = {'fwd': {'final': 'fwd_rating',
                        'sup': 'fwd_sup'},
                'bkwd': {'final': 'bkwd_final',
                         'sup': 'bkwd_sup',
                         'relative': 'bkwd_relative',
                         'absolute': 'bkwd_absolute',
                         'risk_adj': 'bkwd_risk_adj',
                         'mdd''vol': 'bkwd_mdd',
                         'sys_risk': 'bkwd_sys_risk'},
                'rsk': {'final': 'rsk_final',
                        'sup': 'rsk_sup',
                        'regulatory': 'rsk_regulatory',
                        'credit': 'rsk_credit',
                        'operational': 'rsk_operational',
                        'liquidity': 'rsk_liquidity',
                        'investing': 'rsk_investing',
                        'investing_vol': 'rsk_investing_vol',
                        'investing_cvar': 'rsk_investing_cvar',
                        'investing_tailr': 'rsk_investing_tailr',
                        'investing_mdd': 'rsk_investing_mdd'}}

FactorIsolated = {'fwd': False,
                  'bkwd': True,
                  'rsk': True}
