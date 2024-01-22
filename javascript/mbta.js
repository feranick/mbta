url = "https://api-v3.mbta.com/";
key = "91944a70800a4bcabe1b9c2023d12fc8";
headers = {'Accept': 'application/json', 'x-api-key': key};

async function getFeed(url) {
    const res = await fetch(url);
    const obj = await res.json();
    return obj;
    }

async function predSigns() {
    document.getElementById("warnLabel").innerHTML = "Please wait...";
    label = []
    station = document.getElementById("station").value;
    routes = document.getElementById("route").value;
    
    line = routes.split(" ");
    
    //############################
    //# get all stops/vehicles
    //############################
    stops_url = url+"stops/";
    stops = (await getFeed(stops_url))['data'];
    
    vh_url = url+"vehicles/";
    vh = (await getFeed(vh_url))['data'];
    
    st_url = url+"stops/?filter[id]="+station;
    s = (await getFeed(st_url))['data'];
    statNameCurr = s[0]['attributes']['name'];
    
    rt_url = url+"routes/?filter[id]="+line;
    dest = (await getFeed(rt_url))['data'][0]['attributes']['direction_destinations'];
    
    pr_url = url+"predictions/?filter[stop]="+station;
    p = (await getFeed(pr_url))['data'];
    
    if (p.length ==0) {
        label += "\n No data currently available. Try again later.\n";
        label += " Possible cause: no service available at this time\n";
        document.getElementById("results").innerHTML = "".concat(...label);
        return;
        }
    
    dummy = 0;
    pred_arr_times = [];
    direction = [];
    status = [];
    vstation = [];
    vstatName =[];
    vstatus = [];
    vtype = [];
    locat = [];
    lines = [];
    vla = [];
    vlo = [];
    
    let now = new Date(Date.now());
    current_time = now.getHours()+":"+now.getMinutes()+":"+now.getSeconds();
    document.getElementById("results").innerHTML = "Please wait...";
        
    for (let i=0; i<p.length; i++) {
        id_line = p[i]['relationships']['route']['data']['id'];
        
        //if id_line in line and dummy < dP.list_items:
        //if (id_line == line && dummy < 10) {
        if (line.includes(id_line) == true && dummy < 10) {
            if (p[i]['attributes']['arrival_time'] !== null) {
                arr_time = p[i]['attributes']['arrival_time'].slice(11).slice(0,-6);
                arr_time_mins = (get_sec(arr_time) - get_sec(current_time))/60;
            } else {
                arr_time_mins = "";
                }
            
            lines.push(id_line);
            direction += p[i]['attributes']['direction_id'];
            pred_arr_times.push(get_sign(arr_time_mins));
            

            if (p[i]['relationships']['vehicle']['data']['id'] !== null) {
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
        } else {
            console.log("Fail");
        }}
    label += "<hr>";
    label += "<a href=\"https://mbta.com/stops/"+station+"\" target=\"_blank\" rel=\"noopener noreferrer\">"+statNameCurr+"</a>";
    label += "\t\t"+current_time+"\n";
    label += "<hr>";
    for (let j=0; j<direction.length; j++) {
        if (direction[j] == 0) {
        label += mk_coord_URL(dest[direction[j]],vla[j],vlo[j])+"\t"+pred_arr_times[j]+"\t"+train_type(lines[j],vtype[j])+"\t"+mk_line_URL(lines[j])+"\t\t"+vstatus[j]+"\t"+vstatName[j]+"\n";
        }}
    label += "<hr>";
    for (let j=0; j<direction.length; j++) {
        if (direction[j] == 1) {
        label += mk_coord_URL(dest[direction[j]],vla[j],vlo[j])+"\t"+pred_arr_times[j]+"\t"+train_type(id_line,vtype[j])+"\t"+mk_line_URL(lines[j])+"\t\t"+vstatus[j]+"\t"+vstatName[j]+"\n";
        }}
    label += "<hr>";
    document.getElementById("results").innerHTML = "".concat(...label);
    document.getElementById("warnLabel").innerHTML = "";
    }
    
async function predStops() {
    document.getElementById("warnLabel").innerHTML = "Please wait...";
    rt_url = url+"stops/?filter[route]="+document.getElementById("route").value;
    r = (await getFeed(rt_url))['data'];
        
    if (r.length > 0) {
    label = "\n Route: <a href=\"https://mbta.com/schedules/"+document.getElementById("route").value+"/line\" target=\"_blank\" rel=\"noopener noreferrer\">"+document.getElementById("route").value+"</a>\n";
    label += "\n Station ID\tName\n";
    
    for (let i=0; i<r.length; i++) {
        label += " "+r[i]['id']+"\t<a href=\"https://mbta.com/stops/"+r[i]['id']+"\" target=\"_blank\" rel=\"noopener noreferrer\">"+r[i]['attributes']['name']+"</a>\n";
    }
    document.getElementById("results").innerHTML = "".concat(...label);
    
    }  else {
        document.getElementById("results").innerHTML = "\n No Routes with this ID currently in operation\n";}
    document.getElementById("warnLabel").innerHTML = "";
    }

async function predRoutes() {
    stat_id = document.getElementById("station").value;
    st_url = url+"stops/?filter[id]="+stat_id;
    station = (await getFeed(st_url))['data'][0]['attributes']['name'];
    
    rt_url = url+"routes/?filter[stop]="+stat_id;
    r = (await getFeed(rt_url))['data'];
    
    if (r.length > 0) {
        label = "\n Routes going through: <a href=\"https://mbta.com/stops/"+stat_id+"\" target=\"_blank\" rel=\"noopener noreferrer\">"+station+" ("+stat_id+")</a>\n\n ";
        
        for (let i=0; i<r.length; i++) {
            label += r[i]['id']+" ";
            }
    
    document.getElementById("results").innerHTML = "".concat(...label);
    
    }  else {
        document.getElementById("results").innerHTML = "\n No Routes currently in operation through this station\n";}
    }

function predVehicle() {
    id = document.getElementById("vehicle").value;
    get_vehicle(id);
    }
    
async function get_vehicle(id) {
    document.getElementById("warnLabel").innerHTML = "Please wait...";
    //v_url = url+"vehicles/?filter[label]="+document.getElementById("vehicle").value;
    v_url = url+"vehicles/?filter[label]="+id;
    v = (await getFeed(v_url))['data'];
    
    if (v.length > 0) {
    label = "\n Vehicle label: "+document.getElementById("vehicle").value+"\n";
    
    for (let i=0; i<v.length; i++) {
    stat_id = v[i]['relationships']['stop']['data']['id']
    st_url = url+"stops/?filter[id]="+stat_id;
    station = (await getFeed(st_url))['data'][0]['attributes']['name'];
    
    label += " Vehicle ID: "+v[i]['id']+"\n";
    label += "\n Route: "+v[i]['relationships']['route']['data']['id']+" \n";
    label += " Occupancy:"+v[i]['attributes']['occupancy_status']+" \n";
    label += " Longitude:"+v[i]['attributes']['longitude']+" \n";
    label += " Bearing: "+v[i]['attributes']['bearing']+" \n";
    label += " Latitude: "+v[i]['attributes']['latitude']+" \n";
    label += " Speed: "+v[i]['attributes']['speed']+" \n";
    label += " Vehicle type: "+get_type(v[i]['id'])+" \n";
    label += "\n Stop sequence:"+v[i]['attributes']['current_stop_sequence']+" \n";
    label += " Status: "+v[i]['attributes']['current_status']+" "+mk_stop_URL(stat_id, station)+" (Stop ID: "+v[i]['relationships']['stop']['data']['id']+")\n";
    label += " Time: "+v[i]['attributes']['updated_at']+" \n";
    label += mk_coord_URL("Current location", v[i]['attributes']['latitude'], v[i]['attributes']['longitude']);
    
    }
    document.getElementById("results").innerHTML = "".concat(...label);
    
    }  else {
        document.getElementById("results").innerHTML = "\n No Vehicle with this ID currently in operation\n";}
    document.getElementById("warnLabel").innerHTML = "";
    }

function get_type(v) {
    if (v[0] == "y") {
        a = v.slice(1)*1;
        if (a>=600 && a<=910) {
            return "Bus: D40LF";}
        else if (a>=1200 && a<=1224) {
            return "Bus: DE60LFR";}
        else if ((a>=1400 && a<=1459) || (a>=1775 && a<=2118) || (a>=3000 && a<=3005) || (a>=3100 && a<=3359) || (a>=1200 && a<=1224)) {
            return "Bus: XDE40 - Hybrid";}
        else if (a>=1600 && a<=1774) {
            return "Bus: XN40 - GNG";}
        else if ((a>=1250 && a<=1294) || (a>=1300 && a<=1344)) {
            return "Bus: XDE60 - Hybrid";}
        else if (a>=1295 && a<=1299) {
            return "Bus: XE60 - Battery Electric";}
        else {
            return "Bus: N/A";}
        }
    else {
        return "N/A";}
    }
    
function get_sec(time_str) {
    t = time_str.split(':');
    return t[0] * 3600 + t[1] * 60 + t[2]*1;
    }

function get_sign(a) {
    if (a > 0 && a < 0.5) {return " ARR\t";}
    if (a >= 0.5 && a < 1) {return " APPR\t";}
    if (a >= 1) {return Math.round(a)+" min\t";}
    if (a > -10 && a <= 0) {return "BOARD \t";}
    if (a <= -10) {return "--- \t";}
    }
    
async function get_stop(stop) {
    st_url = url+"stops/?filter[id]="+stop;
    s = (await getFeed(st_url))['data'];
    sleep(100);
    if (s.length == 0) {return '';}
    else {return s[0]['attributes']['name'];}
    }

function mk_coord_URL(a, la, lo) {
    return "<a href=\"https://www.google.com/maps/search/?api=1&query="+la+"%2C"+lo+"\" target=\"_blank\" rel=\"noopener noreferrer\">"+a+"</a>";
    }
    
function mk_line_URL(line) {
    return "<a href=\"https://mbta.com/schedules/"+line+"/line\" target=\"_blank\" rel=\"noopener noreferrer\">"+line+"</a>";
    }

function mk_stop_URL(a, b) {
    return "<a href=\"https://mbta.com/stops/"+a+"\" target=\"_blank\" rel=\"noopener noreferrer\">"+b+"</a>"
    }

function train_type(line, veh) {
    code = veh['label'];
    if (line == "Red") {
        if (code < 1800) {
            return "O1";}
        if (code >= 1800 && code < 1900) {
            return "O2";}
        if (code >= 1900) {
            return "N";}
        }
    if (line == "Orange") {
        if (code < 1400) {
            return "O";}
        if (code >= 1400) {
            return "N";}
        }
    if (line.slice(0,5) == "Green") {
        if (code < 3900) {
            return "O";}
        if (code >= 3900) {
            return "N";}
        }
    if (line.slice(0,2) == "CR") {
        return "CR";}
    else {
        //return code;}
        return "<a href='javascript:get_vehicle(code);'>"+code+'</a>';}
        }
    
function sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
   }
