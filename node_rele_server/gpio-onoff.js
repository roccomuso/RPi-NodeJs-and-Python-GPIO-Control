
var Gpio = require("onoff").Gpio; // npm install onoff --save

var config = require('./config.json'); // file di configurazione
var pin = config.pin; // pin fisico 11, ma header 17, occhio alla differenza.

// FUNZIONI PER INTERAGIRE CON IL RELAY COLLEGATO AD UN GPIO pin

led = new Gpio(pin, 'out');

exports.get = function(pin){ // perchè questo file gpio-onoff.js è incluso esternamente
	var value = led.readSync();
	var stato = (value == 1) ? "on": "off";
	
	console.log("Get status: "+stato);
	return {response_code: 200, new_state: stato, path: "/get"};
	
};


exports.on = function(pin){
	led.writeSync(1);
	console.log("Pin ON");
	return {response_code: 200, new_state: "on", path: "/on"};
};

exports.off = function(pin){
	led.writeSync(0);
	console.log("Pin OFF");
	return {response_code: 200, new_state: "off", path: "/off"};
};

exports.toggle = function(pin){

var stato = 0;

/*
   led.read(function (err, value) { // Asynchronous read.
		if (err) throw err;

		led.write(value ^ 1, function (err) { // Asynchronous write.
		  if (err) throw err;
		  stato = value ^ 1;
		  console.log('Pin new value: '+stato);
		});
  });
*/

stato = led.readSync() ^ 1;

led.writeSync(stato);
console.log("Toggle: "+stato);

if (stato == 1)
	return {response_code: 200, new_state: "on", path: "/toggle"};
else
	return {response_code: 200, new_state: "off", path: "/toggle"};
	
};

