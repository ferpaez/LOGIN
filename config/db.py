from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://root:Oliver97!@localhost:3306/logincat")

metadata = MetaData()

