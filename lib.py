from pathlib import Path

import pandas as pd


def load_data(file_path: Path, sheet_name: str) -> pd.DataFrame:
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # numeric fields
    measurements = [
        'Total Nitrogen (mg/L)',
        'Total Phosphorus (mg/L)',
        'Chlorophyll (µg/L)',
        'Total Kjeldahl Nitrogen (mg/L)',
        'Enterococcus Bacteria (MPN/100mL) - A2LA Lab',
        'Enterococcus Bacteria (MPN/100mL) - BWB Lab',
        'Secchi Depth (m)'
    ]

    df[measurements] = df[measurements].apply(pd.to_numeric, errors='coerce')
    df['collection_data'] = pd.to_datetime(df['collection_date'])

    return df

