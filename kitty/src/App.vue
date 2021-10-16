<template>
  <section class="hero is-primary is-fullheight">
    <!-- Hero head: will stick at the top -->
    <div class="hero-head">
      <header class="navbar">
        <div class="container">
          <div class="navbar-brand">
            <router-link to="/" class="navbar-item" active-class="">
              <img src="@/assets/logo.png" alt="Logo" />
              Котята
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
            <div class="navbar-end">
              <router-link to="/" class="navbar-item" active-class="is-active"
                >Home</router-link
              >
              <router-link
                to="/search"
                class="navbar-item"
                active-class="is-active"
                >Search</router-link
              >
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
      <button @click="ddd">hhhhh</button>
    </div>
  </section>
</template>

<script lang="ts">
import { defineComponent, ref, inject } from "vue";

export default defineComponent({
  setup() {
    function ddd() {
      let k = inject("auth0");
      console.log(k);
    }
    let isMenuActive = ref(false);
    const togleMenu = () => {
      isMenuActive.value = !isMenuActive.value;
    };
    return { isMenuActive, togleMenu, ddd };
  },
});
</script>

<style></style>
