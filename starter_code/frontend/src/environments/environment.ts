/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-1ain35b8.us', // the auth0 domain prefix
    audience: 'coffee', // the audience set for the auth0 app
    clientId: '57Kw4MnJE8uzUZ7QmMiMpEpEADhQoOvQ', // the client id generated for the auth0 app
    callbackURL: 'https://localhost:4200', // the base url of the running ionic application. 
  }
};
