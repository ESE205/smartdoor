const express = require('express');
const app = express();
cont mysql = require('mysql');
const utils = require('util');
const conn = mysql.createConnection({
    host: 'xxx',
    user: 'xxx',
    password: 'xxx',
    database: 'xxx',
    port: xxx
});

const query = utils.promisify(conn.query).bind(conn);

const bodyParser = require('body-parser');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended:false}));
const MessagingResponse = require('twilio').twiml.MessagingResponse;

let i = 0;

let access = [];

let map = {};

app.get('/textuser/:photoName', async (req,res) => {

access[i] = 'pending';
map[req.params.photoName] = i;
console.log('texting for authorization with photo ${req.params.photoName}');
const accountSid = '###';
const authToken = '###';
const client = require('twilio')(accountSid, authToken);
    
//conn.connect((err) => {
//    if(err) {
//        console.log('Unable to connect to mysql');
//        throw err;
//  }
//        });
    
let qString = 'INSERT INTO door (intruderid, decision, tmstmp) VALUES (?,?,?)';
await conn.query(qString, [req.params.photoName, 'pending', Date.now()];                 

const message = await client.messages
    .create({
        body: 'This person is at your door, do you want to let them in?',
        from: '###',
        mediaUrl: 'static ip',
        to: '###'
    });

console.log(message.sid);
res.send("OK");

});

app.post('/sms', (req,res) => {
    const twiml = new MessagingResponse();

    twiml.message('Thank you for your response.  The visitor is being informed of your decision');

    res.writeHead(200, {'Content-Type': 'text/xml'});
    if(JSON.parse(req.body.AddOns).results.marchex_sentiment.result.result>0.5){
        access[i] = 'approved';
    }
    else {
        access[i] = 'denied';
    }
    i++;
    res.end(twiml.toString());

});

app.get('/accessstatus/:filename', async (req, res) => {

    res.json({
        "status": access[map[req.params.filename]]
    });

});

app.listen(1337);

