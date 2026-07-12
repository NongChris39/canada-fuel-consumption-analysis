from math import sqrt
import numpy as np
import pandas as pd
from scipy import stats

def hedges_g(a: pd.Series, b: pd.Series) -> float:
    a, b = a.dropna().astype(float), b.dropna().astype(float)
    na, nb = len(a), len(b)
    pooled = (((na-1)*a.var(ddof=1))+((nb-1)*b.var(ddof=1))) / (na+nb-2)
    if pooled <= 0: return 0.0
    d = (a.mean()-b.mean()) / sqrt(pooled)
    correction = 1 - 3/(4*(na+nb)-9)
    return float(correction*d)

def welch_test(df, group_col, value_col, group_a, group_b) -> dict:
    a = df.loc[df[group_col]==group_a, value_col].dropna().astype(float)
    b = df.loc[df[group_col]==group_b, value_col].dropna().astype(float)
    if len(a)<2 or len(b)<2:
        raise ValueError(f"Not enough observations for {group_a} and {group_b}.")
    t_stat, p_value = stats.ttest_ind(a, b, equal_var=False)
    va, vb = a.var(ddof=1)/len(a), b.var(ddof=1)/len(b)
    se = sqrt(va+vb)
    df_w = (va+vb)**2 / ((va**2)/(len(a)-1)+(vb**2)/(len(b)-1))
    diff = float(a.mean()-b.mean())
    margin = stats.t.ppf(0.975, df_w)*se
    return {
        "group_column":group_col,"group_a":group_a,"group_b":group_b,
        "n_a":len(a),"n_b":len(b),"mean_a":float(a.mean()),"mean_b":float(b.mean()),
        "mean_difference_a_minus_b":diff,"ci_95_low":diff-margin,
        "ci_95_high":diff+margin,"welch_t":float(t_stat),"p_value":float(p_value),
        "hedges_g":hedges_g(a,b),
    }

def kruskal_group_test(df, group_col, value_col, min_size=5) -> dict:
    groups, names = [], []
    for name, part in df.groupby(group_col, observed=True):
        values = part[value_col].dropna().astype(float)
        if len(values)>=min_size:
            groups.append(values.to_numpy()); names.append(str(name))
    if len(groups)<2:
        raise ValueError(f"Not enough valid groups for {group_col}.")
    h, p = stats.kruskal(*groups)
    n, k = sum(map(len, groups)), len(groups)
    eps2 = max(0.0, (h-k+1)/(n-k))
    return {
        "group_column":group_col,"group_count":k,"groups":", ".join(names),
        "sample_size":n,"kruskal_h":float(h),"p_value":float(p),
        "epsilon_squared":float(eps2),
    }

def run_default_statistical_tests(df, target):
    pairwise = pd.DataFrame([
        welch_test(df,"Drivetrain inferred",target,"AWD","4WD / 4x4"),
        welch_test(df,"Fuel type",target,"D","X"),
        welch_test(df,"Manufacturer country",target,"Japan","United States"),
    ])
    known_drive = df[df["Drivetrain inferred"]!="Unknown / Other"]
    known_country = df[df["Manufacturer country"]!="Unknown"]
    global_tests = pd.DataFrame([
        kruskal_group_test(known_drive,"Drivetrain inferred",target),
        kruskal_group_test(df,"Fuel type",target),
        kruskal_group_test(known_country,"Manufacturer country",target),
    ])
    return pairwise, global_tests
