import folium
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# VA hospital data
va_hospitals = [
    {"name": "Phoenix VA Health Care System", "lat": 33.4942, "lon": -112.0457, "phone": "(602) 277-5551"},
    {"name": "Northern Arizona VA Health Care System", "lat": 34.5550, "lon": -112.4707, "phone": "(928) 445-4860"},
    {"name": "Southern Arizona VA Health Care System", "lat": 32.2367, "lon": -110.9485, "phone": "(520) 792-1450"},
]

@app.route('/', methods=['GET', 'POST'])
def index():
    map = folium.Map(location=[34.0489, -111.0937], zoom_start=7)
    
    for hospital in va_hospitals:
        folium.Marker(
            [hospital['lat'], hospital['lon']],
            popup=f"{hospital['name']}<br>Phone: {hospital['phone']}"
        ).add_to(map)
    
    html = """
    <style>
        body, html { height: 100%; margin: 0; padding: 0; }
        .container { display: flex; flex-direction: column; height: 100%; }
        .main-content { display: flex; flex: 1; }
        .map-container { flex: 1; }
        .info-container { flex: 1; padding: 20px; overflow-y: auto; }
        #map { height: 100%; width: 100%; }
        .bottom-services { padding: 20px; background-color: #f0f0f0; }
        .service-list { display: flex; flex-wrap: wrap; }
        .service-item { flex: 1 0 25%; padding: 5px; }
        .service-category { margin-top: 15px; }
        .search-form { margin-top: 20px; }
        .search-form input[type="text"] { width: 70%; padding: 5px; }
        .search-form input[type="submit"] { padding: 5px 10px; }
    </style>
    <div class="container">
        <div class="main-content">
            <div class="map-container">
                <div id="map">{{ map_html|safe }}</div>
            </div>
            <div class="info-container">
                <h1>Arizona VA Hospitals and Veteran Resources</h1>
                <h2>Search for Housing by Zipcode</h2>
                <form class="search-form" action="{{ url_for('search_housing') }}" method="get">
                    <input type="text" name="zipcode" placeholder="Enter zipcode">
                    <input type="submit" value="Search Housing">
                </form>
                <h2>Search for Veteran Jobs</h2>
                <form class="search-form" action="{{ url_for('search_jobs') }}" method="get">
                    <input type="text" name="query" placeholder="Enter job title">
                    <input type="submit" value="Search Jobs">
                </form>
            </div>
        </div>
        <div class="bottom-services">
            <h2>Transportation Services</h2>
            <div class="service-category">
                <h3>Public Transportation</h3>
                <div class="service-list">
                    <div class="service-item"><a href="https://www.valleymetro.org/" target="_blank">Valley Metro (Phoenix)</a></div>
                    <div class="service-item"><a href="https://www.suntran.com/" target="_blank">Sun Tran (Tucson)</a></div>
                    <div class="service-item"><a href="https://www.yavapairegionaltransit.com/" target="_blank">Yavapai Regional Transit</a></div>
                    <div class="service-item"><a href="https://www.flagstaffaz.gov/1991/Mountain-Line" target="_blank">Mountain Line (Flagstaff)</a></div>
                    <div class="service-item"><a href="https://www.ycipta.org/" target="_blank">Yuma County Area Transit</a></div>
                    <div class="service-item"><a href="https://www.greyhound.com" target="_blank">Greyhound</a></div>
                    <div class="service-item"><a href="https://www.flixbus.com" target="_blank">FlixBus</a></div>
                    <div class="service-item"><a href="https://www.amtrak.com" target="_blank">Amtrak</a></div>
                </div>
            </div>
            <div class="service-category">
                <h3>Rental Car Services</h3>
                <div class="service-list">
                    <div class="service-item"><a href="https://www.enterprise.com" target="_blank">Enterprise</a></div>
                    <div class="service-item"><a href="https://www.hertz.com" target="_blank">Hertz</a></div>
                    <div class="service-item"><a href="https://www.avis.com" target="_blank">Avis</a></div>
                    <div class="service-item"><a href="https://www.budget.com" target="_blank">Budget</a></div>
                    <div class="service-item"><a href="https://www.alamo.com" target="_blank">Alamo</a></div>
                    <div class="service-item"><a href="https://www.nationalcar.com" target="_blank">National</a></div>
                    <div class="service-item"><a href="https://turo.com" target="_blank">Turo</a></div>
                    <div class="service-item"><a href="https://www.zipcar.com" target="_blank">Zipcar</a></div>
                </div>
            </div>
            <div class="service-category">
                <h3>Ride-Sharing Services</h3>
                <div class="service-list">
                    <div class="service-item"><a href="https://www.uber.com" target="_blank">Uber</a></div>
                    <div class="service-item"><a href="https://www.lyft.com" target="_blank">Lyft</a></div>
                </div>
            </div>
        </div>
    </div>
    """
    return render_template_string(html, map_html=map._repr_html_())

@app.route('/search_housing')
def search_housing():
    zipcode = request.args.get('zipcode', '')
    google_url = f"https://www.google.com/search?q=housing+for+rent+in+{zipcode}+Arizona"
    return redirect(google_url)

@app.route('/search_jobs')
def search_jobs():
    query = request.args.get('query', '')
    indeed_url = f"https://www.indeed.com/jobs?q={query}+veteran&l=Arizona"
    return redirect(indeed_url)

if __name__ == '__main__':
    app.run(debug=True)