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
          :disabled="isLoading"
        />
      </div>
      <div class="control">
        <div
          class="button is-info"
          @click="searchClick()"
          :class="{ 'is-loading': isLoading }"
        >
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
import { defineComponent, ref, onMounted } from "vue";
import { search as searchApi } from "@/api/search";
import { SearchResult } from "@/api/models";
import { useRoute, useRouter, onBeforeRouteUpdate } from "vue-router";

import QA from "@/components/QA.vue";
export default defineComponent({
  name: "Search",
  components: { QA },
  setup() {
    const route = useRoute();
    const router = useRouter();
    let q = ref("");
    let isLoading = ref<boolean>(false);
    let result = ref<Array<SearchResult>>([]);
    onBeforeRouteUpdate((to, from) => {
      if (to.query.q !== from.query.q) {
        if (to.query.q && typeof to.query.q === "string") {
          q.value = to.query.q;
        } else {
          q.value = "";
        }
        try {
          isLoading.value = true;
          search();
        } finally {
          isLoading.value = false;
        }
      }
    });
    function search() {
      if (q.value === "") {
        result.value = [];
      } else {
        searchApi(q.value).then((data) => (result.value = data));
      }
    }
    function searchClick() {
      router.push({ query: { q: q.value } });
    }
    onMounted(() => {
      if (route.query.q && typeof route.query.q === "string") {
        q.value = route.query.q as string;
        search();
      }
    });
    return { q, searchClick, result };
  },
});
</script>

<style></style>
