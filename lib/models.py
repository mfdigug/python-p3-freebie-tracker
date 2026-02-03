from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

# company_dev = Table(
#     'company_devs',
#     Base.metadata,
#     Column('company_id', ForeignKey('companies.id'), primary_key=True),
#     Column('dev_id', ForeignKey('devs.id'), primary_key=True),
#     extend_existing=True,
# )


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    # relationships
    freebies = relationship('Freebie', back_populates='company')
    devs = association_proxy('freebies', 'dev',
                             creator=lambda dev: Freebie(dev=dev))

    def __repr__(self):
        return f'<Company {self.name}>'


class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    # relationships
    freebies = relationship('Freebie', back_populates='dev')
    companies = association_proxy('freebies', 'company',
                                  creator=lambda company: Freebie(company=company))

    def __repr__(self):
        return f'<Dev {self.name}>'


class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())

    # relationships and association object
    company_id = Column(Integer(), ForeignKey('companies.id'))
    dev_id = Column(Integer(), ForeignKey('devs.id'))

    company = relationship('Company', back_populates='freebies')
    dev = relationship('Dev', back_populates='freebies')

    def __repr__(self):
        return f'<Freebie {self.item_name}>'
