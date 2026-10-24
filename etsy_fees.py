import json

# Sample Etsy fee structure for different regions (simplified for demonstration)
# In a real-world scenario, these would be fetched from an API or a more comprehensive data source.
ETSY_FEES = {
    "UK": {
        "listing_fee_gbp": 0.20,
        "transaction_fee_percentage": 6.5,
        "payment_processing_fee_percentage": 4.0,
        "payment_processing_fee_fixed_gbp": 0.30
    },
    "EU": {
        "listing_fee_eur": 0.20,
        "transaction_fee_percentage": 6.5,
        "payment_processing_fee_percentage": 4.0,
        "payment_processing_fee_fixed_eur": 0.30
    },
    "Canada": {
        "listing_fee_cad": 0.20,
        "transaction_fee_percentage": 6.5,
        "payment_processing_fee_percentage": 4.0,
        "payment_processing_fee_fixed_cad": 0.30
    },
    "Australia": {
        "listing_fee_aud": 0.30,
        "transaction_fee_percentage": 6.5,
        "payment_processing_fee_percentage": 4.0,
        "payment_processing_fee_fixed_aud": 0.30
    }
}

def calculate_etsy_fees(price_local_currency, currency_symbol, region):
    """
    Calculates Etsy fees for a given price and region.
    Assumes price_local_currency is the price in the local currency of the region.
    """
    if region not in ETSY_FEES:
        return {"error": f"Region '{region}' not found in fee structure."}

    fees_config = ETSY_FEES[region]
    listing_fee_key = f"listing_fee_{currency_symbol.lower()}"
    payment_processing_fixed_key = f"payment_processing_fee_fixed_{currency_symbol.lower()}"

    # Ensure the required keys exist for the given currency
    if listing_fee_key not in fees_config or payment_processing_fixed_key not in fees_config:
        return {"error": f"Fee configuration missing for {currency_symbol} in {region}."}

    listing_fee = fees_config[listing_fee_key]
    transaction_fee = price_local_currency * (fees_config["transaction_fee_percentage"] / 100)
    payment_processing_fee_percentage = price_local_currency * (fees_config["payment_processing_fee_percentage"] / 100)
    payment_processing_fee_fixed = fees_config[payment_processing_fixed_key]

    total_fees = listing_fee + transaction_fee + payment_processing_fee_percentage + payment_processing_fee_fixed

    return {
        "region": region,
        "price": price_local_currency,
        "currency": currency_symbol,
        "listing_fee": round(listing_fee, 2),
        "transaction_fee": round(transaction_fee, 2),
        "payment_processing_fee_percentage_amount": round(payment_processing_fee_percentage, 2),
        "payment_processing_fee_fixed_amount": round(payment_processing_fee_fixed, 2),
        "total_fees": round(total_fees, 2)
    }

if __name__ == "__main__":
    # Example usage:
    # Selling a product for £50 in the UK
    uk_sale = calculate_etsy_fees(50.00, "GBP", "UK")
    print(json.dumps(uk_sale, indent=4))

    # Selling a product for €30 in Germany (EU)
    eu_sale = calculate_etsy_fees(30.00, "EUR", "EU")
    print(json.dumps(eu_sale, indent=4))

    # Selling a product for $75 in Canada
    canada_sale = calculate_etsy_fees(75.00, "CAD", "Canada")
    print(json.dumps(canada_sale, indent=4))

    # Selling a product for $100 in Australia
    australia_sale = calculate_etsy_fees(100.00, "AUD", "Australia")
    print(json.dumps(australia_sale, indent=4))

    # Example of an unsupported region
    unsupported_sale = calculate_etsy_fees(20.00, "USD", "USA")
    print(json.dumps(unsupported_sale, indent=4))
