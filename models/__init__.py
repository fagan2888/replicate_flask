import config

# Server
from flask import Flask
app = Flask(__name__)
app.config.from_mapping(
  SECRET_KEY = 'dev',
  SQLALCHEMY_DATABASE_URI = config.DBURI
)

# Database
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

# Mixin for generic model attributes
class IdMixin(object):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), server_default=db.func.now(), onupdate=db.func.now())

# ManyToMany relationship between Stocks and ETFs.
stock_etf = db.Table('association', db.Model.metadata,
    db.Column('stocks_id', db.Integer, db.ForeignKey('stocks.id')),
    db.Column('etfs_id', db.Integer, db.ForeignKey('etfs.id'))
)

# Stock Model
class Stock(IdMixin,db.Model):
    __tablename__ = 'stocks'
    symbol = db.Column(db.String(length=50))  # Is this unique? Length? Exchange? Data source?
    source = db.Column(db.String(length=50))  # Data source
    etf = db.relationship("ETF", back_populates="stock", uselist=False)            # The ETF if stock is ETF
    etfs = db.relationship("ETF", back_populates="stocks", secondary=stock_etf)    # The ETFs containing the stock
    history = db.relationship("History", back_populates="stock", uselist=False)
    def __repr__(self): return "<Stock(symbol='%s')>" % (self.symbol)

# ETF Model - Weights?
class ETF(IdMixin, db.Model):
    __tablename__ = 'etfs'
    stock_id = db.Column(db.Integer,db.ForeignKey('stocks.id'))                         # Unique? History?
    stock = db.relationship("Stock", back_populates="etf", uselist=False)           # The ETF's own stock
    stocks = db.relationship("Stock", back_populates="etfs", secondary=stock_etf)   # The stocks in the ETF
    def __repr__(self): return "<ETF(stock='%s')>" % (self.stock)

# History Model
class History(IdMixin, db.Model):
    __tablename__ = 'histories'
    stock_id = db.Column(db.Integer,db.ForeignKey('stocks.id'))
    stock = db.relationship("Stock", back_populates="history", uselist=False)
    date = db.Column( db.DateTime() )
    vwap = db.Column( db.Numeric() )
    high = db.Column( db.Numeric() )
    low = db.Column( db.Numeric() )
    open = db.Column( db.Numeric() )
    close = db.Column( db.Numeric() )
    def __repr__(self): return "<History(stock='%s', date='%s', price='%s')>" % (self.stock, self.date, self.vwap)

<<<<<<< HEAD
# Create Tables in DB if they don't already exist
=======
# Create tables if necessary
>>>>>>> develop
db.create_all()