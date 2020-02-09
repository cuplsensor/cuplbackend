const { OAuth2Server } = require('oauth2-mock-server');

let server = new OAuth2Server();

// Generate a new RSA key and add it to the keystore
server.issuer.keys.generateRSA();

service = server.service;

service.once('beforeTokenSigning', (token, req) => {
	token.payload.aud = 'theapi';
});

// Start the server
server.start(3000, 'localhost');
console.log('Issuer URL:', server.issuer.url);