version = "2025.12.08.1"
url = "https://api-v3.mbta.com/";
key = "91944a70800a4bcabe1b9c2023d12fc8";
gkey = "YOUR_GOOGLE_MAPPING_KEY";
headers = {'Accept': 'application/json', "Accept-Encoding": "gzip", 'x-api-key': key};
maxPredEntries = 20;

////////////////////////////////////
// Get feed from DB - generic     //
////////////////////////////////////
async function getFeed(url) {
    try {
        const res = await fetch(url);
        if (!res.ok) {
           const errorData = await res.json(); // Attempt to parse error response
           throw new Error(`HTTP error! status: ${res.status}, code: ${errorData.errorCode}`);
        }
        const obj = await res.json();
        return obj;
        }
     catch (error) { 
        console.error("Error: ", error); 
        document.getElementById("warnLabel").innerHTML = "Too many requests.";
        }
    }
    
//////////////////////////////
// Nearby functionality     //
//////////////////////////////
async function getNearbyStations() {
    document.getElementById("warnLabel").innerHTML = "Please wait...";
    const radius = get_radius(document.getElementById("radius").value);
    const position = await getCoords(),
            { coords } = position;
    const lat = position['coords']['latitude'];
    const long = position['coords']['longitude'];

    const nst_url = url+"stops/?filter[longitude]="+long+"&filter[latitude]="+lat+"&filter[radius]="+radius;
    const nst = (await getFeed(nst_url))['data'];
             
    if (nst.length == 0) {
        console.log(" No data currently available. Try again later.");
        console.log(" Possible cause: no service available at this time\n");
        return;
        }
    
    let select = document.getElementById("nearbyStations");
    select.innerHTML = "";

    const stops_url = url+"stops/";
    const stops = (await getFeed(stops_url))['data'];
    
    for(var i = 0; i < nst.length; i++) {
        if (['node', 'door'].indexOf(nst[i]['id'].slice(0,4))<0) {
            let nameSt = await get_stops(nst[i]['id'], stops);
            if(!isNaN(nst[i]['id'].slice(0,4))) {
                nameSt+=" - Bus";}
            let dist = get_distance(lat, long, nst[i]['attributes']['latitude'], nst[i]['attributes']['longitude'],0);
            select.innerHTML += "<option value=\"" + nst[i]['id'] + "\">" + nameSt + "\t("+ dist+" m)</option>";
            }}
    document.getElementById("warnLabel").innerHTML = "";
    setNearbyStations();
    }
    
async function setNearbyStations() {
    let select = document.getElementById("nearbyStations");
    let stat_id = select.options[select.selectedIndex].value;
    document.getElementById("station").value = stat_id;
    getRoutes(stat_id);
    }

//////////////////////////////
// Signs prediction view    //
//////////////////////////////
function predSigns() {
    document.getElementById("warnLabel").innerHTML = "Please wait...";
    const station = document.getElementById("station").value;
    const routes = document.getElementById("route").value;
    setCookie('currStation',station,100);
    setCookie('currRoute',routes,100);
    getSigns(station, routes);
}

async function getSigns(station, routes) {
    let label = [];
    let line = routes.split(" ");
    
    //############################
    //# get all stops/vehicles
    //############################
    const stops_url = url+"stops/";
    const stops = (await getFeed(stops_url))['data'];
    
    const vh_url = url+"vehicles/";
    const vh = (await getFeed(vh_url))['data'];
    
    const st_url = url+"stops/?filter[id]="+station;
    const s = (await getFeed(st_url))['data'];
    const statNameCurr = s[0]['attributes']['name'];
    
    const rt_url = url+"routes/?filter[id]="+line;
    const dest = (await getFeed(rt_url))['data'][0]['attributes']['direction_destinations'];
    
    const pr_url = url+"predictions/?filter[stop]="+station;
    const p = (await getFeed(pr_url))['data'];
    
    if (p.length ==0) {
        label += "\n No data currently available. Try again later.\n";
        label += " Possible cause: no service available at this time\n";
        document.getElementById("results").innerHTML = "".concat(...label);
        document.getElementById("warnLabel").innerHTML = "";
        return;
        }
    
    let dummy = 0;
    let pred_arr_times = [];
    let direction = [];
    let status = [];
    let vstation = [];
    let vstatName =[];
    let vstatus = [];
    let vtype = [];
    let locat = [];
    let lines = [];
    let vla = [];
    let vlo = [];
    
    let current_time = get_current_time();
    document.getElementById("results").innerHTML = "Something is wrong. Please reload page.";
    
    for (let i=0; i<p.length; i++) {
        let id_line = p[i]['relationships']['route']['data']['id'];
        if (line.includes(id_line) == true && dummy < maxPredEntries && p[i]['attributes']['schedule_relationship'] != "CANCELLED") {
            if (p[i]['attributes']['arrival_time'] !== null) {
                arr_time = p[i]['attributes']['arrival_time'].slice(11).slice(0,-6);
                arr_time_mins = (get_sec(arr_time) - get_sec(current_time))/60;
            } else {
                arr_time_mins = -10;
                }
            
            lines.push(id_line);
            direction += p[i]['attributes']['direction_id'];
            pred_arr_times.push(get_sign(arr_time_mins));
                                    
            if (p[i]['relationships']['vehicle']['data'] !== null) {
                for (let j=0; j<vh.length; j++) {
                    if (vh[j]['id'] == p[i]['relationships']['vehicle']['data']['id']) {
                        v = vh[j];
                    }
                }
                vtype.push(v['attributes']);
                vstatus.push(v['attributes']['current_status']);
                vstation.push(v['relationships']['stop']['data']['id']);
                vst_url = url+"stops/?filter[id]="+v['relationships']['stop']['data']['id'];
                for (let j=0; j<stops.length; j++) {
                    if (stops[j]['id'] == v['relationships']['stop']['data']['id']) {
                        statName = stops[j]['attributes']['name'];
                    }
                }
                vstatName.push("<a href=\"https://mbta.com/stops/"+v['relationships']['stop']['data']['id']+"\" target=\"_blank\" rel=\"noopener noreferrer\">"+statName+"</a>");
                vla.push(v['attributes']['latitude']);
                vlo.push(v['attributes']['longitude']);
                }
            dummy += 1;
        }}
        
    label += "<hr>";
    label += " <a href=\"https://mbta.com/stops/"+station+"\" target=\"_blank\" rel=\"noopener noreferrer\">"+statNameCurr+"</a>";
    label += "\t\t"+current_time+"\n";
    if (direction.includes(0)) {
    label += "<hr>";
    for (let j=0; j<direction.length; j++) {
        if (direction[j] == 0) {
        label += mk_map_URL(dest[direction[j]],vla[j],vlo[j])+"\t"+pred_arr_times[j]+"\t"+vehicle_type(lines[j],vtype[j])+"\t"+mk_line_URL(lines[j])+"\t\t"+undef_format(vstatus[j])+"\t"+undef_format(vstatName[j]);
        }}}
    if (direction.includes(1)) {
    label += "<hr>";
    for (let j=0; j<direction.length; j++) {
        if (direction[j] == 1) {
        label += mk_map_URL(dest[direction[j]],vla[j],vlo[j])+"\t"+pred_arr_times[j]+"\t"+vehicle_type(lines[j],vtype[j])+"\t"+mk_line_URL(lines[j])+"\t\t"+undef_format(vstatus[j])+"\t"+undef_format(vstatName[j]);
        }}}
    label += "<hr>";

    alerts = await getAlerts(station, routes);
    if (alerts.length>0) {
        for (let i=0; i<alerts.length; i++) {
            label += alerts[i].attributes.short_header;
            }
        label += "<hr>";
        }
    
    document.getElementById("results").innerHTML = "".concat(...label);
    document.getElementById("warnLabel").innerHTML = "";
    }
    
function get_sign(a) {
    if (a > 0 && a < 0.5) {return " ARR\t";}
    if (a >= 0.5 && a < 1) {return " APPR\t";}
    if (a >= 1) {return Math.round(a)+" min\t";}
    if (a > -10 && a <= 0) {return "BOARD \t";}
    if (a <= -10) {return "--- \t";}
    }
    
////////////////////////////////////
// Get Alerts                   //
////////////////////////////////////
async function getAlerts(station, route) {
    const alerts_url = url+"alerts/?filter[stop]="+station+"&filter[route]="+route;
    const alerts = (await getFeed(alerts_url))['data'];
    return alerts;
    }

//////////////////////////////
// Stops view               //
//////////////////////////////
async function predStops() {
    document.getElementById("warnLabel").innerHTML = "Please wait...";
    const rt_url = url+"stops/?filter[route]="+document.getElementById("route").value;
    const r = (await getFeed(rt_url))['data'];
        
    if (r.length > 0) {
    let label = "\n Route: <a href=\"https://mbta.com/schedules/"+document.getElementById("route").value+"/line\" target=\"_blank\" rel=\"noopener noreferrer\">"+document.getElementById("route").value+"</a>\n";
    label += "\n Station ID\tName\n";
    
    for (let i=0; i<r.length; i++) {
        label += " <a href=\"#\" onclick=javascript:setStops('"+r[i]['id']+"');>"+r[i]['id']+"</a>";
        label += "\t<a href=\"https://mbta.com/stops/"+r[i]['id']+"\" target=\"_blank\" rel=\"noopener noreferrer\">"+r[i]['attributes']['name']+"</a>\n";
    }
    document.getElementById("results").innerHTML = "".concat(...label);
    
    }  else {
        document.getElementById("results").innerHTML = "\n No Routes with this ID currently in operation\n";}
    document.getElementById("warnLabel").innerHTML = "";
    }
    
function setStops(stop) {
    document.getElementById('station').value=stop;
    getRoutes(stop);
}

//////////////////////////////
// Routes view              //
//////////////////////////////
function predRoutes() {
    const stat_id = document.getElementById("station").value;
    initCookie('currStation',document.getElementById("station").value);
    initCookie('currRoute', document.getElementById("route").value);
    getRoutes(stat_id);
}

async function getRoutes(stat_id) {
    const st_url = url+"stops/?filter[id]="+stat_id;
    const station = (await getFeed(st_url))['data'][0]['attributes']['name'];
    
    const rt_url = url+"routes/?filter[stop]="+stat_id;
    const r = (await getFeed(rt_url))['data'];
    
    if (r.length > 0) {
        clearList("route");
        for (let i=0; i<r.length; i++) {
            document.getElementById("route").innerHTML +="<option value=\"" + r[i]['id'] + "\">" + r[i]['id'] + "</option>";
            }
    predSigns();
    }  else {
        document.getElementById("results").innerHTML = "\n No Routes currently in operation through this station\n";}
    }
    
//////////////////////////////
// Vehicle view             //
//////////////////////////////
function predVehicle() {
    const id = document.getElementById("vehicle").value;
    get_vehicle(id, "");
    }
    
function refresh_vehicle() {
    if (document.getElementById("vehicle").value !== "") {
    get_vehicle(document.getElementById("vehicle").value, document.getElementById("route").value);}
    }
    
async function get_vehicle(id, line) {
    document.getElementById("warnLabel").innerHTML = "Please wait...";
    setCookie('currVehicle',id,100);
    document.getElementById('vehicle').value=id;
    const v_url = url+"vehicles/?filter[label]="+id;
    const v = (await getFeed(v_url))['data'];
    
    if (line == "") {
        art_url = url+"routes/";
        art = (await getFeed(art_url))['data'];
        routes = []
        for (f=0; f<art.length; f++) {
            routes.push(art[f]['id']);}
        line = routes;}
    /*
    else if (line.slice(0,2) == "CR") {
        pattern = /^[RGBy]/;
        cr = v.filter(item => pattern.test(item.id));
        console.log(cr);
        if (cr) {v = cr;}
        }
    */
      
    if (v.length > 0) {
    label = "<hr>";
    label += " Vehicle label: "+id+"\n";
    
    for (let i=0; i<v.length; i++) {
    if (v[i]['relationships']['stop']['data'] != null && (line.includes(v[i]['relationships']['route']['data']['id']) || line.slice(0,2) == "CR")) {   
    let stat_id = v[i]['relationships']['stop']['data']['id']
    let st_url = url+"stops/?filter[id]="+stat_id;
    let station = (await getFeed(st_url))['data'][0]['attributes']['name'];
    label += "<hr>";
    label += " Vehicle ID: "+v[i]['id']+"\n";
    label += "\n Route: "+mk_line_URL(v[i]['relationships']['route']['data']['id'])+" \n";
    label += " Occupancy: "+format_null(v[i]['attributes']['occupancy_status'])+" \n";
    label += " Stop sequence: "+v[i]['attributes']['current_stop_sequence']+" \n";
    label += " Status: "+v[i]['attributes']['current_status']+" "+mk_stop_URL(stat_id, station)+" (Stop ID: "+v[i]['relationships']['stop']['data']['id']+")\n";
    label += " Time: "+format_time(v[i]['attributes']['updated_at'])+" \n";
    label += "\n Latitude: "+v[i]['attributes']['latitude']+" \n";
    label += " Longitude: "+v[i]['attributes']['longitude']+" \n";
    label += " Bearing: "+v[i]['attributes']['bearing']+" \n";
    label += " Speed: "+format_null(v[i]['attributes']['speed'])+" mph\n";
    label += " Number of carriages: " + v[i]['attributes']['carriages'].length +"\n";
    label += " Vehicle type: "+vehicle_model(v[i], v[i]['relationships']['route']['data']['id'])+" \n";
    label += mk_map_URL("Map current location", v[i]['attributes']['latitude'], v[i]['attributes']['longitude'])+"\n";
    label += mk_streetview_URL("StreetView", v[i]['attributes']['latitude'], v[i]['attributes']['longitude'],v[i]['attributes']['bearing'])+"\n";
    label += await (mk_gmaps_dir_URL("Route map", v[i]['relationships']['route']['data']['id']))+"\n";
    
    mk_gmaps_dir_URL
    //label += embed_map(gkey,v[i]['attributes']['latitude'],v[i]['attributes']['longitude']);
    }}
    document.getElementById("results").innerHTML = "".concat(...label);
    
    }  else {
        document.getElementById("results").innerHTML = "\n No Vehicle with this ID currently in operation\n";}
    document.getElementById("warnLabel").innerHTML = "";
    }

//////////////////////////////
// Vehicle types and models //
//////////////////////////////
function vehicle_type(line, veh) {
    let tag = "N/A";
    let code = 0;
    if (typeof veh == 'object') {
    if (veh.hasOwnProperty('label') == true) {
        code = veh['label'];
    if (line == "Red") {
        if (code < 1700) {
            tag = "O1";}
        if (code >= 1700 && code < 1800) {
            tag = "O1b";}
        if (code >= 1800 && code < 1900) {
            tag = "O2";}
        if (code >= 1900) {
            tag = "N";}
        }
    else if (line == "Orange") {
        if (code < 1400) {
            tag = "O";}
        if (code >= 1400) {
            tag = "N";}
        }
    else if (line.slice(0,5) == "Green") {
        if(code.length > 4) {
            code_first = code.slice(0,4);}
        if ((code_first >= 3600) || (code_first<=3719)) {
            tag = "O1";}
        if ((code_first >= 3800)  || (code_first <= 3894)) {
            tag ="O2";}
        if (code_first >= 3900) {
            tag = "N";}
        }
    else {
        tag = code;
        }
    return "<a href='javascript:get_vehicle(\""+code+"\",\""+line+"\");'>"+tag+'</a>';
    }} else {return "\t";}
    }

function vehicle_model(v, line) {
    const id = v['id'][0];
    const a = v['attributes']['label'];
    
    if (id == "R") {
        if ((a >= 1500) && (a<=1523)) {
            return "Pullman-Standard (1969-1970)";}
        if ((a >= 1600) && (a<=1651)) {
            return "Pullman-Standard (1969-1970)";}
        if ((a >= 1700) && (a<=1757)) {
            return "UTDC (1987-1989)";}
        if ((a >= 1800) && (a<=1885)) {
            return "Bombardier (1993-1994)";}
        if ((a >= 1900) && (a<=2151)) {
            return "CRRC (2021-2025)";}
    }
    
    if (id == "O") {
        if ((a >= 1400) && (a<=1551)) {
            return "CRRC (2018-2025)";}
    }
    
    if (id == "B") {
        return "Siemens 700-series (2007-2009)";
    }

    if (id == "G") {
        if(a.length > 4) {
            a = a.slice(0,4);}
        if ((a >= 3600) && (a<=3699)) {
            return "Kinki Sharyo Type 7 LRV (1986-1988)";}
        if ((a >= 3700) && (a<=3719)) {
            return "Kinki Sharyo Type 7 LRV (1997)";}
        if ((a >= 3800) && (a <= 3894)) {
            return "AnsaldoBreda Type 8 LRV (1998-2007)";}
        if (a >= 3900) {
            return "CAF USA Type 9 LRV (2018-2020)";}
    }
    if (id == "y") {
        if (a>=600 && a<=910) {
            return "Bus: D40LF (2006-2008)";}
        else if (a>=1200 && a<=1224) {
            return "Bus: DE60LFR (2010)";}
        else if (a>=1400 && a<=1459) {
            return "Bus: XDE40 - Hybrid (2014-1015)";}
        else if (a>=1600 && a<=1774) {
            return "Bus: XN40 - GNG (2016-2017)";}
        else if ((a>=1775 && a<=1924) || (a>=3000 && a<=3005)) {
            return "Bus: XDE40 - Hybrid (2016-2017)";}
        else if (a>=1250 && a<=1293) {
            return "Bus: XDE60 - Hybrid (2016-2017)";}
        else if (a==1294) {
            return "Bus: XDE60 - Hybrid - Extended Battery (2018)";}
        else if (a>=1295 && a<=1299) {
            return "Bus: XE60 - Battery Electric (2019)";}
        else if (a>=1925 && a<=2118) {
            return "Bus: XDE40 - Hybrid (2019-2020)";}
        else if  (a>=3100 && a<=3159) {
            return "Bus: XDE40 - Hybrid (2020)";}
        else if (a>=1300 && a<=1344) {
            return "Bus: XDE60 - Hybrid (2022-2023)";}
        else if  (a>=3200 && a<=3359) {
            return "Bus: XDE40 - Hybrid (2023)";}
        else if  (a>=4200 && a<=4231) {
            return "Bus: XE40 - Electric - Left side doors (2024-2025)";}
        else if  (a>=4300 && a<=4347) {
            return "Bus: XE40 - Electric (2024-2026)";}
        else {
            return "Bus: N/A";}
        }
        
    if (line.slice(0,2) == "CR") {
        if (a>1700 && a<1725) {
           return "Kawasaki CTC-4 Control Trailer Coaches (1990-1991)";}
        else if (a>1800 && a<1828) {
           return "Rotem CTC-5 Control Trailer Coaches (2012-2014)";}
        else if (a>=1828 && a<1870) {
           return "Rotem CTC-5 Control Trailer Coaches (2022-2024)";}
        else if (a>=1025 && a<1037) {
           return "Morrison-Knudsen F40PH-3C (1991-1993, Reb: 2003-2004 / 2019-2024)";}
        else if (a>=1050 && a<1076) {
           return "EMD F40PH-3C (1987-1988, Reb: 2001-2003 / 2019-2024)";}
        else if (a>=1115 && a<1140) {
           return "GMD GP40MC (1973-1975-1993, Reb: 1997)";}
        else if (a>=2000 && a<2040) {
           return "MPI HSP-46 (2014-2014)";}
       }
    else {
        return "N/A";}
    }
    
function set_SL_CT(line) {
    if (line == "741") { return "SL1";}
    if (line == "742") { return "SL2";}
    if (line == "743") { return "SL3";}
    if (line == "751") { return "SL4";}
    if (line == "749") { return "SL5";}
    if (line == "746") { return "SLW";}
    if (line == "747") { return "CT2";}
    if (line == "708") { return "CT3";}
    else {return line;}
}

////////////////////////
// Query DB for stops //
////////////////////////
async function get_stop(stop) {
    const st_url = url+"stops/?filter[id]="+stop;
    const s = (await getFeed(st_url))['data'];
    sleep(100);
    if (s.length == 0) {return '';}
    else {return s[0]['attributes']['name'];}
    }
    
async function get_stops(stop, stops) {
    let name = "";
    for (let j=0; j<stops.length; j++) {
        if (stops[j]['id'] == stop) {
            name = stops[j]['attributes']['name'];
            }}
    return name;
    }

///////////////
// make URLs //
///////////////
function mk_map_URL(a, la, lo) {
    return "\n <a href=\"https://www.google.com/maps/@?api=1&map_action=map&layer=transit&zoom=18&center="+la+","+lo+"\" target=\"_blank\" rel=\"noopener noreferrer\">"+a+"</a>";
    }
    
function mk_streetview_URL(a, la, lo, h) {
    return "\n <a href=\"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint="+la+","+lo+"&heading="+h+"\" target=\"_blank\" rel=\"noopener noreferrer\">"+a+"</a>";
    }

async function mk_gmaps_dir_URL(a, line) {
    const grt_url = url+"stops/?filter[route]="+line;
    const r = (await getFeed(grt_url))['data'];
    const orig = r[0]['attributes']['latitude']+","+r[0]['attributes']['longitude'];
    const dest = r[r.length-1]['attributes']['latitude']+","+r[r.length-1]['attributes']['longitude'];
    return "\n <a href=\"https://www.google.com/maps/dir/?api=1&origin="+orig+"&destination="+dest+"&travelmode=transit&zoom=16\" target=\"_blank\" rel=\"noopener noreferrer\">"+a+"</a>";
    }

function mk_line_URL(line) {
    return "<a href=\"https://mbta.com/schedules/"+line+"/line\" target=\"_blank\" rel=\"noopener noreferrer\">"+set_SL_CT(line)+"</a>";
    }

function mk_stop_URL(a, b) {
    return "<a href=\"https://mbta.com/stops/"+a+"\" target=\"_blank\" rel=\"noopener noreferrer\">"+b+"</a>"
    }
/*
function embed_map(gkey, lat, long) {
    return "\n\n <iframe width=\"450\" height=\"250\" frameborder=\"0\" style=\"border:0\" referrerpolicy=\"no-referrer-when-downgrade\"    src=\"https://www.google.com/maps/embed/v1/view?key="+gkey+"&center="+lat+","+long+"&zoom=17\"</iframe>";
    }
*/

///////////////////////////////////////
// Date/Time/length/coord formatting //
///////////////////////////////////////
function getCoords() {
    return new Promise((resolve, reject) =>
        navigator.geolocation.getCurrentPosition(resolve, handleError, geolocationOptions));
    }
    
const geolocationOptions = {
    enableHighAccuracy: true,
    timeout: 10000, // Wait max 5 seconds
    maximumAge: 0   // Don't use cached location
};
    
function handleError(error) {
    let errorMessage = '';
    switch (error.code) {
        case error.PERMISSION_DENIED:
            errorMessage = "User denied the request for Geolocation.";
            break;
        case error.POSITION_UNAVAILABLE:
            errorMessage = "Location information is unavailable.";
            break;
        case error.TIMEOUT:
            errorMessage = "The request to get user location timed out.";
            break;
        case error.UNKNOWN_ERROR:
            errorMessage = "An unknown error occurred.";
            break;
    }
    console.error(errorMessage);
    console.error(`Error Code: ${error.code}, Message: ${error.message}`);
    document.getElementById('warnLabel').textContent = errorMessage;
}

function undef_format(a) {
    if (a === undefined)
        { return "";}
    else
        {return a;}
    }
    
function get_sec(time_str) {
    t = time_str.split(':');
    return t[0] * 3600 + t[1] * 60 + t[2]*1;
    }
    
function get_current_time() {

    function get_dig(a) {
        let secs = "";
        if (a<10) {
        secs = "0"+a;}
        else {
        secs = a;}
        return secs;}
        
    let now = new Date(Date.now());
    let secs = "";
    if (now.getSeconds()<10) {
        secs = "0"+now.getSeconds();}
    else {
        secs = now.getSeconds();}
    return get_dig(now.getHours())+":"+get_dig(now.getMinutes())+":"+get_dig(now.getSeconds());
    }

function format_time(time_str) {
    //2024-01-24T18:40:02-05:00
    const t = time_str.split(/-|T|:/);
    //return t[1]+"/"+t[2]+"/"+t[0]+"  "+t[3]+":"+t[4]+":"+t[5]
    return t[3]+":"+t[4]+":"+t[5];
}

function get_radius(a) {
    return a*0.02/1.609;
}

function get_distance(la1, lo1, la2, lo2, a) {

    function r(a) {
        return a*Math.PI/180;
        }
    
    R = 6378.13685;
    return (1000*(Math.acos((Math.sin(r(la1)) * Math.sin(r(la2))) + (Math.cos(r(la1)) * Math.cos(r(la2))) * (Math.cos(r(lo2) - r(lo1)))) * R)).toFixed(a);
    }

function format_null(a) {
    if (a == null) {
        return "--";}
    else {
        return a;}
    }
    
function clearList(elementID) {
    for (i=document.getElementById(elementID).options.length*1; i>=0; i--) {
            document.getElementById(elementID).remove(i);}
    }
    
///////////////////////
// Sleep //
///////////////////////
function sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
   }

///////////////////////
// Cookie management //
///////////////////////
function setCookie(cname, cvalue, exdays) {
  let d = new Date();
  d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
  let expires = "expires="+d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);}
    }
  return "";
}

function eraseCookie(name) {
    document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

function initCookie(name, value) {
    let x = getCookie(name);
        if (x=="") {setCookie(name,value,100);}
    }
    
function eraseAllCookies() {
    eraseCookie('homeStation');
    eraseCookie('homeRoute');
    eraseCookie('currStation');
    eraseCookie('currRoute');
    eraseCookie('currVehicle');
    }

function initCookies() {
    initCookie('homeStation','place-knncl');
    initCookie('homeRoute', 'Red');
    initCookie('currStation','place-knncl');
    initCookie('currRoute', 'Red');
    initCookie('currVehicle', '');
    }

///////////////////////
// Initialization    //
///////////////////////
function setHome() {
    initCookies();
    document.getElementById("station").value = getCookie('homeStation');
    document.getElementById("route").innerHTML = "<option value=\"" + getCookie('homeRoute') + "\">" + getCookie('homeRoute') + "</option>";
    document.getElementById("vehicle").value = "";
    }

function init() {
    initCookies();
    document.getElementById("station").value = getCookie('currStation');
    clearList("route");
    document.getElementById("route").innerHTML = "<option value=\"" + getCookie('currRoute') + "\">" + getCookie('currRoute') + "</option>";
    document.getElementById("vehicle").value = getCookie('currVehicle');
}

window.onload = init;

