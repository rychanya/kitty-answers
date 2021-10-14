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
} from "@fortawesome/free-solid-svg-icons";
import { dom } from "@fortawesome/fontawesome-svg-core";

library.add(faUserSecret, faJedi, faSearch, faPaw);

createApp(App).use(store).use(router).mount("#app");

dom.watch();
