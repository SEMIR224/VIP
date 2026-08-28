
from flask import Flask, render_template_string, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'semir_secret_key_2026'

# የአንተ ሚስጥራዊ ፓስወርድ
ADMIN_PASSWORD = "smr123"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="am">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>1WIN VIP Casino - Secure</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background-color: #0d1117; color: #ffffff; padding-bottom: 70px; }
        
        .header { display: flex; justify-content: space-between; align-items: center; padding: 12px 16px; background-color: #161b22; border-bottom: 1px solid #21262d; position: sticky; top: 0; z-index: 100; }
        .logo { font-size: 22px; font-weight: 900; font-style: italic; color: #ffffff; letter-spacing: 1px; }
        .logo span { color: #0088ff; }
        .header-right { display: flex; align-items: center; gap: 10px; }
        .balance-box { font-size: 14px; font-weight: bold; color: #8b949e; text-align: right; }
        .balance-amount { color: #2ea44f; font-size: 16px; display: block; }
        
        .container { padding: 15px; max-width: 500px; margin: 0 auto; }
        
        .banner { background: linear-gradient(135deg, #1f2937, #111827); border: 1px solid #374151; border-radius: 12px; padding: 15px; margin-bottom: 20px; text-align: center; }
        .banner h3 { color: #f59e0b; margin-bottom: 5px; font-size: 18px; }
        .banner p { color: #9ca3af; font-size: 13px; }

        .game-card { background-color: #161b22; border-radius: 16px; border: 1px solid #30363d; padding: 20px; text-align: center; box-shadow: 0 8px 24px rgba(0,0,0,0.5); }
        .game-title { font-size: 18px; font-weight: bold; color: #58a6ff; margin-bottom: 15px; text-align: left; }
        
        .slot-display { background-color: #010409; border: 2px solid #30363d; border-radius: 12px; padding: 25px 10px; margin-bottom: 20px; font-size: 45px; display: flex; justify-content: space-around; letter-spacing: 5px; }
        
        .btn-spin { background: linear-gradient(180deg, #ff9800, #ed6c02); color: #000; font-size: 18px; font-weight: 800; border: none; padding: 14px; border-radius: 10px; cursor: pointer; width: 100%; text-transform: uppercase; }
        
        .result-msg { margin-top: 15px; padding: 10px; border-radius: 8px; font-weight: bold; font-size: 15px; }
        .win-bg { background-color: rgba(46, 164, 79, 0.15); color: #3fb950; border: 1px solid rgba(46, 164, 79, 0.4); }
        .info-bg { background-color: rgba(210, 153, 34, 0.15); color: #d29922; border: 1px solid rgba(210, 153, 34, 0.4); }

        .action-section { background-color: #161b22; border-radius: 12px; border: 1px solid #30363d; padding: 15px; margin-top: 20px; }
        .action-section h4 { font-size: 15px; color: #8b949e; margin-bottom: 10px; text-align: left; }
        .input-amount, .select-method { width: 100%; padding: 12px; background-color: #0d1117; border: 1px solid #30363d; border-radius: 8px; color: white; font-size: 15px; text-align: center; margin-bottom: 10px; }
        .btn-group { display: flex; gap: 10px; }
        .btn-act { flex: 1; padding: 10px; border: none; border-radius: 8px; font-weight: bold; font-size: 13px; cursor: pointer; }
        .btn-dep-act { background-color: #238636; color: white; }
        .btn-wit-act { background-color: #da3633; color: white; }
        
        .payment-info { font-size: 12px; color: #0088ff; margin-top: 8px; text-align: left; background: rgba(0, 136, 255, 0.1); padding: 8px; border-radius: 6px; }

        .login-box { max-width: 350px; margin: 100px auto; background: #161b22; padding: 30px; border-radius: 12px; border: 1px solid #30363d; text-align: center; }
        .login-box h2 { color: #58a6ff; margin-bottom: 20px; }
        .btn-logout { background: #30363d; color: #f85149; border: none; padding: 6px 12px; border-radius: 6px; font-size: 12px; cursor: pointer; margin-top: 5px; }
    </style>
</head>
<body>

    {% if not session.get('logged_in') %}
    <div class="login-box">
        <h2>🔒 VIP Admin Login</h2>
        {% if error %}
            <p style="color: #f85149; margin-bottom: 10px; font-size: 13px;">{{ error }}</p>
        {% endif %}
        <form method="POST">
            <input type="password" class="input-amount" name="password" placeholder="ሚስጥራዊ ቃል (Password) አስገባ" required>
            <button class="btn-spin" type="submit" style="font-size: 15px; padding: 10px;">ግባ (Login)</button>
        </form>
    </div>
    {% else %}

    <div class="header">
        <div class="logo">1<span>WIN</span> VIP</div>
        <div class="header-right">
            <div class="balance-box">
                ቀሪ ሒሳብ
                <span class="balance-amount">{{ balance }} ETB</span>
            </div>
            <form action="{{ url_for('logout') }}" method="POST" style="margin:0;">
                <button class="btn-logout" type="submit">ውጣ (Logout)</button>
            </form>
        </div>
    </div>

    <div class="container">
        <div class="banner">
            <h3>🔥 100% Win Guarantee Slot</h3>
            <p>ቴሌብር እና የአቢሲንያ ባንክ የክፍያ ስርዓት</p>
        </div>

        <div class="game-card">
            <div class="game-title">🎰 VIP Lucky Slots</div>
            
            <div class="slot-display">
                <span>{{ slot1 }}</span> | <span>{{ slot2 }}</span> | <span>{{ slot3 }}</span>
            </div>

            <form method="POST">
                <input type="hidden" name="action" value="spin">
                <button class="btn-spin" type="submit">🎰 SPIN (10 ETB)</button>
            </form>

            {% if result_text %}
                <div class="result-msg {{ result_class }}">{{ result_text }}</div>
            {% endif %}
        </div>

        <!-- Payment Section (Telebirr & Bank of Abyssinia) -->
        <div class="action-section">
            <h4>💳 የክፍያ አማራጮች (Telebirr & Abyssinia)</h4>
            <form method="POST">
                <select class="select-method" name="payment_method" required>
                    <option value="telebirr">📱 ቴሌብር (Telebirr)</option>
                    <option value="abyssinia">🏦 የአቢሲንያ ባንክ (Bank of Abyssinia)</option>
                </select>
                
                <input type="number" class="input-amount" name="amount" placeholder="የገንዘብ መጠን (ETB)" required>
                <input type="text" class="input-amount" name="account_info" placeholder="የቴሌብር ቁጥር ወይም የባንክ አካውንት" required>
                
                <div class="btn-group" style="margin-top: 10px;">
                    <button class="btn-act btn-dep-act" type="submit" name="action" value="deposit">📥 Deposit (ገቢ)</button>
                    <button class="btn-act btn-wit-act" type="submit" name="action" value="withdraw">📤 Withdraw (ውጣ)</button>
                </div>
            </form>
            <div class="payment-info">
                ℹ️ በቴሌብር ወይም በአቢሲንያ ባንክ አማራጭ ገንዘብ ማስገባት እና ማውጣት ይቻላል።
            </div>
        </div>
    </div>
    {% endif %}

</body>
</html>
"""

balance = 1000.0

@app.route('/', methods=['GET', 'POST'])
def home():
    global balance
    slot1, slot2, slot3 = '💎', '💎', '💎'
    result_text = ""
    result_class = ""
    error = ""
    
    if request.method == 'POST':
        if 'password' in request.form:
            if request.form.get('password') == ADMIN_PASSWORD:
                session['logged_in'] = True
                return redirect(url_for('home'))
            else:
                error = "❌ የተሳሳተ ሚስጥራዊ ቃል! እባክዎ እንደገና ይሞክሩ።"
        
        elif session.get('logged_in'):
            action_type = request.form.get('action')
            
            if action_type == 'spin':
                if balance >= 10:
                    balance -= 10
                    slot1, slot2, slot3 = '💎', '💎', '💎'
                    win_amount = 50.0
                    balance += win_amount
                    result_text = f"🎉 እንኳን ደስ አለዎት! ጃክፖት አሸንፈዋል! +{win_amount} ETB"
                    result_class = "win-bg"
                else:
                    result_text = "⚠️ ለማጫወት በቂ ሒሳብ የሎትም! እባክዎን Deposit ያድርጉ።"
                    result_class = "info-bg"
                    
            elif action_type == 'deposit':
                try:
                    amt = float(request.form.get('amount', 0))
                    method = request.form.get('payment_method')
                    info = request.form.get('account_info')
                    method_name = "ቴሌብር" if method == 'telebirr' else "የአቢሲንያ ባንክ"
                    
                    if amt > 0:
                        balance += amt
                        result_text = f"✅ በ{method_name} ({info}) በስኬት {amt} ETB ገቢ ሆነዋል!"
                        result_class = "win-bg"
                except:
                    pass

            elif action_type == 'withdraw':
                try:
                    amt = float(request.form.get('amount', 0))
                    method = request.form.get('payment_method')
                    info = request.form.get('account_info')
                    method_name = "ቴሌብር" if method == 'telebirr' else "የአቢሲንያ ባንክ"
                    
                    if 0 < amt <= balance:
                        balance -= amt
                        result_text = f"✅ {amt} ETB በ{method_name} (Acc: {info}) እንዲወጣ ጥያቄዎ ተቀባይነት አግኝቷል!"
                        result_class = "win-bg"
                    else:
                        result_text = "❌ ለማውጣት የጠየቁት ገንዘብ ከቀሪ ሒሳብዎ ይበልጣል!"
                        result_class = "info-bg"
                except:
                    pass
                
    return render_template_string(HTML_TEMPLATE, balance=balance, slot1=slot1, slot2=slot2, slot3=slot3, result_text=result_text, result_class=result_class, error=error)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
