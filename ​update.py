import os
import re
from datetime import datetime
import requests

JSON_URL = "https://raw.githubusercontent.com/drmlive/sliv-live-events/main/sonyliv.json"
OUTPUT_FILE = "playlist.m3u"

BASE_M3U_TEMPLATE = """#EXTM3U
# SonyLIV Direct CDN Playlist
# Generated  : {current_time}
# CDN Host   : dishmt.slivcdn.com
# Channels   : 22
# Token embedded in each URL as ?hdnea=...
# Cookie: {token}


# ── Entertainment ──
#EXTINF:-1 tvg-id="set-hd.sonyliv" tvg-name="SET HD" group-title="SonyLIV Entertainment",SET HD
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36
#EXTVLCOPT:http-referrer=https://www.sonyliv.com/
#EXTVLCOPT:http-cookie={token}
#EXTHTTP:{{"User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36","Referrer":"https://www.sonyliv.com/","Origin":"https://www.sonyliv.com","Cookie":"{token}"}}
https://dishmt.slivcdn.com/hls/live/2011671/SETHD/master.m3u8?{token}

#EXTINF:-1 tvg-id="sab-hd.sonyliv" tvg-name="Sony SAB HD" group-title="SonyLIV Entertainment",Sony SAB HD
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36
#EXTVLCOPT:http-referrer=https://www.sonyliv.com/
#EXTVLCOPT:http-cookie={token}
#EXTHTTP:{{"User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36","Referrer":"https://www.sonyliv.com/","Origin":"https://www.sonyliv.com","Cookie":"{token}"}}
https://dishmt.slivcdn.com/hls/live/2011749/SABHD/master.m3u8?{token}

#EXTINF:-1 tvg-id="marathi.sonyliv" tvg-name="Sony Marathi" group-title="SonyLIV Entertainment",Sony Marathi
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36
#EXTVLCOPT:http-referrer=https://www.sonyliv.com/
#EXTVLCOPT:http-cookie={token}
#EXTHTTP:{{"User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36","Referrer":"https://www.sonyliv.com/","Origin":"https://www.sonyliv.com","Cookie":"{token}"}}
https://dishmt.slivcdn.com/hls/live/2011740/SonyMarathi/master.m3u8?{token}

#EXTINF:-1 tvg-id="pal.sonyliv" tvg-name="Sony Pal" group-title="SonyLIV Entertainment",Sony Pal
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36
#EXTVLCOPT:http-referrer=https://www.sonyliv.com/
#EXTVLCOPT:http-cookie={token}
#EXTHTTP:{{"User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36","Referrer":"https://www.sonyliv.com/","Origin":"https://www.sonyliv.com","Cookie":"{token}"}}
https://dishmt.slivcdn.com/hls/live/2011741/SonyPalSD/master.m3u8?{token}

#EXTINF:-1 tvg-id="aath.sonyliv" tvg-name="Sony Aath" group-title="SonyLIV Entertainment",Sony Aath
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36
#EXTVLCOPT:http-referrer=https://www.sonyliv.com/
#EXTVLCOPT:http-cookie={token}
#EXTHTTP:{{"User-Agent":"Mozilla/5.0 (Linux; Android 10; Gecko) Chrome/126.0.0.0 Mobile Safari/537.36","Referrer":"https://www.sonyliv.com/","Origin":"https://www.sonyliv.com","Cookie":"{token}"}}
https://dishmt.slivcdn.com/hls/live/2011641/SonyAathSD/master.m3u8?{token}

# ── Kids ──
#EXTINF:-1 tvg-id="yay.sonyliv" tvg-name="Sony Yay" group-title="SonyLIV Kids",Sony Yay
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36
#EXTVLCOPT:http-referrer=https://www.sonyliv.com/
#EXTVLCOPT:http-cookie={token}
#EXTHTTP:{{"User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36","Referrer":"https://www.sonyliv.com/","Origin":"https://www.sonyliv.com","Cookie":"{token}"}}
https://dishmt.slivcdn.com/hls/live/2011746/SonyYaySD/master.m3u8?{token}

# ── Movies ──
#EXTINF:-1 tvg-id="max-hd.sonyliv" tvg-name="Sony MAX HD" group-title="SonyLIV Movies",Sony MAX HD
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36
#EXTVLCOPT:http-referrer=https://www.sonyliv.com/
#EXTVLCOPT:http-cookie={token}
#EXTHTTP:{{"User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36","Referrer":"https://www.sonyliv.com/","Origin":"https://www.sonyliv.com","Cookie":"{token}"}}
https://dishmt.slivcdn.com/hls/live/2011670/SonyMaxhd/master.m3u8?{token}

#EXTINF:-1 tvg-id="max.sonyliv" tvg-name="Sony MAX" group-title="SonyLIV Movies",Sony MAX
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36
#EXTVLCOPT:http-referrer=https://www.sonyliv.com/
#EXTVLCOPT:http-cookie={token}
#EXTHTTP:{{"User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36","Referrer":"https://www.sonyliv.com/","Origin":"https://www.sonyliv.com","Cookie":"{token}"}}
https://dishmt.slivcdn.com/hls/live/2011745/SonyMaxSD/master.m3u8?{token}

#EXTINF:-1 tvg-id="max2.sonyliv" tvg-name="Sony MAX 2" group-title="SonyLIV Movies",Sony MAX 2
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36
#EXTVLCOPT:http-referrer=https://www.sonyliv.com/
#EXTVLCOPT:http-cookie={token}
#EXTHTTP:{{"User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36","Referrer":"https://www.sonyliv.com/","Origin":"https://www.sonyliv.com","Cookie":"{token}"}}
https://dishmt.slivcdn.com/hls/live/2011908/MAX2/master.m3u8?{token}

#EXTINF:-1 tvg-id="wah.sonyliv" tvg-name="Sony WAH" group-title="SonyLIV Movies",Sony WAH
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36
#EXTVLCOPT:http-referrer=https://www.sonyliv.com/
#EXTVLCOPT:http-cookie={token}
#EXTHTTP:{{"User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36","Referrer":"https://www.sonyliv.com/","Origin":"https://www.sonyliv.com","Cookie":"{token}"}}
https://dishmt.slivcdn.com/hls/live/2011906/SonyWah/master.m3u8?{token}

#EXTINF:-1 tvg-id="pix-hd.sonyliv" tvg-name="Sony PIX HD" group-title="SonyLIV Movies",Sony PIX HD
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36
#EXTVLCOPT:http-referrer=https://www.sonyliv.com/
#EXTVLCOPT:http-cookie={token}
#EXTHTTP:{{"User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36","Referrer":"https://www.sonyliv.com/","Origin":"https://www.sonyliv.com","Cookie":"{token}"}}
https://dishmt.slivcdn.com/hls/live/2011748/PIXHD/master.m3u8?{token}

# ── Sports ──
#EXTINF:-1 tvg-id="ten1-hd.sonyliv" tvg-name="Sony Ten 1 HD" group-title="SonyLIV Sports",Sony Ten 1 HD
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36
#EXTVLCOPT:http-referrer=https://www.sonyliv.com/
#EXTVLCOPT:http-cookie={token}
#EXTHTTP:{{"User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36","Referrer":"https://www.sonyliv.com/","Origin":"https://www.sonyliv.com","Cookie":"{token}"}}
https://dishmt.slivcdn.com/hls/live/2011747/TEN1HD/master.m3u8?{token}

#EXTINF:-1 tvg-id="ten1.sonyliv" tvg-name="Sony Ten 1" group-title="SonyLIV Sports",Sony Ten 1
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36
#EXTVLCOPT:http-referrer=https://www.sonyliv.com/
#EXTVLCOPT:http-cookie={token}
#EXTHTTP:{{"User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36","Referrer":"https://www.sonyliv.com/","Origin":"https://www.sonyliv.com","Cookie":"{token}"}}
https://dishmt.slivcdn.com/hls/live/2011739/TEN1SD/master.m3u8?{token}

#EXTINF:-1 tvg-id="ten2-hd.sonyliv" tvg-name="Sony Ten 2 HD" group-title="SonyLIV Sports",Sony Ten 2 HD
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36
#EXTVLCOPT:http-referrer=https://www.sonyliv.com/
#EXTVLCOPT:http-cookie={token}
#EXTHTTP:{{"User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36","Referrer":"https://www.sonyliv.com/","Origin":"https://www.sonyliv.com","Cookie":"{token}"}}
https://dishmt.slivcdn.com/hls/live/2020434/TEN2HD/master.m3u8?{token}

#EXTINF:-1 tvg-id="ten2.sonyliv" tvg-name="Sony Ten 2" group-title="SonyLIV Sports",Sony Ten 2
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36
#EXTVLCOPT:http-referrer=https://www.sonyliv.com/
#EXTVLCOPT:http-cookie={token}
#EXTHTTP:{{"User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36","Referrer":"https://www.sonyliv.com/","Origin":"https://www.sonyliv.com","Cookie":"{token}"}}
https://dishmt.slivcdn.com/hls/live/2020590/TEN2SD/master.m3u8?{token}

#EXTINF:-1 tvg-id="ten3-hd.sonyliv" tvg-name="Sony Ten 3 HD" group-title="SonyLIV Sports",Sony Ten 3 HD
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36
#EXTVLCOPT:http-referrer=https://www.sonyliv.com/
#EXTVLCOPT:http-cookie={token}
#EXTHTTP:{{"User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36","Referrer":"https://www.sonyliv.com/","Origin":"https://www.sonyliv.com","Cookie":"{token}"}}
https://dishmt.slivcdn.com/hls/live/2020591/TEN3HD/master.m3u8?{token}

#EXTINF:-1 tvg-id="ten3.sonyliv" tvg-name="Sony Ten 3" group-title="SonyLIV Sports",Sony Ten 3
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36
#EXTVLCOPT:http-referrer=https://www.sonyliv.com/
#EXTVLCOPT:http-cookie={token}
#EXTHTTP:{{"User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36","Referrer":"https://www.sonyliv.com/","Origin":"https://www.sonyliv.com","Cookie":"{token}"}}
https://dishmt.slivcdn.com/hls/live/2020592/TEN3SD/master.m3u8?{token}

#EXTINF:-1 tvg-id="ten4-hd.sonyliv" tvg-name="Sony Ten 4 HD" group-title="SonyLIV Sports",Sony Ten 4 HD
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36
#EXTVLCOPT:http-referrer=https://www.sonyliv.com/
#EXTVLCOPT:http-cookie={token}
#EXTHTTP:{{"User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36","Referrer":"https://www.sonyliv.com/","Origin":"https://www.sonyliv.com","Cookie":"{token}"}}
https://dishmt.slivcdn.com/hls/live/2020589/ten4hd/master.m3u8?{token}

#EXTINF:-1 tvg-id="ten4.sonyliv" tvg-name="Sony Ten 4" group-title="SonyLIV Sports",Sony Ten 4
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36
#EXTVLCOPT:http-referrer=https://www.sonyliv.com/
#EXTVLCOPT:http-cookie={token}
#EXTHTTP:{{"User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36","Referrer":"https://www.sonyliv.com/","Origin":"https://www.sonyliv.com","Cookie":"{token}"}}
https://dishmt.slivcdn.com/hls/live/2020437/ten4sd/master.m3u8?{token}

#EXTINF:-1 tvg-id="ten5-hd.sonyliv" tvg-name="Sony Ten 5 HD" group-title="SonyLIV Sports",Sony Ten 5 HD
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36
#EXTVLCOPT:http-referrer=https://www.sonyliv.com/
#EXTVLCOPT:http-cookie={token}
#EXTHTTP:{{"User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36","Referrer":"https://www.sonyliv.com/","Origin":"https://www.sonyliv.com","Cookie":"{token}"}}
https://dishmt.slivcdn.com/hls/live/2020593/SONYSIXHD/master.m3u8?{token}

#EXTINF:-1 tvg-id="ten5.sonyliv" tvg-name="Sony Ten 5" group-title="SonyLIV Sports",Sony Ten 5
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36
#EXTVLCOPT:http-referrer=https://www.sonyliv.com/
#EXTVLCOPT:http-cookie={token}
#EXTHTTP:{{"User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36","Referrer":"https://www.sonyliv.com/","Origin":"https://www.sonyliv.com","Cookie":"{token}"}}
https://dishmt.slivcdn.com/hls/live/2020594/SONYSIXSD/master.m3u8?{token}

# ── Infotainment ──
#EXTINF:-1 tvg-id="bbc-earth.sonyliv" tvg-name="BBC Earth HD" group-title="SonyLIV Infotainment",BBC Earth HD
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36
#EXTVLCOPT:http-referrer=https://www.sonyliv.com/
#EXTVLCOPT:http-cookie={token}
#EXTHTTP:{{"User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36","Referrer":"https://www.sonyliv.com/","Origin":"https://www.sonyliv.com","Cookie":"{token}"}}
https://dishmt.slivcdn.com/hls/live/2011907/SonyBBCEarthHD/master.m3u8?{token}
"""

def main():
    try:
        res = requests.get(f"{JSON_URL}?t={int(datetime.now().timestamp())}", timeout=15)
        res.raise_for_status()
        match = re.search(r'(hdnea=exp=[^"\'\s&]+)', res.text)
        
        if not match:
            print("Token nahi mila.")
            return

        new_token = match.group(1)

        # Agar playlist pehle se bani hai aur token same hai, to update mat karo
        if os.path.exists(OUTPUT_FILE):
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                content = f.read()
                if new_token in content:
                    print("Token already latest hai. No update needed.")
                    return

        # Nayi file likho
        now_str = datetime.now().strftime("%d %b %Y, %H:%M:%S IST")
        updated_playlist = BASE_M3U_TEMPLATE.format(token=new_token, current_time=now_str)

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(updated_playlist)

        print(f"Playlist update ho gayi with token: {new_token[:30]}...")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
