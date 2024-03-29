from sqlalchemy import String, Column, Float, Integer, Date, Text

from cbsqt.data.utils.tool import Base


class SuntimeFundInfo(Base):
    __tablename__ = 't_fund_info'
    __table_args__ = {'schema': 'suntime'}
    fund_id = Column(Integer, primary_key=True, index=True)
    reg_code = Column(String(200))
    reg_time = Column(Date)
    fund_name = Column(String(200))
    fund_full_name = Column(String(200))
    fund_name_py = Column(String(200))
    foundation_date = Column(Date)
    currency = Column(String(200))
    is_reg = Column(Integer)
    is_private = Column(Integer)
    fund_member = Column(String(1000))
    fund_manager = Column(String(1000))
    fund_issue_org = Column(String(1000))
    fund_custodian = Column(String(1000))
    fund_administrion = Column(String(1000))
    fund_stockbroker = Column(String(1000))
    fund_manager_nominal = Column(String(1000))
    end_date = Column(Date)
    end_cycle = Column(String(100))
    fund_type_structure = Column(String(200))
    fund_type_allocation = Column(String(200))
    fund_type_restriction = Column(String(200))
    fund_type_investment_way = Column(String(200))
    fund_type_target = Column(String(200))
    fund_type_strategy = Column(String(200))
    fund_type_strategy_level1 = Column(String(100))
    fund_type_strategy_level2 = Column(String(100))
    terminal_strategy = Column(String(100))
    fund_type_quant = Column(String(200))
    fund_type_hedging = Column(String(200))
    fund_status = Column(String(200))
    is_abnormal_liquidation = Column(Integer)
    manage_type = Column(String(1000))
    is_deposit = Column(String(200))
    country = Column(String(1000))
    prov = Column(String(1000))
    city = Column(String(1000))
    open_date = Column(String(1000))
    expected_return = Column(Float(6))
    data_freq = Column(String(20))


class SuntimeOrgInfo(Base):
    __tablename__ = 't_fund_org'
    __table_args__ = {'schema': 'suntime'}
    org_id = Column(Integer, primary_key=True)
    org_name = Column(String(400))
    org_name_en = Column(String(1000))
    org_name_py = Column(String(1000))
    org_full_name = Column(String(1000))
    org_category = Column(String(1000))
    found_date = Column(Date)
    uscc = Column(String(50))
    org_code = Column(String(400))
    is_reg = Column(Integer)
    reg_time = Column(Date)
    is_member = Column(Integer)
    member_join_date = Column(Date)
    member_type = Column(String(20))
    master_strategy = Column(String(40))
    representative_fund_id = Column(Integer)
    representative_fund = Column(String(200))
    manage_type = Column(String(400))
    other_manage_type = Column(String(5000))
    manage_fund_id = Column(Text)
    manage_fund = Column(Text)
    researcher_scale = Column(Integer)
    asset_mgt_scale = Column(Float(2))
    asset_mgt_scale_range = Column(Integer)
    property = Column(String(1000))
    reg_capital = Column(Float(6))
    real_capital = Column(Float(20))
    real_capital_proportion = Column(String(400))


class SuntimeFundOrgMapping(Base):
    __tablename__ = 't_fund_org_mapping'
    __table_args__ = {'schema': 'suntime'}
    id = Column(Integer, primary_key=True)
    fund_name = Column(String(200))
    org_name = Column(String(200))
    fund_id = Column(Integer)
    org_id = Column(Integer)
    org_type = Column(String(200))
    org_type_code = Column(Integer)
    start_date = Column(Date)
    end_date = Column(Date)
    is_current = Column(Integer)
    entry_time = Column(Date)
    update_time = Column(Date)
    tmstamp = Column(Integer)
    access_code = Column(Integer)


class SuntimeOrgEvent(Base):
    __tablename__ = 't_org_events'
    __table_args__ = {'schema': 'suntime'}
    ord_id = Column(Integer, primary_key=True, index=True)
    org_full_name = Column(String(255))
    reg_code = Column(String(50))
    reg_time = Column(Date)
    found_date = Column(Date)
    events_source = Column(String(50))
    events_type = Column(String(50))
    events_status = Column(String(50))
    events_description = Column(String(2000))
    entry_date = Column(Date)
    leave_date = Column(Date)
    leave_status = Column(String(50))
    is_last = Column(Integer)
    entry_time = Column(Date)
    update_time = Column(Date)
    tmstamp = Column(Integer)
    access_code = Column(Integer)
