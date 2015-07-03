# RPi-NodeJs-and-Python-GPIO-Control
Scritps in Node Js and Python to create a listening server and control a specific Raspberry Pi GPIO pin.

# Node Js way: app.js

To run it at startup on your Raspberry Pi, add the following line to <code>/etc/rc.local</code>:<br/>
<code>sudo node home/dir/path/app.js &</code>

(remember first to install node js on the RPi)

The routing is handled in <b>app.js</b>. The functions are written in <b>gpio-onoff.js</b>. The configuration parameters are 2, <em>port</em> and <em>pin</em>, defined in <b>config.json</b>.

The server will listen on the port defined in <b>config.json</b>. Ready to get these HTTP request:

<ul>
<li><code>GET /on</code>: turns ON the GPIO pin defined in <b>config.json</b>.</li>
<li><code>GET /off</code>: turns OFF the GPIO pin.</li>
<li><code>GET /toggle</code>: toggles the GPIO pin.</li>
<li><code>GET /get</code>: get the GPIO pin status.</li>
</ul>

# PYTHON way: relay.py

To run it at startup on your Raspberry Pi, add the following line to <code>/etc/rc.local</code>:<br/>
<code>python home/dir/path/relay.py -c listen 5000 &</code>

The server will listen on the 5000 port. Ready to get these HTTP request:<br/>

<ul>
<li><code>GET /accendi</code>: turns ON the GPIO pin.</li>
<li><code>GET /spegni</code>: turns OFF the GPIO pin.</li>
<li><code>GET /toggle</code>: toggles the GPIO pin.</li>
<li><code>GET /blink</code>: blink the GPIO pin with default values.</li>
</ul>
