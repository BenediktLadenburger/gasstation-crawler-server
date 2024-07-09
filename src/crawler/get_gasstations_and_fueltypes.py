from sql_to_dict_symlink import get


def get_gasstations_and_fueltypes():
    sql = """
        SELECT id, url, fk_fueltype as fueltype
        FROM gasstation
            INNER JOIN fuelavailability
                ON fuelavailability.fk_gasstation = gasstation.id
        WHERE is_active = true;
    """
    result_temp = get(sql, ())
    result = []
    for item in result_temp:

        # Find the index of the item with the same id
        i = next((index for (index, d) in enumerate(result)
                  if d['id'] == item['id']), None)

        if i is None:
            # If not found, add a new item with an empty fueltypes list
            new_item = {**item, 'fueltypes': []}
            result.append(new_item)
            i = len(result) - 1

        # Append the property to the fueltypes list of the found item
        result[i]['fueltypes'].append(item['fueltype'])
    return result
