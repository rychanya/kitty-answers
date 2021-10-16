<template>
  <div class="box">
    <template v-if="full">
      <h1 class="title has-text-black is-6">{{ qa.question }}</h1>
      <h2 class="subtitle has-text-grey-light is-6">
        {{ qa.type }}
      </h2>
    </template>

    <div class="level is-mobile">
      <div class="level-left">
        <a
          class="level-item"
          :href="tShareURL"
          target="blank"
          rel="noopener noreferrer"
        >
          <span class="icon">
            <i class="fab fa-telegram"></i>
          </span>
        </a>
        <router-link
          class="level-item"
          :to="{ name: 'QA', params: { id: qa._id } }"
        >
          <span class="icon">
            <i class="fas fa-tag"></i>
          </span>
        </router-link>
        <a
          class="level-item"
          v-if="qa.by"
          :href="tShareURL"
          target="blank"
          rel="noopener noreferrer"
        >
          <span class="icon">
            <i class="fas fa-user"></i>
          </span>
        </a>
        <a v-else>
          <span class="icon">
            <i class="fas fa-paw"></i>
          </span>
        </a>
        <a
          v-if="qa.incomplete"
          class="level-item"
          :href="tShareURL"
          target="blank"
          rel="noopener noreferrer"
        >
          <span class="icon">
            <i class="fas fa-couch"></i>
          </span>
        </a>
      </div>

      <div class="level-right">
        <span class="icon-text level-item">
          <span class="icon">
            <i class="fas fa-thumbs-down"></i>
          </span>
          <span>Home</span> </span
        ><span class="icon-text level-item">
          <span class="icon">
            <i class="fas fa-thumbs-up"></i>
          </span>
          <span>Home</span>
        </span>
      </div>
    </div>
    {{ qa }}
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import { QA } from "@/api/models";
import { useLink } from "vue-router";
export default defineComponent({
  props: {
    qa: Object as PropType<QA>,
    full: {
      default: false,
      type: Boolean,
    },
  },
  setup(props) {
    const { href } = useLink({ to: "/" });
    const tShareURL = `https://t.me/share/url?url=${encodeURIComponent(
      window.location.origin + href.value
    )}&text=${encodeURIComponent("Нашлось в котятах")}`;
    return { tShareURL };
  },
});
</script>

<style></style>
