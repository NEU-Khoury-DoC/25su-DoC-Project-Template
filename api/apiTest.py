from flask import Flask, jsonify
import requests
import pandas as pd


app = Flask(__name__)

API_URL = "https://data.europarl.europa.eu/api/v2/meps"
HEADERS = {
    "Accept": "application/json"
}

@app.route("/meps")
def getMEPs():
    try:
        resp = requests.get("https://data.europarl.europa.eu/api/v2/meps", headers=HEADERS)
        data = resp.json()

        meps_raw = data.get("data", [])
        mep_records = []

        for mep in meps_raw:
            if not isinstance(mep, dict):
                continue

            mep_id_raw = mep.get("id", "")
            mep_id = mep_id_raw.split("/")[-1]
            name = mep.get("label", "")
            european_group = mep.get("politicalGroup", {}).get("label", "")  # ✅ group added

            if mep_id and name:
                mep_records.append({
                    "mep_id": mep_id,
                    "name": name,
                    "european_group": european_group
                })

        meps_df = pd.DataFrame(mep_records)

        import os
        os.makedirs("output", exist_ok=True)
        meps_df.to_csv("output/meps_list.csv", index=False)

        return jsonify(mep_records)

    except Exception as e:
        print("Error fetching MEPs:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/voteEU")
def getEUs():
    try:

        params = {
            "format": "application/ld+json",
        }

        resp = requests.get("https://howtheyvote.eu/api/votes", params, headers=HEADERS)
        print(resp)
        data = resp.json()  
        return data

    except requests.exceptions.RequestException as e:
        print("failed:", e)
        return "bad"
    

@app.route("/mep-speeches")
def get_mep_speech_profiles():
    try:
        BASE_URL = "https://data.europarl.europa.eu/api/v2/speeches"

        headers = {
            "Accept": "application/ld+json",
            "User-Agent": "trayna-dev-0.1"
        }

        params = {
            "parliamentary-term": ["10"],
            "activity-type": ["PLENARY_DEBATE_SPEECH"],
            "sitting-date": "2024-01-01",
            "sitting-date-end": "2024-12-31",
            "limit": 50,
            "offset": 0
        }

        all_speeches = []
        max_pages = 5
        for i in range(max_pages):
            params["offset"] = i * params["limit"]
            resp = requests.get(BASE_URL, headers=headers, params=params)
            if resp.status_code != 200:
                print(f"Error fetching speeches on page {i+1}")
                break

            json_data = resp.json()
            items = json_data.get("data", {}).get("items", [])
            if not items:
                break

            for item in items:
                all_speeches.append({
                    "person_id": item.get("person", {}).get("id"),
                    "person_name": item.get("person", {}).get("fullName"),
                    "activity_type": item.get("activityType", {}).get("label", ""),
                    "date": item.get("activity", {}).get("startDate")
                })

            time.sleep(1)

        # Aggregate
        mep_stats = defaultdict(lambda: {"total": 0, "PLENARY_DEBATE_SPEECH": 0})
        for s in all_speeches:
            if not s["person_id"]:
                continue
            name = s["person_name"]
            typ = s["activity_type"]
            mep_stats[name]["total"] += 1
            mep_stats[name][typ] += 1

        df = pd.DataFrame([
            {
                "MEP": mep,
                "Total Speeches": data["total"],
                "Debate Speeches": data.get("PLENARY_DEBATE_SPEECH", 0)
            }
            for mep, data in mep_stats.items()
        ])

        os.makedirs("output", exist_ok=True)
        df.to_csv("output/mep_speech_profile.csv", index=False)

        return jsonify(df.to_dict(orient="records"))

    except Exception as e:
        return jsonify({"error": str(e)}), 500


base_url = "https://howtheyvote.eu/api/votes"
all_votes = []

# --- Paginate through results ---
page = 1
while True:
    print(f"Fetching page {page}...")
    resp = requests.get(base_url, params={"page": page})
    data = resp.json()
    
    results = data.get("results", [])
    if not results:
        break  # No more pages

    for vote in results:
        all_votes.append({
            'vote_id': vote.get('id'),
            'title': vote.get('title'),
            'subject': vote.get('subject'),
            'timestamp': vote.get('timestamp')[:10],
            'url': vote.get('url')
        })
    
    if data.get("next") is None:
        break
    page += 1

# --- Convert to DataFrame and Save ---
df_leg_votes = pd.DataFrame(all_votes)
df_leg_votes.to_csv("all_egislative_votes.csv", index=False)
print("✅ Saved all_legislative_votes.csv with", len(df_leg_votes), "votes.")
    
if __name__ == "__main__":
    app.run(debug=True, port=5001)