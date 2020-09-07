def round_fraction_to_nearest_int(frac_str):
    num_str, denom_str = frac_str.split('/')
    num = float(num_str)
    denom = float(denom_str)
    return round(num / denom)
