
from pprint import pprint as pp

from calculate import main as calculate

calc = calculate('Rocket 🚀', 'data/transaktioner_2022-01-01_2022-03-26.csv')

pp(calc, indent=2)
