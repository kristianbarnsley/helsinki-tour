import streamlit as st
import json
from PIL import Image
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

# Add Font Awesome for icons
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">', unsafe_allow_html=True)

# Define valid team passwords
TEAM_PASSWORDS = {
    "team1pass": "Team 1",
    "team2pass": "Team 2"
}

ADMIN_PASSWORD = "adminpass"

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'team_name' not in st.session_state:
    st.session_state.team_name = None
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# Create data directory if it doesn't exist
if not os.path.exists("data"):
    os.makedirs("data")

# Initialize or load team progress
TEAM_PROGRESS_FILE = "data/team_progress.json"
if not os.path.exists(TEAM_PROGRESS_FILE):
    initial_progress = {
        "teams": {
            "Team 1": {"current_challenge": 0, "answers": {}},
            "Team 2": {"current_challenge": 0, "answers": {}}
        }
    }
    with open(TEAM_PROGRESS_FILE, "w") as f:
        json.dump(initial_progress, f)

def load_team_progress():
    with open(TEAM_PROGRESS_FILE, "r") as f:
        return json.load(f)

def save_team_progress(progress):
    with open(TEAM_PROGRESS_FILE, "w") as f:
        json.dump(progress, f)

# Define challenges with UI configurations
challenges = [
    {
        "title":"Introduciton",
        "media": {
            "video": "Intro-video.mp4",
            "description": ""
        },
        "tasks": [
            "none",
        ],
        "ui_elements":{},
    },
    {
        "title":"Swedish founding & the village years: Sederholm House",
        "location": "Sederholm House",
        "location_link": "https://maps.app.goo.gl/zE5UYnvFgHAY15jZA",
        "media": {
            "audio": "Sederholm House.m4a",
            "description": "Audio Tour"
        },
        "transcript": "Take a look at the pale-yellow stone walls of Johan Sederholm's 1757 townhouse and you're meeting Helsinki when it was still a tiny Swedish fishing village called Helsingfors. King Gustav I of Sweden founded the town in 1550 to steal Baltic trade from Tallinn, but for two centuries it limped along: plague, fires, and shifting sandbanks all kept merchants away. Sederholm was part of the first generation that finally made the gamble pay. Picture the creak of masts just beyond the door, barrels of tar and salted herring stacked to the rafters, and Swedish‑speaking clerks scratching tallies by candle‑light. This house is the oldest intact building downtown; its thick walls are Stockholm’s signature stamped on a place that hadn’t yet dreamed of becoming a capital.",
        "tasks": [
            "Play swedish word association against eachother. Each team must alternate in saying a word associated with Sweden",
        ],
        "ui_elements":{
            "radio": {
                "enabled": True,
                "label": "Did your team win?",
                "options": ["Yes", "No"]
            },
        },
    },
    {
        "title":"Swedish founding & the village years: Tori Quarters",
        "location": "Tori Quarters",
        "location_link": "https://maps.app.goo.gl/mnSRCTRdDg2K9BF6A",
        "media": {
            "audio": "Tori Quarters.m4a",
            "description": "Audio Tour"
        },
        "transcript": "Stroll the cobbled lanes between Pohjoisesplanadi, Katariinankatu and Sofiankatu and let the pastel façades rewind time to the 18th‑century “Age of Sail.” Here were chandlers, coopers, rope‑makers, and taverns serving rye ale to skippers waiting on the tide. Finland’s tar, timber and fur shipped out; French wine, Dutch tiles and Caribbean sugar flowed in. These narrow plots, rebuilt after fires, obey a medieval logic: shop on the street, warehouse in back, residence on top. Listen for the clang of a blacksmith’s hammer, the multilingual chatter of Swedes, Finns, Germans and Russians, and the gulls that have patrolled the harbour for 300 years. Torikorttelit is Helsinki’s original shopping mall—only the fashions have changed.",
        "tasks": [
            "Find a modern item for sale that would have also been available in the 1700s. Take photos with your items and the shopkeeper who sold them to you.",
        ],
        "ui_elements":{
            "file_upload": {
                "enabled": True,
                "types": ["jpg", "jpeg", "png"],
                "multiple": True,
                "label": "Upload your photos of the items and shopkeeper"
            }
        },
    },
    {
        "title":"Fortress era & strategic awakening: Market Square quay viewpoint",
        "location": "Market Square quay viewpoint",
        "location_link": "https://maps.app.goo.gl/LgzAyuXX7qqxZAjf7",
        "media": {
            "audio": "Market Square quay viewpoint.m4a",
            "description": "Audio Tour"
        },
        "transcript": "Face south across the glittering harbour. The low grassy ramparts you can just make out on the horizon are Suomenlinna. Sweden began the fort in 1748, naming it Sveaborg—“Castle of the Swedes.” Overnight, sleepy Helsingfors became a naval construction yard: 7,000 soldiers, masons and prisoners quarried granite, forged cannon and launched gunboats. Locals bartered fish and butter; soldiers spent their pay in the taverns behind you. By the 1780s half the town’s jobs depended on the fortress. Helsinki’s first true growth spurt wasn’t politics, but defence economics—and it happened right in this viewfinder.",
        "tasks": [
            "Find a local who has visited Suomenlinna Fortress & get them to tell you something interesting about it.",
        ],
        "ui_elements":{
            "text_input": {
                "enabled": True,
                "type": "text_area",
                "label": "What is interesting about the fortress?"
            },
        },
    },
    {
        "title":"Fortress era & strategic awakening: Old Market hall (Vanha kauppahalli)",
        "location": "Old Market hall (Vanha kauppahalli)",
        "location_link": "https://maps.app.goo.gl/VFJZLBeXSa4DcZrG7",
        "media": {
            "audio": "Old Market hall (Vanha kauppahalli).m4a",
            "description": "Audio Tour"
        },
        "transcript": "Pull open the iron‑framed doors (built 1889) and breathe in a time capsule of Baltic appetite. Smoked vendace from Lake Päijänne, cloudberry jam hauled from Lapland bogs, reindeer sausages, Russian blini caviar, and coffee—the drink Finns would one day consume more per capita than anyone on Earth. In the late 1800s this hall civilised the open‑air fish market: tiled counters, ice blocks and modern hygiene kept cholera at bay. Dockworkers in blue woollen caps, Russian officers craving rye bread, Estonian wives hunting spices, and bourgeois ladies ordering oysters for dinner parties—everyone met under these arches. What you taste here is Helsinki’s edible history.",
        "tasks": [
            "Find, picture and eat the 3 most Finnish snack you can find",
            "Locate a food stall and discover the price of 'muikku' (small fried fish)"
        ],
        "ui_elements":{
            "file_upload": {
                "enabled": True,
                "types": ["jpg", "jpeg", "png"],
                "multiple": True,
                "label": "Upload your photos of the snacks"
            },
            "text_input": {
                "enabled": True,
                "type": "short",
                "label": "Price of Muikku"
            },
        },
    },
    {
        "title":"Fortress era & strategic awakening: Pohjoisesplanadi / Unioninkatu",
        "location": "Pohjoisesplanadi / Unioninkatu",
        "location_link": "https://maps.app.goo.gl/HJWNG3rznrQxqSab8",
        "media": {
            "audio": "Bilingual St name signs.m4a",
            "description": "Audio Tour"
        },
        "transcript": "Check the street plaque. Today it’s in Finnish & Swedish, but from 1809 to 1917 it also bore Cyrillic—a silent scar from the Finnish War. Why did Russia invade? Napoleon had just bullied Tsar Alexander I into blockading Britain; Sweden refused, so Russia marched north to push the frontier away from vulnerable St Petersburg. In March 1808 Russian troops crossed the ice into Helsinki, seized the town without a shot, and besieged the great sea‑fortress Sveaborg offshore. When the fortress capitulated that May, Sweden’s hold on Finland was broken; the Treaty of Fredrikshamn (1809) made the region a Russian Grand Duchy. Alexander now needed a safer, more defensible capital than Turku (which was Finland's capital during Swedish rule) —one closer to his army and navy—so he picked Helsinki and hired architect C. L. Engel to give it the white‑columned look you see up the hill. Wooden huts were replaced by stone blocks, Esplanadi boulevard was carved straight through the medieval grid, and Orthodox onion domes (red brick church you can see towards the east) soon joined Lutheran spires. So these street signs mark more than a corner—they mark the day Helsinki’s language, skyline and destiny pivoted eastward.",
        "tasks": [
            "Find a local -  who speaks primarily Finnish, Swedish, or Russian. Get them to teach you how to say 'Helsinki is amazing' in their respective languages, then attempt to repeat the phrases back on video. Have them rate your pronunciation on a scale of 1-10.",
            "Bonus if you can find someone to teach you the phrase in any of the other languages"
        ],
        "ui_elements":{
            "file_upload": {
                "enabled": True,
                "types": ["mp4", "mov", "jpg", "jpeg", "png"],
                "multiple": True,
                "label": "Upload a video of your performance and any bonuses"
            },
            "text_input": {
                "enabled": True,
                "type": "short",
                "label": "How did they rate you?"
            },
        },
    },
    {
        "title":"Fortress era & strategic awakening: Havis Amanda Fountain",
        "location": "Havis Amanda Fountain",
        "location_link": "https://maps.app.goo.gl/rGxpUnMQ47mcJC85A",
        "media": {
            "audio": "Havas Amanda Fountain.m4a",
            "description": "Audio Tour"
        },
        "transcript": "Ville Vallgren’s bronze mermaid rises from a swirl of sea lions, forever climbing ashore like a new‑born Helsinki. Unveiled in 1908, she scandalised conservatives (“too French, too naked!”) but students adopted her as their May Day goddess—every spring they wash and “cap” her with a white graduation cap. Her sea‑spray tells two stories: Helsinki’s eternal bond with the Baltic, and a young city daring to flaunt modern art and modern morals just nine years before independence.",
        "tasks": [
            "Take a video singing “kiss from a rose” by Seal, with a Seal",
            "Find out the statue’s nickname among locals",
            "Ask a local about the tradition involving this fountain on May Day",
        ],
        "ui_elements":{
            "file_upload": {
                "enabled": True,
                "types": ["mp4", "mov", "jpg", "jpeg", "png"],
                "multiple": True,
                "label": "Upload a video of your performance"
            },
            "text_input": {
                "enabled": True,
                "type": "short",
                "label": "What is the nickname of the fountain?"
            },
            "text_input": {
                "enabled": True,
                "type": "text_area",
                "label": "What happens on May Day?"
            },
        },
    },
    {
        "title":"Fortress era & strategic awakening: Kappeli Restaurant",
        "location": "Kappeli Restaurant",
        "location_link": "https://maps.app.goo.gl/NRhbYZnjfQFuBs3x7",
        "media": {
            "audio": "Kappeli Restaraunt.m4a",
            "description": "Audio Tour"
        },
        "transcript": "This glass pavilion opened as a humble summer café; by the 1890s it buzzed with writers, composers and politicians plotting Finland’s future. Jean Sibelius scribbled waltzes here; gossip‑columnist Zacharias Topelius eavesdropped on ministers over crayfish and schnapps. Peer up at the ceiling frescoes—angels toasting with champagne. Kappeli is where art, politics and good food collided, proving that revolutions can start with a really decent onion soup.",
        "tasks": [
            "Order a beer, and record a travel monolouge to camera in the style of your favourite travel TV presenter",
        ],
        "ui_elements":{
            "file_upload": {
                "enabled": True,
                "types": ["mp4", "mov"],
                "multiple": True,
                "label": "Upload a video of your monolouge"
            },
        },
    },
    {
        "title":"Fortress era & strategic awakening: Esplanadi Park ",
        "location": "Esplanadi Park ",
        "location_link": "https://maps.app.goo.gl/ipYx2eVk2gH6ZzU46",
        "media": {
            "audio": "Esplanadi Park.m4a",
            "description": "Audio Tour"
        },
        "transcript": "Before 1812 this was a scruffy field outside town. After Russia moved the capital here, Engel carved a grand promenade between two rows of elms. Think of it as Helsinki’s living room: military bands in the 19th century, tango orchestras in the 1930s, silent disco today. In the park stands poet J. L. Runeberg (1885), pen poised; nearby are statues of playwright Aleksis Kivi and the park’s designer Engel himself. Every stone bench has hosted daydreams, declarations of love and political debates. Pause, and you’re sitting in the cross‑section of leisure and nation‑building.",
        "tasks": [
            "Find and photograph the statue of Finnish national poet Johan Ludvig Runeberg.",
            "Bonus points: Identify and photograph the pastry named after him.",
        ],
        "ui_elements":{
            "file_upload": {
                "enabled": True,
                "types": ["mp4", "mov", "jpg", "jpeg", "png"],
                "multiple": True,
                "label": "Upload your photos"
            },
        },
    },
    {
        "title":"Swedish founding & village years: Old Church Park",
        "location": "Old Church Park",
        "location_link": "https://maps.app.goo.gl/5mVfY3EmQXkeVX1h7",
        "media": {
            "audio": "Old Church Park.m4a",
            "description": "Audio Tour"
        },
        "transcript": "Beneath this tranquil lawn lie the mass graves of the Great Plague of 1710, when two‑thirds of Helsinki’s 1,600 residents died in four months. The ground was then outside the town walls; carts of bodies rattled here at night, torches sputtering in the sea wind. The simple wooden Old Church (1826) came later, but a handful of mossy 18th‑century headstones still peek through the grass. Listen for the hush that falls even on busy days—Helsinkians call it Ruttopuisto, “Plague Park,” and tread a little lighter in memory.",
        "tasks": [
            "none",
        ],
        "ui_elements":{},
    },
    {
        "title":"Cold‑War neutrality & the Helsinki Accords: Presidential Palace ",
        "location": "Presidential Palace ",
        "location_link": "https://maps.app.goo.gl/E7x373cTPb4jbJPSA",
        "media": {
            "audio": "Presidential Palace.m4a",
            "description": "Audio Tour"
        },
        "transcript": "Before the mansion, a timber salt warehouse stood here; it was demolished when merchant J. H. Heidenstrauch erected his grand residence in 1816 —soon purchased by the Russian crown and later adopted as the Finnish President’s residence (1919). On 30 July 1975 those state rooms shimmered as 35 heads of state—Gerald Ford, Leonid Brezhnev, Helmut Schmidt, Harold Wilson —dined ahead of signing the Helsinki Final Act, the capstone of Finland’s Cold‑War neutrality. Picture waiters weaving between tables laden with vendace roe and cloudberry parfait while a string quartet tried to drown the murmur of translators. Outside, schoolchildren waved every flag in Europe. For one summer night, Helsinki was the diplomatic centre of the world.",
        "tasks": [
            "none",
        ],
        "ui_elements":{},
    },
    {
        "title": "Arrival of Christianity: Helsinki Cathedral (Helsingin tuomiokirkko)",
        "location": "Helsinki Cathedral",
        "location_link": "https://maps.app.goo.gl/iGnXZ2JW1AkYpmvW6",
        "media": {
            "audio": "Helsinki Cathedral.m4a",
            "description": "Audio Tour"
        },
        "transcript": "Those white columns weren’t always white: when Engel began the church in 1830 it was green, and it was named after Russia’s patron saint, Nicholas. Renamed and repainted after independence, it now symbolises Finnish Lutheran identity—and, by extension, Finnish perseverance. Christianity arrived in Finland around 1155 with the legend of Bishop Henry; for centuries Swedish bishops ruled the spiritual roost. The cathedral’s Greek‑revival form says: “We’re northern, but we speak classical grandeur.” Climb the steps—each one is a photograph waiting to happen—and look back at the cityscape it commands.",
        "tasks": [
            "Take a photo of the most hardcore apostle & explain why",
            "Find and record the year the Cathedral was completed"
        ],
        "ui_elements": {
            "file_upload": {
                "enabled": True,
                "types": ["jpg", "jpeg", "png"],
                "multiple": True,
                "label": "Upload your photos of the apostles"
            },
            "text_input": {
                "enabled": True,
                "type": "text_area",
                "label": "Explain your choice of apostle"
            },
            "number_input": {
                "enabled": True,
                "label": "Enter the year the Cathedral was completed",
                "min_value": 1800,
                "max_value": 1900
            }
        }
    },
    {
        "title":"Independence & civil‑war shock: House of the Estates",
        "location": "House of the Estates",
        "location_link": "https://maps.app.goo.gl/g5H45VCV6ZzaN9a37",
        "media": {
            "audio": "House of Estates (1).m4a",
            "description": "Audio Tour",
            "additional_audio" : ["House of Estates (2).m4a", "House of Estates (3).m4a"],
        },
        "transcript": "Stand beneath the gilded pediment of Athena guiding Finland: this Renaissance‑revival hall is where the story of Finnish statehood hits its dramatic climax. The last mile to freedom From 1809 Finland had been a Russian Grand Duchy with its own laws and currency but a tsar on the throne. By 1917 that arrangement was wobbling: Russification drives (1899–1905) tried to curb Finnish autonomy and sparked mass protests. General strikes in 1905 and 1917 spread new ideas—parliamentary democracy, women’s suffrage (granted here in 1906, the first in Europe). Then the Russian February Revolution 1917 toppled the tsar. Finland’s parliament (the Eduskunta) claimed supreme power; Petrograd said “not so fast.” By December the Bolsheviks were busy with their own revolution and civil war. Seizing the moment, Finnish deputies gathered in this chamber on 6 December 1917 and voted 100–88 to “hereby declare Finland an independent republic.” The chandeliers shook with applause. From parchment to powder‑smoke Independence was inked, but unity was not. Two Finlands emerged: “Reds” – urban workers and tenant farmers, inspired by socialism and backed (lightly) by Russian Bolsheviks still garrisoned in the country. “Whites” – landowners, middle classes and many farmers, led by General Mannerheim and quietly armed by Germany. On 27 January 1918 the Reds raised the lantern on Helsinki’s Workers’ Hall; the Whites answered with railway seizures in the north. For three bleak months Finland became a war zone of trench lines, armoured trains and brother‑against‑brother firefights. The Reds initially held Helsinki, using this very building as a command post; the Whites and a German expeditionary force retook the city in April after street battles that scarred nearby façades. Aftermath in these walls Victorious Whites reconvened here in June 1918 to draft a constitution—eventually choosing a republic over a monarchy. Outside, graves were still fresh and the economy in tatters, but the political map was set: a sovereign Finland, wary of both Germany and Soviet Russia, determined never to fight itself again. So linger a moment: the parquet floor you’re standing on heard both the cheers of independence and the boots of civil war. Few rooms in Europe have hosted such rapid swings from revolution to reconciliation.",
        "tasks": [
            "none",
        ],
        "ui_elements":{},
    },
    {
        "title":"World‑War II & post‑war rebuild: Bank of Finland façade",
        "location": "Bank of Finland façade",
        "location_link": "https://maps.app.goo.gl/Qrku3vuGy1zZZtjT8",
        "media": {
            "audio": "WW2 (1).m4a",
            "description": "Audio Tour",
            "additional_audio" : ["WW2 (2).m4a", "WW2 (3).m4a"],
        },
        "transcript": "If you look closely at the granite blocks, you will notice dozens of small craters. They are the physical residue of Soviet air‑raids carried out in February 1944 and they provide a concise introduction to Finland’s remarkably complex experience of the Second World War. The first phase, known internationally as the Winter War, began on 30 November 1939. After signing the Molotov‑Ribbentrop Pact with Nazi Germany, the Soviet Union demanded a territorial buffer to protect Leningrad; the Finnish government refused, and Soviet forces crossed the border. Finland, vastly out‑numbered, nonetheless held the Red Army for 105 winter days. The Moscow Peace Treaty of March 1940 ended hostilities but forced Finland to cede roughly 11 per cent of its territory, including the province of Karelia. The country remained sovereign, yet the settlement left a profound sense of unfinished business on both sides. That unresolved tension explains why Finland soon found itself in a second conflict, the Continuation War, which began in June 1941 after Germany invaded the Soviet Union. Finland now sought, with German material support, to recover the land lost the previous year. Although the Finnish leadership always emphasised an independent war‑aim—regaining Karelia rather than pursuing Hitler’s broader objectives—the alliance placed Helsinki within the Soviet bomber radius. The scars on this wall record the heaviest of those raids. On the night of 26–27 February 1944, Soviet aircraft dropped some 1,500 bombs on the city. Anti‑aircraft batteries on Tähtitorninmäki hill managed to deter part of the force, but several bombs exploded close to the Bank, driving shrapnel deep into the façade where it remains today. They are a rare example of wartime damage deliberately preserved as a memorial. Military fortunes shifted rapidly that summer. With the Red Army advancing on all fronts, Finland negotiated an armistice that took effect on 4 September 1944. The terms required the Finns to expel German troops from Lapland and to pay reparations worth 300 million US dollars (in 1938 prices), largely in the form of ships and industrial machinery. Many of those contracts were financed, supervised and signed inside the Bank you are facing. Economists often argue that meeting the schedule of these payments laid the administrative groundwork for Finland’s post‑war industrialisation. Thus, a few square metres of damaged stone encapsulate a double narrative: a small state’s refusal to surrender its independence in 1939 and its equally pragmatic decision, five years later, to disengage from a dangerous alliance and accept costly reparations rather than occupation. In granite and shrapnel, the façade offers an unusually direct lecture on how Finland fought two wars, lost territory, preserved democracy, and paid its way back into peacetime.",
        "tasks": [
            "Outside the bank, record a 2 minute tech startup elivator pitch for a exicting new Finnish business of your creation",
        ],
        "ui_elements":{
            "file_upload": {
                "enabled": True,
                "types": ["mp4", "mov"],
                "multiple": True,
                "label": "Upload a video of your pitch"
            },
        },
    },
    {
        "title":"Work and Play: Thirsty Scholar pub",
        "location": "Thirsty Scholar pub",
        "location_link": "https://maps.app.goo.gl/TyeZFE1edKbTtPVo9",
        "media": {
            "audio": "Thirsty Scholar Pub.m4a",
            "description": "Audio Tour",
        },
        "transcript": "Although this corner pub opened only recently, its location on Yliopistonkatu—literally “University Street”—puts it in the long shadow of the University of Helsinki, founded in 1640 in Turku and transferred here after the Great Fire of 1827. From the moment the first lecture was delivered in 1828, students have treated beer as their unofficial study aid and social glue. In the 19th century the university’s “nations” (osakunnat)—regional student societies—met in back‑room beer halls to debate politics and plan song‑festivals. Many of the speeches that shaped Finland’s nationalist awakening were first tried out over tankards no different from the pints poured here. When Finland gained independence in 1917, undergraduates marched past this block wearing the white caps that still appear every Vappu (May Day), the annual carnival of spring, scholarship and, inevitably, beer. During the Cold War, the nearby Old Student House echoed with ideological arguments—some fiery, some fogged by malt. Today’s students still crowd into bars like the Thirsty Scholar after afternoon lectures, carrying forward a tradition in which academic life and lager coexist without apology. Raise a glass and you are participating in the convivial side of Finnish higher education—a lineage as old as the university itself.",
        "tasks": [
            "Ask the bartender for a recommended Finnish drink to share. Take a photo with your drinks",
        ],
        "ui_elements":{
            "file_upload": {
                "enabled": True,
                "types": ["jpg", "jpeg", "png"],
                "multiple": True,
                "label": "Upload a photo with your drinks"
            },
        },
    },
    {
        "title":"EU integration & creative‑city boom: Kiasma Museum",
        "location": "Kiasma Museum",
        "location_link": "https://maps.app.goo.gl/xQUwF3Lce7wTSAsd9",
        "media": {
            "audio": "Kiasma Museum & Amos Rex.m4a",
            "description": "Audio Tour",
        },
        "transcript": "Kiasma’s silver curves (1998, Steven Holl) slice the skyline like a Nordic aurora; underground, Amos Rex (2018) bubbles up as alien skylights in Lasipalatsi Square. Their exhibitions pulse with VR installations, climate art and queer Sámi photography—proof that post‑EU Helsinki sells ideas, not timber or tar. Since joining the EU in 1995, Finland has won the world’s happiest‑country ranking seven times, Nokia’s ringtone became the soundtrack of a decade, and Helsinki bagged World Design Capital 2012. Inside these walls you’ll see why: creativity is the new fortress.",
        "tasks": [
            "Identify a famous Finnish artist whose works are exhibited here & record a Finnish person teaching you how to pronounce their name & giving you marks out of 10",
        ],
        "ui_elements":{
            "file_upload": {
                "enabled": True,
                "types": ["mp4", "mov", "jpg", "jpeg", "png"],
                "multiple": True,
                "label": "Upload a video of your performance"
            },
            "text_input": {
                "enabled": True,
                "type": "short",
                "label": "What score did they give you?"
            },
        },
    },
    {
        "title":"Coming to a close: Senate Square",
        "location": "Senate Square",
        "location_link": "https://maps.app.goo.gl/2G3rRhEWNooL4i3j7",
        "media": {
            "audio": "Senate Square Ensemble.m4a",
            "description": "Audio Tour",
        },
        "transcript": "Make a slow 360°. North: the cathedral’s green domes (Faith & Russian rule). East: the Government Palace (Imperial administration). South: Sederholm House and the Tori Quarters (Swedish merchants). West: the University (Enlightenment and nation‑building). Under your feet: cobbles where Red Guards dug trenches in 1918; above your head: gulls riding Baltic winds that once carried salt, Russian frigates, and today’s cruise ferries. In a single square you have walked five centuries—from Gustav Vasa’s fish‑market gamble to EU‑era design labs. Whatever tomorrow brings—fusion reactors, ice‑free Arctic routes, maybe a Martian embassy—Helsinki will add it to this silent conversation of stone and sky. Kiitos for touring with us; the rest of the story is yours to write.",
        "tasks": [
            "none",
        ],
        "ui_elements":{},
    },
]

# Create uploads directory if it doesn't exist
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Login screen
if not st.session_state.authenticated:
    st.title("Helsinki City Tour Challenge")
    st.write("Please enter your team password to begin:")
    
    def handle_login():
        if st.session_state.password == ADMIN_PASSWORD:
            st.session_state.authenticated = True
            st.session_state.is_admin = True
        elif st.session_state.password in TEAM_PASSWORDS:
            st.session_state.authenticated = True
            st.session_state.team_name = TEAM_PASSWORDS[st.session_state.password]
        else:
            st.session_state.login_error = "Invalid password. Please try again."
    
    if 'login_error' not in st.session_state:
        st.session_state.login_error = None
    
    st.text_input("Team Password", type="password", key="password", on_change=handle_login)
    if st.button("Login"):
        handle_login()
    
    if st.session_state.login_error:
        st.error(st.session_state.login_error)
        st.session_state.login_error = None
    
    st.stop()

# Load team progress
team_progress = load_team_progress()

# Admin view
if st.session_state.is_admin:
    st.title("Admin Dashboard")
    
    # Display team progress
    for team_name, team_data in team_progress["teams"].items():
        st.header(f"Team: {team_name}")
        st.write(f"Current Challenge: {team_data['current_challenge'] + 1} of {len(challenges)}")
        st.progress((team_data['current_challenge'] + 1) / len(challenges))
        
        # Display answers
        if team_data['answers']:
            st.subheader("Answers:")
            for answer_key, answer_value in team_data['answers'].items():
                st.write(f"**{answer_key}**:")
                # Check if the answer is a list of files (image uploads)
                if isinstance(answer_value, list):
                    for filename in answer_value:
                        file_path = os.path.join("uploads", f"{team_name}_{filename}")
                        if os.path.exists(file_path):
                            try:
                                image = Image.open(file_path)
                                st.image(image, caption=filename, use_column_width=True)
                            except Exception as e:
                                st.write(f"Could not display {filename}: {str(e)}")
                        else:
                            st.write(f"File not found: {filename}")
                else:
                    st.write(answer_value)
        else:
            st.write("No answers submitted yet.")
        
        st.markdown("---")
    
    # Add refresh button
    if st.button("Refresh Data"):
        team_progress = load_team_progress()
        st.success("Data refreshed!")
        st.rerun()
    
    # Clear data button
    if st.button("Clear All Team Data"):
        initial_progress = {
            "teams": {
                "Team 1": {"current_challenge": 0, "answers": {}},
                "Team 2": {"current_challenge": 0, "answers": {}}
            }
        }
        save_team_progress(initial_progress)
        st.success("All team data has been cleared!")
        st.rerun()
    
    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.is_admin = False
        st.rerun()
    
    st.stop()

# Initialize session state with team's progress
if 'current_challenge' not in st.session_state:
    st.session_state.current_challenge = team_progress["teams"][st.session_state.team_name]["current_challenge"]
if 'answers' not in st.session_state:
    st.session_state.answers = team_progress["teams"][st.session_state.team_name]["answers"]

def validate_challenge_completion(challenge, answers):
    """Check if all required fields for the current challenge are completed."""
    missing_fields = []
    challenge_key = challenge['title']
    
    for element_type, config in challenge['ui_elements'].items():
        if config.get('enabled', False):
            field_key = f"{challenge_key}_{element_type}"
            if field_key not in answers or not answers[field_key]:
                missing_fields.append(config.get('label', element_type))
    
    return missing_fields

# App title and description
st.title("Helsinki City Tour")


# Show other teams' progress
st.sidebar.title("Team Progress")
st.sidebar.write(f"Welcome, {st.session_state.team_name}!")
for team_name, team_data in team_progress["teams"].items():
    st.sidebar.write(f"{team_name}: Challenge {team_data['current_challenge'] + 1} of {len(challenges)}")
    st.sidebar.progress((team_data['current_challenge'] + 1) / len(challenges))

# Add update button
if st.sidebar.button("Refresh Progress"):
    team_progress = load_team_progress()
    st.rerun()

# Display current challenge
current = challenges[st.session_state.current_challenge]
st.header(f"{current['title']}")
if 'location' in current:
    location_html = f'<a href="{current["location_link"]}" target="_blank" style="text-decoration: none; color: inherit;"><span style="display: inline-flex; align-items: center; gap: 5px;"><i class="fas fa-map-marker-alt"></i> {current["location"]}</span></a>'
    st.markdown(location_html, unsafe_allow_html=True)

# Display media if available
if 'media' in current:
    media = current['media']
    if 'video' in media:
        video_path = os.path.join(script_dir, "media", media['video'])
        if os.path.exists(video_path):
            st.write(media['description'])
            st.video(video_path)
    elif 'audio' in media:
        audio_path = os.path.join(script_dir, "media", media['audio'])
        if os.path.exists(audio_path):
            st.write(media['description'])
            st.audio(audio_path)
        if 'additional_audio' in media:
            for additional_audio in media['additional_audio']:
                additional_path = os.path.join(script_dir, "media", additional_audio)
                if os.path.exists(additional_path):
                    st.audio(additional_path)
        if 'transcript' in current:
            with st.expander("Transcript"):
                st.write(current['transcript'])


# Display tasks
if current["tasks"][0] != "none":
    st.write("Tasks:")
    for i, task in enumerate(current["tasks"], 1):
        st.write(f"{i}. {task}")

# Dynamic UI rendering based on challenge configuration
if 'ui_elements' in current:
    for element_type, config in current['ui_elements'].items():
        if config.get('enabled', False):
            if element_type == 'file_upload':
                uploaded_files = st.file_uploader(
                    config.get('label', "Upload your files"),
                    type=config.get('types', ["jpg", "jpeg", "png"]),
                    accept_multiple_files=config.get('multiple', False)
                )
                if uploaded_files:
                    # Convert to list if single file
                    if not isinstance(uploaded_files, list):
                        uploaded_files = [uploaded_files]
                    
                    # Save files and track in session state
                    saved_files = []
                    for uploaded_file in uploaded_files:
                        file_path = os.path.join("uploads", f"{st.session_state.team_name}_{uploaded_file.name}")
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        saved_files.append(uploaded_file.name)
                        st.success(f"Saved {uploaded_file.name}")
                    
                    # Update session state with uploaded files
                    st.session_state.answers[f"{current['title']}_{element_type}"] = saved_files
                    team_progress["teams"][st.session_state.team_name]["answers"] = st.session_state.answers
                    save_team_progress(team_progress)
            
            elif element_type == 'text_input':
                if config.get('type') == 'text_area':
                    answer = st.text_area(config.get('label', "Enter your answer"))
                else:
                    answer = st.text_input(config.get('label', "Enter your answer"))
                if answer:
                    st.session_state.answers[f"{current['title']}_{element_type}"] = answer
                    team_progress["teams"][st.session_state.team_name]["answers"] = st.session_state.answers
                    save_team_progress(team_progress)
                    st.success("Answer saved!")
            
            elif element_type == 'number_input':
                answer = st.number_input(
                    config.get('label', "Enter a number"),
                    min_value=config.get('min_value', 0),
                    max_value=config.get('max_value', 100),
                    step=config.get('step', 1)
                )
                if answer:
                    st.session_state.answers[f"{current['title']}_{element_type}"] = answer
                    team_progress["teams"][st.session_state.team_name]["answers"] = st.session_state.answers
                    save_team_progress(team_progress)
                    st.success("Answer saved!")
            
            elif element_type == 'radio':
                answer = st.radio(
                    config.get('label', "Select an option"),
                    options=config.get('options', [])
                )
                if answer:
                    st.session_state.answers[f"{current['title']}_{element_type}"] = answer
                    team_progress["teams"][st.session_state.team_name]["answers"] = st.session_state.answers
                    save_team_progress(team_progress)
                    st.success("Answer saved!")
            
            elif element_type == 'checkbox':
                answer = st.checkbox(config.get('label', "Check if completed"))
                if answer:
                    st.session_state.answers[f"{current['title']}_{element_type}"] = answer
                    team_progress["teams"][st.session_state.team_name]["answers"] = st.session_state.answers
                    save_team_progress(team_progress)
                    st.success("Answer saved!")
            
            elif element_type == 'selectbox':
                answer = st.selectbox(
                    config.get('label', "Select an option"),
                    options=config.get('options', [])
                )
                if answer:
                    st.session_state.answers[f"{current['title']}_{element_type}"] = answer
                    team_progress["teams"][st.session_state.team_name]["answers"] = st.session_state.answers
                    save_team_progress(team_progress)
                    st.success("Answer saved!")
            
            elif element_type == 'slider':
                answer = st.slider(
                    config.get('label', "Select a value"),
                    min_value=config.get('min_value', 0),
                    max_value=config.get('max_value', 100),
                    step=config.get('step', 1)
                )
                if answer:
                    st.session_state.answers[f"{current['title']}_{element_type}"] = answer
                    team_progress["teams"][st.session_state.team_name]["answers"] = st.session_state.answers
                    save_team_progress(team_progress)
                    st.success("Answer saved!")

# Navigation buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Previous") and st.session_state.current_challenge > 0:
        st.session_state.current_challenge -= 1
        team_progress["teams"][st.session_state.team_name]["current_challenge"] = st.session_state.current_challenge
        save_team_progress(team_progress)
        st.rerun()

with col2:
    # Check if all required fields are completed
    missing_fields = validate_challenge_completion(current, st.session_state.answers)
    
    if missing_fields:
        st.warning("Please complete all required fields before proceeding:")
        for field in missing_fields:
            st.write(f"• {field}")
    
    if st.button("Next", disabled=bool(missing_fields)) and st.session_state.current_challenge < len(challenges) - 1:
        st.session_state.current_challenge += 1
        team_progress["teams"][st.session_state.team_name]["current_challenge"] = st.session_state.current_challenge
        save_team_progress(team_progress)
        st.rerun()

# Progress indicator
st.progress((st.session_state.current_challenge + 1) / len(challenges))
st.write(f"Stage {st.session_state.current_challenge + 1} of {len(challenges)}")

# Logout button
if st.sidebar.button("Logout"):
    st.session_state.authenticated = False
    st.session_state.team_name = None
    st.rerun() 