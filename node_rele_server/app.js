var express = require('express'); // Usiamo libreria express per facilitarci il routing // npm install express --save
var app = express();

var relay = require('./gpio-onoff.js');

var config = require('./config.json'); // file di configurazione
var porta = config.porta;


app.get('/toggle', function (req, res) { // processiamo richiesta get verso /toggle

  // risposta in JSON
  res.json(relay.toggle());

});

app.get('/on', function (req, res) { // processiamo richiesta get verso /toggle

  // risposta in JSON
  res.json(relay.on());

});

app.get('/off', function (req, res) { // processiamo richiesta get verso /toggle

  // risposta in JSON
  res.json(relay.off());

});

app.get('/get', function (req, res) { // processiamo richiesta get verso /toggle

  // risposta in JSON
  res.json(relay.get());

});

// Express route for any other unrecognised incoming requests
app.get('*', function(req, res) {
  res.status(404).send('Unrecognised API call');
});

var server = app.listen(porta, function () { // server in ascolto sulla porta 5000


  var host = server.address().address;
  var port = server.address().port;

  console.log('App in ascolto su http://%s:%s', host, port);

});