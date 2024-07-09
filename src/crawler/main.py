import time
from get_gasstations_and_fueltypes import get_gasstations_and_fueltypes 
from html_thief import get_fuelprices
import database_writer


def main():
    while True:
        gasstations = get_gasstations_and_fueltypes()
        for gasstation in gasstations:
            result = get_fuelprices(gasstation['url'], gasstation['fueltypes'])
            database_writer.write(gasstation['id'], result)
            time.sleep(2)
        time.sleep(60*10)


if __name__ == "__main__":
    main()
