import { createStore, Store } from "vuex";
import { InjectionKey } from "vue";
import { User } from "@auth0/auth0-spa-js";

export interface State {
  auth: {
    isAuthenticated: boolean;
    user: User | undefined;
  };
}

export const key: InjectionKey<Store<State>> = Symbol();

export default createStore<State>({
  state: {
    auth: {
      isAuthenticated: false,
      user: undefined,
    },
  },
  mutations: {},
  actions: {},
  modules: {},
});
