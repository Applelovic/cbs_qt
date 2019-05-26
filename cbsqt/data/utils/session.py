from sqlalchemy.orm import sessionmaker
from cbsqt.data.utils.engine import Engine


class Sesssion:
    lu_cbaas_dev = sessionmaker(bind=Engine.lu_cbaas_dev)
    lu_cbaas_test = sessionmaker(bind=Engine.lu_cbaas_test)
    sycamore_cbaas_prod = sessionmaker(bind=Engine.sycamore_cbaas_prod)