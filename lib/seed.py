#!/usr/bin/env python3
from faker import Faker
import random
from random import choice as rc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Company, Dev, Freebie

fake = Faker()

engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()


def create_companies():
    companies = [
        Company(
            name=fake.company(),
            founding_year=fake.year(),
        )
        for i in range(20)]
    session.add_all(companies)
    session.commit()
    return companies


def create_devs():
    devs = [
        Dev(
            name=fake.name()
        )
        for i in range(40)]
    session.add_all(devs)
    session.commit()
    return devs


def create_freebies():
    freebies = [
        Freebie(
            item_name=fake.word(),
            value=random.randint(0, 20)
        )
        for i in range(100)]
    session.add_all(freebies)
    session.commit()
    return freebies


def delete_records():
    session.query(Company).delete()
    session.query(Dev).delete()
    session.query(Freebie).delete()
    session.commit()


def relate_one_to_many(companies, devs, freebies):
    for freebie in freebies:
        freebie.company = rc(companies)
        freebie.dev = rc(devs)

    session.add_all(freebies)
    session.commit()
    return companies, devs, freebies


if __name__ == "__main__":
    delete_records()
    companies = create_companies()
    devs = create_devs()
    freebies = create_freebies()
    companies, devs, freebies = relate_one_to_many(companies, devs, freebies)
