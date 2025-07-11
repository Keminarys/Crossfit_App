import pandas as pd

def calculate_rm1(charge: float, percentage: float) -> int:
    return int(charge / percentage)

def build_berger_table(df: pd.DataFrame, rep_max: int, charge_max: int) -> pd.DataFrame:
    df = df.copy()
    df.at[rep_max, "Charge"] = charge_max
    rm1 = calculate_rm1(charge_max, df.iloc[rep_max]["Pourcentage"])
    df.loc[1:, "Charge"] = df.loc[1:, "Pourcentage"] * rm1
    return df[df.Charge > 0].astype({"Charge": int})

def build_berger_table_multi(df: pd.DataFrame, reference_df: pd.DataFrame,
                              rep_max: int, charge_max: int, series: int) -> pd.DataFrame:
    multi_df = df.copy().iloc[:, [0, series]]
    rm1 = calculate_rm1(charge_max, reference_df.iloc[rep_max]["Pourcentage"])
    multi_df["Charge"] = multi_df[series] * rm1
    return multi_df[multi_df["Charge"] > 0].astype({"Charge": int})
