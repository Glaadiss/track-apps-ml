import env_file
import psycopg2
from definitions import ROOT_DIR

ENV = env_file.get(path='{}/.env'.format(ROOT_DIR))
conn = psycopg2.connect("host='{}' port={} dbname='{}' user={} password={}".format(ENV['host'], ENV['port'], ENV['dbname'], ENV['user'], ENV['password']))
