import os
import re
import base64

# Import the dl.so module which contains the main Flask app
try:
    import dl
    app = dl.app  # Use the existing Flask app from dl.so
    print("✓ Using existing dl.so Flask app")
except ImportError:
    print("Warning: dl.so module not found. Creating new Flask app.")
    from flask import Flask
    app = Flask(__name__)

# Configuration
BASE_URL = "https://daddylive.savvyservers.org"
PROXY_ENDPOINT = f"{BASE_URL}/dl/dlm3u?url="

def get_channel_info(channel_name):
    """Get channel information (tvg-id, tvg-logo, group-title) based on channel name"""
    # This is a simplified mapping - you can expand this with more channels
    channel_mapping = {
        "ABC USA": {
            "tvg-id": "ABC.(WABC).New.York,.NY.us",
            "tvg-logo": "https://raw.githubusercontent.com/MarkMCFC/iptv-scraper/refs/heads/main/logos/abc.png",
            "group-title": "UNITED STATES"
        },
        "A&E USA": {
            "tvg-id": "A.and.E.US.-.Eastern.Feed.us",
            "tvg-logo": "https://raw.githubusercontent.com/MarkMCFC/iptv-scraper/refs/heads/main/logos/aande.png",
            "group-title": "UNITED STATES"
        },
        "AMC USA": {
            "tvg-id": "AMC.-.Eastern.Feed.us",
            "tvg-logo": "https://raw.githubusercontent.com/MarkMCFC/iptv-scraper/refs/heads/main/logos/amc.png",
            "group-title": "UNITED STATES"
        },
        "Animal Planet": {
            "tvg-id": "Animal.Planet.US.-.East.us",
            "tvg-logo": "https://raw.githubusercontent.com/MarkMCFC/iptv-scraper/refs/heads/main/logos/animal-planet.png",
            "group-title": "UNITED STATES"
        },
        "BBC America (BBCA)": {
            "tvg-id": "BBC.America.-.East.us",
            "tvg-logo": "https://raw.githubusercontent.com/MarkMCFC/iptv-scraper/refs/heads/main/logos/bbc-america.png",
            "group-title": "UNITED STATES"
        },
        "BBC One UK": {
            "tvg-id": "BBCOne.uk",
            "tvg-logo": "https://raw.githubusercontent.com/MarkMCFC/iptv-scraper/refs/heads/main/logos/bbc-one.png",
            "group-title": "UNITED KINGDOM"
        },
        "BBC Two UK": {
            "tvg-id": "BBC.Two.HD.uk",
            "tvg-logo": "https://raw.githubusercontent.com/MarkMCFC/iptv-scraper/refs/heads/main/logos/bbc-two.png",
            "group-title": "UNITED KINGDOM"
        },
        "BBC Three UK": {
            "tvg-id": "BBC.Three.HD.uk",
            "tvg-logo": "https://raw.githubusercontent.com/MarkMCFC/iptv-scraper/refs/heads/main/logos/bbc-three.png",
            "group-title": "UNITED KINGDOM"
        },
        "BBC Four UK": {
            "tvg-id": "BBC.Four.HD.uk",
            "tvg-logo": "https://raw.githubusercontent.com/MarkMCFC/iptv-scraper/refs/heads/main/logos/bbc-four.png",
            "group-title": "UNITED KINGDOM"
        },
        "BBC News Channel HD": {
            "tvg-id": "BBC.World.News.North.America.(BBCWN).us",
            "tvg-logo": "https://raw.githubusercontent.com/MarkMCFC/iptv-scraper/refs/heads/main/logos/bbc-news.png",
            "group-title": "UNITED STATES"
        },
        "BET USA": {
            "tvg-id": "BET.-.Eastern.Feed.us",
            "tvg-logo": "https://raw.githubusercontent.com/MarkMCFC/iptv-scraper/refs/heads/main/logos/showtime-shoxbet-usa.png",
            "group-title": "UNITED STATES"
        },
        "Bravo USA": {
            "tvg-id": "Bravo.USA.-.Eastern.Feed.us",
            "tvg-logo": "https://raw.githubusercontent.com/MarkMCFC/iptv-scraper/refs/heads/main/logos/bravo.png",
            "group-title": "UNITED STATES"
        },
        "BIG TEN Network (BTN USA)": {
            "tvg-id": "Big.Ten.Network.us",
            "tvg-logo": "https://raw.githubusercontent.com/MarkMCFC/iptv-scraper/refs/heads/main/logos/big-ten-network.png",
            "group-title": "UNITED STATES"
        },
        "BNT 1 Bulgaria": {
            "tvg-id": "BNT.bg",
            "tvg-logo": "https://raw.githubusercontent.com/MarkMCFC/iptv-scraper/refs/heads/main/logos/bnt-1.png",
            "group-title": "BULGARIA"
        },
        "BNT 2 Bulgaria": {
            "tvg-id": "BNT2(src01).bg",
            "tvg-logo": "https://raw.githubusercontent.com/MarkMCFC/iptv-scraper/refs/heads/main/logos/bnt-2.png",
            "group-title": "BULGARIA"
        },
        "BNT 3 Bulgaria": {
            "tvg-id": "BNT.3.bg",
            "tvg-logo": "https://raw.githubusercontent.com/MarkMCFC/iptv-scraper/refs/heads/main/logos/bnt-3.png",
            "group-title": "BULGARIA"
        },
        "Barca TV Spain": {
            "tvg-id": "BarcaTV(Catalan).es",
            "tvg-logo": "https://raw.githubusercontent.com/MarkMCFC/iptv-scraper/refs/heads/main/logos/barca-tv.png",
            "group-title": "SPAIN"
        },
        "BeIN SPORTS USA": {
            "tvg-id": "beINSports.us",
            "tvg-logo": "https://raw.githubusercontent.com/MarkMCFC/iptv-scraper/refs/heads/main/logos/bein-sports-6.png",
            "group-title": "UNITED STATES"
        },
        "Benfica TV PT": {
            "tvg-id": "BenficaTVMulticamaras(src01).pt",
            "tvg-logo": "https://raw.githubusercontent.com/MarkMCFC/iptv-scraper/refs/heads/main/logos/benfica-tv.png",
            "group-title": "PORTUGAL"
        },
        "Boomerang": {
            "tvg-id": "Boomerang.us",
            "tvg-logo": "https://raw.githubusercontent.com/MarkMCFC/iptv-scraper/refs/heads/main/logos/boomerang.png",
            "group-title": "UNITED STATES"
        }
    }
    
    return channel_mapping.get(channel_name, {
        "tvg-id": "test",
        "tvg-logo": "https://raw.githubusercontent.com/MarkMCFC/iptv-scraper/refs/heads/main/logos/default.png",
        "group-title": "GENERAL"
    })

@app.route('/playlist/channels')
def serve_playlist():
    """Serve the m3u playlist with proper formatting and EPG URL"""
    try:
        # Read the original m3u file
        with open('daddylive.m3u', 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Start with the proper header
        modified_content = '#EXTM3U url-tvg="https://github.com/Pukabyte/dlepg/raw/refs/heads/main/daddylive-channels-epg.xml.gz"\n\n'
        
        # Process each line
        lines = content.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Skip empty lines and the original header
            if not line or line == '#EXTM3U':
                i += 1
                continue
            
            # Check if this is an EXTINF line
            if line.startswith('#EXTINF:'):
                # Extract channel name from the EXTINF line
                match = re.search(r'#EXTINF:-1,group-title="#DAHF",(.+)', line)
                if match:
                    channel_name = match.group(1)
                    channel_info = get_channel_info(channel_name)
                    
                    # Create the new EXTINF line with proper formatting
                    new_extinf = f'#EXTINF:-1 tvg-id="{channel_info["tvg-id"]}" tvg-logo="{channel_info["tvg-logo"]}" group-title="{channel_info["group-title"]}",{channel_name}'
                    modified_content += new_extinf + '\n'
                    
                    # Get the next line (URL) and prepend the proxy endpoint
                    i += 1
                    if i < len(lines):
                        url_line = lines[i].strip()
                        if url_line and not url_line.startswith('#'):
                            # Prepend the proxy endpoint to the URL
                            modified_url = f"{PROXY_ENDPOINT}{url_line}"
                            modified_content += modified_url + '\n\n'
            
            i += 1
        
        # Return the modified playlist with proper headers for VLC compatibility
        return app.response_class(
            modified_content,
            mimetype='audio/x-mpegurl',
            headers={
                'Access-Control-Allow-Origin': '*'
            }
        )
    
    except FileNotFoundError:
        return "Playlist file not found", 404
    except Exception as e:
        return f"Error serving playlist: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860, debug=False) 