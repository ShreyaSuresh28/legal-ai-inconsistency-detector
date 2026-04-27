def compute_risk_score(df):
    scores = []
    flags = []

    for _, row in df.iterrows():
        score = 0
        f = []

        if "Missing" in str(row.get("Issues")):
            score += 20
            f.append("RED: Missing data")

        if "Salary" in str(row.get("Issues")):
            score += 20
            f.append("RED: Salary issue")

        if "Exit before joining" in str(row.get("Issues")):
            score += 30
            f.append("RED: Date violation")

        if "department" in str(row.get("Issues")).lower():
            score += 10
            f.append("GREEN: Dept issue")

        score = min(score, 100)

        scores.append(score)
        flags.append(", ".join(f))

    df["RiskScore"] = scores
    df["Flags"] = flags

    return df
