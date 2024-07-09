import sql_to_dict


def run(gasstations):
    sql = '''
        SELECT fk_fueltype as fueltype, price, time_created
        FROM price
        WHERE fk_gasstation = ?
    '''

    for item in gasstations:
        id = item['gasstation']['id']
        res = sql_to_dict.get(sql, (id,))
        # Initialize price_history as an empty list if it doesn't exist
        if 'price_history' not in item:
            item['price_history'] = {}

        for price in res:
            # Check if the fuel_type already exists in price_history
            if price['fueltype'] not in item['price_history']:
                # If not, initialize it with an empty list
                item['price_history'][price['fueltype']] = []
            # Append the price to the corresponding fuel_type list
            item['price_history'][price['fueltype']].append({
                "price": price['price'],
                "time_created": price['time_created']
            })

    return gasstations
