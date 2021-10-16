import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faUserSecret,
  faJedi,
  faSearch,
  faPaw,
  faCouch,
  faThumbsUp,
  faThumbsDown,
  faTag,
  faUser,
} from "@fortawesome/free-solid-svg-icons";
import { faTelegram } from "@fortawesome/free-brands-svg-icons";
import { dom } from "@fortawesome/fontawesome-svg-core";
import { Auth0Plugin } from "@/auth/auth0-plugin";

library.add(
  faUserSecret,
  faJedi,
  faSearch,
  faPaw,
  faTelegram,
  faCouch,
  faThumbsUp,
  faThumbsDown,
  faTag,
  faUser
);

createApp(App).use(Auth0Plugin).use(store).use(router).mount("#app");

dom.watch();
