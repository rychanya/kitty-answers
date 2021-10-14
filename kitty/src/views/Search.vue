<template>
  <div class="container">
    <div class="field has-addons">
      <div class="control is-expanded">
        <input
          class="input"
          type="text"
          placeholder=""
          @keypress.enter="searchClick()"
          v-model="q"
        />
      </div>
      <div class="control">
        <div class="button is-info" @click="searchClick()">
          <span class="icon is-left">
            <i class="fas fa-search"></i>
          </span>
        </div>
      </div>
    </div>
    <div class="columns is-multiline is-centered">
      <div class="column is-full">
        <div v-for="group in result" class="box block content" :key="group._id">
          <h1 class="title has-text-black is-6">{{ group._id.question }}</h1>
          <h2 class="subtitle has-text-grey-light is-6">
            {{ group._id.type }}
          </h2>
          <div v-for="qa in group.data" :key="qa._id">
            <QA :qa="qa"></QA>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { search } from "@/api/search";
import { SearchResult } from "@/api/models";
import QA from "@/components/QA.vue";
export default defineComponent({
  name: "Search",
  components: { QA },
  setup() {
    let q = ref("");
    let result = ref<Array<SearchResult>>([]);
    function searchClick() {
      search(q.value).then((data) => (result.value = data));
    }
    return { q, searchClick, result };
  },
});
</script>

<style></style>
