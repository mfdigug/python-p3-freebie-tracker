from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)
engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()


class Company(Base):
    __tablename__ = 'companies'
    # attributes
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    # relationships
    freebies = relationship('Freebie', back_populates='company')
    devs = association_proxy('freebies', 'dev',
                             creator=lambda dev: Freebie(dev=dev))

    # methods
    # create new freebie instance & assign to comnpany and dev
    def give_freebie(self, dev, item_name, value):
        freebie = Freebie(
            item_name=item_name,
            value=value,
            company=self,
            dev=dev
        )
        session.add(freebie)
        session.commit()
        return freebie

    def oldest_company():
        return session.query(Company).order_by(Company.founding_year).first()

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

    # methods
    def received_one(self, item_name):
        for freebie in self.freebies:
            if freebie.item_name == item_name:
                return True
        return False

    def give_away(self, dev, freebie):
        if freebie.dev == self:
            freebie.dev = dev
            session.commit()

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

    # i have not idea what i am doing
    def print_details(self):
        print(f"{self.dev.name} owns a {self.item_name} from {self.company.name}")

    def __repr__(self):
        return f'<Freebie {self.item_name}>'
