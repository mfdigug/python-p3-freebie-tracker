#!/usr/bin/env python3

from faker import Faker
import random

from sqlalchemy import create_engine

from models import Company, Dev, Freebie, session

fake = Faker()

if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')

    import ipdb
    ipdb.set_trace()
