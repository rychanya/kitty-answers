import { App, reactive } from "vue";
import createAuth0Client, { Auth0Client } from "@auth0/auth0-spa-js";

createAuth0Client({
  domain: process.env.VUE_APP_AUTH0_DOMAIN,
  client_id: process.env.VUE_APP_AUTH0_CLIENT_KEY,
  redirect_uri: window.location.origin,
  audience: process.env.VUE_APP_AUTH0_AUDIENCE,
});
