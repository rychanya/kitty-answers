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
    <div class="field is-grouped is-grouped-multiline">
      <div class="control">
        <div class="tags has-addons">
          <span class="tag is-dark">
            <span class="icon"><i class="fas fa-tag"></i></span>
          </span>
          <span class="tag is-info">
            <router-link :to="{ name: 'QA', params: { id: qa._id } }">{{
              qa._id
            }}</router-link>
          </span>
        </div>
      </div>

      <div class="control">
        <div class="tags has-addons">
          <span class="tag is-dark">
            <span v-if="qa.by" class="icon"><i class="fas fa-user"></i></span>
            <span v-else class="icon"><i class="fas fa-paw"></i></span>
          </span>
          <span class="tag is-info">
            <template v-if="qa.by">{{ qa.by }}</template>
            <template v-else>котенок</template>
          </span>
        </div>
      </div>

      <div class="control" v-if="qa.incomplete">
        <div class="tags has-addons">
          <span class="tag is-dark">
            <span class="icon"><i class="fas fa-couch"></i></span>
          </span>
          <span class="tag is-danger"> неполный </span>
        </div>
      </div>
    </div>

    <div v-if="qa.correct" class="notification is-success is-light">
      <answer
        :answer="qa.correct"
        :answers="qa.answers"
        :type="qa.type"
      ></answer>
    </div>
    <template v-if="qa.incorrect.length > 0">
      <div class="buttons is-centered">
        <a class="button" @click="togleIncorrect()">{{
          isHasIncorrect
            ? "Скрыть неправильные ответы"
            : "Показать неправильные ответы"
        }}</a>
      </div>
      <template v-if="isHasIncorrect">
        <div
          class="notification is-danger is-light"
          v-for="el in qa.incorrect"
          :key="el"
        >
          <answer :answer="el" :answers="qa.answers" :type="qa.type"></answer>
        </div>
      </template>
    </template>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType, ref } from "vue";
import { QA } from "@/api/models";
import { useLink } from "vue-router";
import Answer from "./Answer.vue";
export default defineComponent({
  components: { Answer },
  props: {
    qa: Object as PropType<QA>,
    full: {
      default: false,
      type: Boolean,
    },
  },
  setup(props) {
    const { href } = useLink({
      to: { name: "QA", params: { id: props.qa?._id } },
    });
    const tShareURL = `https://t.me/share/url?url=${encodeURIComponent(
      window.location.origin + href.value
    )}`;
    let isHasIncorrect = ref<boolean>(false);
    const togleIncorrect = () => (isHasIncorrect.value = !isHasIncorrect.value);
    return { tShareURL, isHasIncorrect, togleIncorrect };
  },
});
</script>

<style></style>
