import machine as m
from machine import Timer
import network
import urequests as requests
import ujson
import utime
import ntptime

led=m.Pin(2, m.Pin.OUT)

def toggle_led():
    if led.value() == 1:
        led.off()
    else:
        led.on()
        
def turnon_led():
    led.on()
        
def start_timer2():
    print("Starting timer 2...")
    t2 = Timer(-1)
    t2.init(period=1000, mode=Timer.PERIODIC, callback=lambda t:toggle_led())

#print("Starting timer 1")
#t1 = Timer(-1)
#t1.init(period=8000, mode=Timer.ONE_SHOT, callback=lambda t:start_timer2())

def set_time(timezone):
    ntptime.settime()
    otime = list(utime.localtime())
    otime[3] = otime[3]+timezone
    ntime = utime.mktime(tuple(otime))
    utime.localtime(ntime)
   
def get_now_time():
    now = utime.localtime()
    st = "{day:02d}/{month:02d}/{year} - {hour:02d}:{minute:02d}:{sec:02d}"
    return st.format(day = now[2], month=now[1], year=now[0], hour=now[3], minute=now[4], sec=now[5])
    

def connect_wifi():
    conn = network.WLAN(network.STA_IF)
    conn.active(True)
    conn.connect('Farinhaki', 'farinhaki2424527')

    t1 = Timer(-1)
    t1.init(period=100, mode=Timer.PERIODIC, callback=lambda t:toggle_led())
    while (conn.isconnected() == False):
        print("Waiting connection...")
        utime.sleep_ms(500)
    t1.deinit()
    turnon_led()
    print("Connected!")

def get_usd_quotation():
    response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")

    print("Return="+str(response.status_code))

    usd_response = ujson.loads(response.text)["bpi"]['USD']
    print("Rate USD="+usd_response['rate'])
    
def get_brl_quotation():
    response=requests.get("https://economia.awesomeapi.com.br/json/all/USD-BRL,BTC-BRL,ETH-BRL")
    print("Return="+str(response.status_code))
    print("=="+get_now_time()+"==")
    brl_usd = ujson.loads(response.text)["USD"]["ask"]
    brl_eth = ujson.loads(response.text)["ETH"]["ask"]
    brl_btc = ujson.loads(response.text)["BTC"]["ask"]
    print("   * USD: "+brl_usd+"\n   * ETH:"+brl_eth+"\n   * BTC: "+brl_btc)
    print("============\\\\===========")
    
def start_quote_timer():
    get_brl_quotation()
    tq = Timer(-1)
    tq.init(period=30*60*1000, mode=Timer.PERIODIC, callback= lambda t:get_brl_quotation())
    

connect_wifi()
set_time(-3)
start_quote_timer()