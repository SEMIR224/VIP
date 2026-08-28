from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# 1. የሙከራ ተጠቃሚ መረጃ (በእውነተኛ አፕ ላይ ከዳታቤዝ ይመጣል)
user_account = {
    "username": "User1",
    "balance": 1000.0  # የመነሻ ቀሪ ሂሳብ በብር
}

# 2. የጨዋታዎች እና የኦድ (Odds) ዝርዝር
matches = [
    {
        "id": 1,
        "teams": "Arsenal vs Chelsea",
        "odds": {"1": 1.85, "X": 3.40, "2": 4.20}
    },
    {
        "id": 2,
        "teams": "Real Madrid vs Barcelona",
        "odds": {"1": 2.10, "X": 3.20, "2": 3.10}
    },
    {
        "id": 3,
        "teams": "Manchester City vs Liverpool",
        "odds": {"1": 1.95, "X": 3.50, "2": 3.80}
    }
]

# 3. የተጠቃሚው ማሳያ ገጽ (HTML & JavaScript)
HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="am">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VIP Betting App</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #121212; color: #ffffff; margin: 0; padding: 20px; }
        .header { display: flex; justify-content: space-between; align-items: center; background-color: #1e1e1e; padding: 15px 20px; border-radius: 8px; margin-bottom: 20px; }
        .balance { font-size: 18px; font-weight: bold; color: #28a745; }
        .match-card { background-color: #1e1e1e; padding: 15px; border-radius: 8px; margin-bottom: 15px; border: 1px solid #333; }
        .teams { font-size: 18px; font-weight: bold; margin-bottom: 10px; }
        .odds-group { display: flex; gap: 10px; }
        .btn-odd { flex: 1; padding: 10px; background-color: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 14px; }
        .btn-odd:hover { background-color: #0056b3; }
    </style>
</head>
<body>

    <div class="header">
        <h2>VIP Betting App</h2>
        <div class="balance">ቀሪ ሂሳብ: <span id="user-balance">{{ user.balance }}</span> ETB</div>
    </div>

    <h3>የዛሬ ጨዋታዎች</h3>

    <div id="matches-list">
        {% for match in matches %}
        <div class="match-card">
            <div class="teams">{{ match.teams }}</div>
            <div class="odds-group">
                <button class="btn-odd" onclick="placeBet({{ match.id }}, '1', {{ match.odds['1'] }})">1 ({{ match.odds['1'] }})</button>
                <button class="btn-odd" onclick="placeBet({{ match.id }}, 'X', {{ match.odds['X'] }})">X ({{ match.odds['X'] }})</button>
                <button class="btn-odd" onclick="placeBet({{ match.id }}, '2', {{ match.odds['2'] }})">2 ({{ match.odds['2'] }})</button>
            </div>
        </div>
        {% endfor %}
    </div>

    <script>
        function placeBet(matchId, choice, odds) {
            let stake = prompt("የሚመድቡትን ገንዘብ መጠን ያስገቡ (ETB):");
            if (!stake || isNaN(stake) || parseFloat(stake) <= 0) {
                alert("እባክዎን ትክክለኛ የገንዘብ መጠን ያስገቡ!");
                return;
            }

            fetch('/api/bet', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    match_id: matchId,
                    choice: choice,
                    odds: odds,
                    stake: parseFloat(stake)
                })
            })
            .then(res => res.json())
            .then(data => {
                alert(data.message);
                if (data.success) {
                    document.getElementById('user-balance').innerText = data.new_balance.toFixed(2);
                }
            });
        }
    </script>

</body>
</html>
"""

# 4. የመነሻ ገጽ መስመር (Home Route)
@app.route('/')
def home():
    return render_template_string(HTML_LAYOUT, user=user_account, matches=matches)

# 5. ትኬት መቁረጫ አልጎሪዝም (Betting Logic API)
@app.route('/api/bet', methods=['POST'])
def process_bet():
    req_data = request.json
    stake = req_data.get('stake', 0)
    odds = req_data.get('odds', 1.0)

    # ቀሪ ሂሳብ ማረጋገጥ
    if stake > user_account['balance']:
        return jsonify({
            "success": False,
            "message": "ትኬት መቁረጥ አልተቻለም፡ በቂ ቀሪ ሂሳብ የለዎትም!"
        })

    # ቀሪ ሂሳብ መቀነስ እና የማሸነፊያ ስሌት
    user_account['balance'] -= stake
    potential_win = stake * odds

    return jsonify({
        "success": True,
        "message": f"ትኬቱ በትክክል ተቆርጧል!\nሊያሸንፉ የሚችሉት: {potential_win:.2f} ETB",
        "new_balance": user_account['balance']
    })

if __name__ == '__main__':
    app.run(debug=True)
