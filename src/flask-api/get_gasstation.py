import sql_to_dict


def run(id):
    sql_gasstation = """
        SELECT id, name, url, postal_id, city, street
        FROM gasstation
        WHERE id = ?;
    """
    sql_price = """
        SELECT fk_fueltype as fueltype, price, time_created
        FROM price
        WHERE fk_gasstation = ?;
    """

    gasstation = sql_to_dict.get(sql_gasstation, (id,))
    gasstation_result = sql_to_dict.get(sql_gasstation, (id,))
    if gasstation_result:
        gasstation = gasstation_result[0]
    else:
        gasstation = None

    price_results = sql_to_dict.get(sql_price, (id,))
    if price_results:
        prices = {}
        for price in price_results:
            fueltype = price['fueltype']
            del price['fueltype']
            prices[fueltype] = price
    else:
        prices = {}

    return {
        "gasstation": gasstation,
        "prices": prices
    }
