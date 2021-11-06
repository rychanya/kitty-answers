<template>
  <section class="hero is-primary is-fullheight">
    <!-- Hero head: will stick at the top -->
    <div class="hero-head">
      <header class="navbar is-primary">
        <div class="container">
          <div class="navbar-brand">
            <router-link to="/" class="navbar-item" active-class="">
              <img src="@/assets/logo.png" alt="Logo" />
            </router-link>
            <span
              class="navbar-burger"
              data-target="navbarMenuHeroC"
              :class="{ 'is-active': isMenuActive }"
              @click="togleMenu()"
            >
              <span></span>
              <span></span>
              <span></span>
            </span>
          </div>
          <div
            id="navbarMenuHeroC"
            class="navbar-menu"
            :class="{ 'is-active': isMenuActive }"
          >
            <div class="navbar-start">
              <router-link
                to="/search"
                class="navbar-item"
                active-class="is-active"
              >
                <span class="icon"> <i class="fas fa-search"></i> </span>
              </router-link>

              <router-link
                v-if="isAuthenticated"
                to="/upload"
                class="navbar-item"
                active-class="is-active"
              >
                <span class="icon"> <i class="fas fa-file-excel"></i> </span>
              </router-link>
            </div>
            <div class="navbar-end">
              <auth-comp></auth-comp>
            </div>
          </div>
        </div>
      </header>
    </div>

    <!-- Hero content: will be in the middle -->
    <div class="hero-body">
      <router-view />
    </div>

    <!-- Hero footer: will stick at the bottom -->
    <div class="hero-foot">
      <button @click="testTask()">test</button>
    </div>
  </section>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from "vue";
import AuthComp from "@/components/Auth.vue";
import { useStore } from "vuex";
import { key } from "@/store/index";
import {testTask} from "@/api/search"

export default defineComponent({
  components: { AuthComp },
  setup() {
    const store = useStore(key);

    const user = computed(() => store.state.auth.user);
    const isAuthenticated = computed(() => store.state.auth.isAuthenticated);

    let isMenuActive = ref(false);
    const togleMenu = () => {
      isMenuActive.value = !isMenuActive.value;
    };

    return {
      isMenuActive,
      togleMenu,
      user,
      isAuthenticated,
      testTask
    };
  },
});
</script>

<style></style>
