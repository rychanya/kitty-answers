<template>
  <div class="box">
    <template v-if="full">
      <h1 class="title has-text-black is-6">{{ qa.question }}</h1>
      <h2 class="subtitle has-text-grey-light is-6">
        {{ qa.type }}
      </h2></template
    >
    <div class="field is-grouped is-grouped-multiline">
      <div class="control">
        <div class="tags has-addons">
          <span class="tag is-dark">id</span>
          <span class="tag is-info">{{ qa._id }}</span>
        </div>
      </div>

      <div v-if="qa.by" class="control">
        <div class="tags has-addons">
          <span class="tag is-dark">by</span>
          <span class="tag is-info">{{ qa.by }}</span>
        </div>
      </div>
      <div v-else class="control">
        <div class="tags has-addons">
          <span class="tag is-dark">by</span>
          <span class="tag is-info"><i class="fas fa-paw"></i></span>
        </div>
      </div>

      <div v-if="qa.incomplete" class="control">
        <div class="tags has-addons">
          <span class="tag is-dark">!</span>
          <span class="tag is-danger">Добавлено сообщестовом</span>
        </div>
      </div>
    </div>
    <a :href="tShareURL">telega</a>
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
