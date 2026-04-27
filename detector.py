import pandas as pd

def detect_inconsistencies(df):
    issues = []

    for _, row in df.iterrows():
        row_issues = []

        if pd.isna(row.get("EmployeeID")) or pd.isna(row.get("Name")):
            row_issues.append("Missing critical field")

        if pd.notna(row.get("Salary")):
            if row["Salary"] < 10000 or row["Salary"] > 1000000:
                row_issues.append("Salary anomaly")

        doj = row.get("DateOfJoining")
        doe = row.get("DateOfExit")

        if pd.notna(doj) and pd.notna(doe):
            if doe < doj:
                row_issues.append("Exit before joining")

        if pd.isna(row.get("Department")):
            row_issues.append("Missing department")

        issues.append(", ".join(row_issues))

    df["Issues"] = issues
    return df
