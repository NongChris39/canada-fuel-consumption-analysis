from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from .config import TARGET_COLUMN

def generate_all_figures(df: pd.DataFrame, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    values = df[TARGET_COLUMN].dropna()
    q1, med, q3 = values.quantile([0.25,0.5,0.75])
    iqr = q3-q1
    plt.figure(figsize=(12,6))
    plt.hist(values,bins=30,alpha=.75,edgecolor="black")
    for x,label,style in [
        (q1,f"Q1: {q1:.1f}","--"),(med,f"Median: {med:.1f}","--"),
        (q3,f"Q3: {q3:.1f}","--"),(q1-1.5*iqr,"Lower Tukey bound",":"),
        (q3+1.5*iqr,"Upper Tukey bound",":"),
    ]:
        plt.axvline(x,linestyle=style,label=label)
    plt.xlabel("Combined fuel consumption (L/100 km)")
    plt.ylabel("Frequency"); plt.title("Distribution of combined fuel consumption")
    plt.legend(); plt.tight_layout()
    plt.savefig(output_dir/"consumption_distribution.png",dpi=300,bbox_inches="tight")
    plt.close()

    for col, name, title in [
        ("Fuel type","consumption_by_fuel.png","Consumption by fuel type"),
        ("Manufacturer country","consumption_by_country.png","Consumption by manufacturer country"),
        ("Drivetrain inferred","consumption_by_drivetrain.png","Consumption by inferred drivetrain"),
    ]:
        plot_df = df.copy()
        if col=="Manufacturer country": plot_df = plot_df[plot_df[col]!="Unknown"]
        if col=="Drivetrain inferred": plot_df = plot_df[plot_df[col]!="Unknown / Other"]
        plt.figure(figsize=(13,7))
        sns.boxplot(data=plot_df,x=col,y=TARGET_COLUMN)
        plt.xticks(rotation=35,ha="right"); plt.title(title); plt.tight_layout()
        plt.savefig(output_dir/name,dpi=300,bbox_inches="tight"); plt.close()

    numeric_cols = [
        "Model year","Engine size (L)","Cylinders","City (L/100 km)",
        "Highway (L/100 km)","Combined (L/100 km)","Speed count",
    ]
    corr = df[[c for c in numeric_cols if c in df.columns]].corr(numeric_only=True)
    mask = np.triu(np.ones_like(corr,dtype=bool))
    plt.figure(figsize=(11,8))
    sns.heatmap(corr,mask=mask,annot=True,fmt=".2f",cmap="RdBu_r",center=0)
    plt.title("Correlation matrix of numeric technical variables")
    plt.tight_layout()
    plt.savefig(output_dir/"numeric_correlation_matrix.png",dpi=300,bbox_inches="tight")
    plt.close()

    x = df["Engine size (L)"].astype(float); y = df[TARGET_COLUMN].astype(float)
    slope, intercept = np.polyfit(x,y,1); r = np.corrcoef(x,y)[0,1]
    order = np.argsort(x.to_numpy()); xs = x.to_numpy()[order]
    plt.figure(figsize=(12,6))
    plt.scatter(x,y,alpha=.35,s=18)
    plt.plot(xs,slope*xs+intercept,linestyle="--",label=f"Slope={slope:.2f}, r={r:.3f}")
    plt.xlabel("Engine size (L)"); plt.ylabel("Combined fuel consumption (L/100 km)")
    plt.title("Engine size and fuel consumption"); plt.legend(); plt.tight_layout()
    plt.savefig(output_dir/"engine_size_vs_consumption.png",dpi=300,bbox_inches="tight")
    plt.close()

    counts = df["Vehicle class simplified"].value_counts()
    plt.figure(figsize=(12,6)); ax = counts.plot(kind="bar",edgecolor="black")
    for i,v in enumerate(counts): ax.text(i,v,str(v),ha="center",va="bottom")
    plt.xlabel("Simplified vehicle class"); plt.ylabel("Number of vehicles")
    plt.title("Distribution of simplified vehicle classes")
    plt.xticks(rotation=35,ha="right"); plt.tight_layout()
    plt.savefig(output_dir/"vehicle_class_distribution.png",dpi=300,bbox_inches="tight")
    plt.close()
