from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def check_vpn(ip_address):
    try:
        response = requests.get(f'https://ipinfo.io/{ip_address}/json')
        data = response.json()

        org = data.get('org', '')
        org_upper = org.upper()
        is_vpn = any(keyword in org_upper for keyword in ['VPN', 'HOSTING', 'CLOUDFLARE'])

        return {
            "Sehir": data.get('city', None),
            "Ulke": data.get('country', None),
            "ip": data.get('ip', ip_address),
            "vpn_mi": is_vpn,
            "org": org
        }
    except Exception as e:
        return {"error": str(e)}

@app.route('/', methods=['GET'])
def check_vpn_route():
    ip = request.args.get('ip')
    if not ip:
        return jsonify({"error": "IP NERDE YARRAM"}), 400
    
    result = check_vpn(ip)
    if 'error' in result:
        return jsonify(result), 500
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
