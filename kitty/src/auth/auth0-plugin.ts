import { App } from "vue";
import createAuth0Client from "@auth0/auth0-spa-js";

export const Auth0Plugin = {
  async install(app: App) {
    console.log(process.env)
    const auth0 = await createAuth0Client({
      domain: "dev-w0syo8i3.eu.auth0.com",
      // domain: process.env.AUTH0_DOMAIN,

      client_id: process.env.AUTH0_CLIENT_KEY,
      redirect_uri: window.location.origin,
    });
    console.log(auth0);
    app.provide("auth0", auth0);
  },
};
