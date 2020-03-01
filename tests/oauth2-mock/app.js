const { OAuth2Server } = require('oauth2-mock-server');
const MOCK_IDP_PORT = 3000;
const MOCK_IDP_HOST = 'localhost';
const MOCK_API_AUDIENCE = 'mock_api_audience';

async function startserver(server) {
  	

	// Generate a new RSA key and add it to the keystore
	server.issuer.keys.generateRSA();

	service = server.service;

	service.once('beforeTokenSigning', (token, req) => {
		token.payload.aud = MOCK_API_AUDIENCE;
	});

	// Start the server
  	await server.start(MOCK_IDP_PORT, MOCK_IDP_HOST);
  	console.log('Issuer URL:', server.issuer.url);
  	return "done!";
}

let server = new OAuth2Server();

startserver(server);
