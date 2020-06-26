/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: '<api_server_url>', // the running FLASK api server url
  auth0: {
    url: '<auth0 domain>', // the auth0 domain prefix
    audience: '<api audience>', // the audience set for the auth0 app
    clientId: '<client secret>', // the client id generated for the auth0 app
    callbackURL: '<callback_url>', // the base url of the running ionic application. 
  }
};
