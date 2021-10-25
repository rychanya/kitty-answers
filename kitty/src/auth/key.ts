import { InjectionKey, Ref } from "vue";
import { User, RedirectLoginOptions } from "@auth0/auth0-spa-js";

const loginKey: InjectionKey<(options: RedirectLoginOptions) => void> =
  Symbol("login");
const logoutKey: InjectionKey<() => void> = Symbol("logout");
const getTokenSilentlyKey: InjectionKey<() => void> =
  Symbol("getTokenSilently");
const userKey: InjectionKey<Ref<User>> = Symbol("user");
const isAuthenticatedKey: InjectionKey<Ref<boolean>> =
  Symbol("isAuthenticated");
const isLoadingKey: InjectionKey<Ref<boolean>> = Symbol("isLoading");

export {
  loginKey,
  logoutKey,
  getTokenSilentlyKey,
  userKey,
  isAuthenticatedKey,
  isLoadingKey,
};
