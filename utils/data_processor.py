def clean_and_validate(lines):
    valid = []
    invalid = 0
    total = 0

    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue

        total += 1
        parts = line.split("|")

        if len(parts) != 8:
            invalid += 1
            continue

        tid, date, pid, name, qty, price, cid, region = parts

        name = name.replace(",", "")
        qty = qty.replace(",", "")
        price = price.replace(",", "")

        if not tid.startswith("T"):
            invalid += 1
            continue
        if not cid or not region:
            invalid += 1
            continue

        try:
            qty = int(qty)
            price = float(price)
        except:
            invalid += 1
            continue

        if qty <= 0 or price <= 0:
            invalid += 1
            continue

        valid.append({
            "tid": tid,
            "product": name,
            "qty": qty,
            "price": price,
            "customer": cid,
            "region": region
        })

    print(f"Total records parsed: {total}")
    print(f"Invalid records removed: {invalid}")
    print(f"Valid records after cleaning: {len(valid)}")

    return valid
