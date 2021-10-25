import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store, { key } from "./store";
import { loadIcons } from "@/icons";
import createAuth0Client, { Auth0Client } from "@auth0/auth0-spa-js";

loadIcons();
let AuthClient: Auth0Client;
createAuth0Client({
  domain: process.env.VUE_APP_AUTH0_DOMAIN,
  client_id: process.env.VUE_APP_AUTH0_CLIENT_KEY,
  redirect_uri: window.location.origin,
  audience: process.env.VUE_APP_AUTH0_AUDIENCE,
}).then((client) => {
  AuthClient = client;

  createApp(App).use(store, key).use(router).mount("#app");
});
export { AuthClient };
