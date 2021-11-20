<template>
  <template v-if="isAuthenticated">
    <div class="navbar-item">
      <a class="button is-danger" @click="logout()">Выйти</a>
    </div>
    <div class="navbar-item">
      <span class="icon">
        <i class="fas fa-user"></i>
      </span>
    </div>
  </template>
  <template v-else>
    <div class="navbar-item">
      <a class="button is-outlined" @click="login()">Войти</a>
    </div>
  </template>
</template>

<script lang="ts">
import { defineComponent, computed } from "vue";
import { AuthClient } from "@/main";
import { RedirectLoginOptions, LogoutOptions } from "@auth0/auth0-spa-js";
import { useStore } from "vuex";
import { key } from "@/store/index";

export default defineComponent({
  setup() {
    const store = useStore(key);
    const user = computed(() => store.state.auth.user);
    const isAuthenticated = computed(() => store.state.auth.isAuthenticated);

    AuthClient.isAuthenticated().then((v) => {
      store.state.auth.isAuthenticated = v;
    });
    AuthClient.getUser().then((v) => {
      store.state.auth.user = v;
    });

    async function login(options?: RedirectLoginOptions) {
      await AuthClient.loginWithRedirect(options);
    }

    async function logout(options?: LogoutOptions) {
      store.state.auth.isAuthenticated = false;
      store.state.auth.user = undefined;
      await AuthClient.logout(options);
    }
    return { login, logout, user, isAuthenticated };
  },
});
</script>

<style></style>
